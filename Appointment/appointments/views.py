from .models import TimeSlot
from .forms import TimeSlotForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Booking
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.contrib import messages
import logging

logger = logging.getLogger('appointments')

@login_required
def available_slots(request):
    slots = TimeSlot.objects.filter(is_booked=False)
    return render(request, 'appointments/available_slots.html', {'slots': slots})


@login_required
def book_slot(request, slot_id):
    try:
        slot = get_object_or_404(TimeSlot, id=slot_id, is_booked=False)
        logger.info(f"User {request.user.username} is attempting to book slot {slot_id}.")
        if request.user.role != 'client':
            messages.error(request, "Only clients can book appointments.")
            return redirect('available_slots')
        if request.method == 'POST':
            
            if slot.is_booked:
                messages.error(request, "This timeslot has already been booked.")
                return redirect('available_slots')
            Booking.objects.create(client=request.user, timeslot=slot)
            slot.is_booked = True
            slot.save()
            send_mail(
                subject='Appointment Booking Confirmation',
                message=f'You have successfully booked the appointment: {slot.start} - {slot.end} (Provider: {slot.provider.username})',
                from_email=None,
                recipient_list=[request.user.email],
            )
            messages.success(request, "Booking successful!")
            logger.info(f"Slot {slot_id} booked successfully by user {request.user.username}.")
            return redirect('my_bookings')
        return render(request, 'appointments/book_slot.html', {'slot': slot})
    except Exception as e:
        logger.error(f"Error booking slot {slot_id} for user {request.user.username}: {e}")
        messages.error(request, f"An error occurred during booking: {e}")
        return redirect('available_slots')
    
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(client=request.user)
    return render(request, 'appointments/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    try:
        booking = get_object_or_404(Booking, id=booking_id, client=request.user)
        if request.method == 'POST':
            slot = booking.timeslot
            slot.is_booked = False
            slot.save()
            booking.delete()
            messages.success(request, "Booking cancelled successfully.")
            logger.info(f"Booking {booking_id} cancelled by user {request.user.username}.")
            return redirect('my_bookings')
        return render(request, 'appointments/cancel_booking.html', {'booking': booking})
    except Booking.DoesNotExist:
        messages.error(request, "This booking was not found or you do not have permission to cancel it.")
        logger.warning(f"User {request.user.username} tried to cancel a non-existent booking {booking_id}.")
        return redirect('my_bookings')
    except Exception as e:
        messages.error(request, f"An error occurred during cancellation: {e}")
        logger.error(f"Error cancelling booking {booking_id} for user {request.user.username}: {e}")
        return redirect('my_bookings')

@staff_member_required  
def calendar_api(request):
    from .models import Booking  
    bookings = Booking.objects.select_related('timeslot', 'client', 'timeslot__provider')
    data = []
    for booking in bookings:
        data.append({
            'id': booking.id,
            'client': booking.client.username,
            'provider': booking.timeslot.provider.username,
            'start': booking.timeslot.start,
            'end': booking.timeslot.end,
        })
    return JsonResponse(data, safe=False)

@login_required
def create_timeslot(request):
    if request.user.role != 'provider':
        messages.error(request, "Only provider can make appointments.")
        logger.error(f"User {request.user.username} attempted to create a timeslot without provider role.")
        return redirect('home')
    try:
        if request.method == 'POST':
            form = TimeSlotForm(request.POST)
            if form.is_valid():
                timeslot = form.save(commit=False)
                timeslot.provider = request.user
                timeslot.save()
                messages.success(request, "Appointment created successfully!")
                logger.info(f"Timeslot created successfully by user {request.user.username}.")
                return redirect('timeslot_list')
            else:
                logger.warning(f"Invalid form submission by user {request.user.username}: {form.errors}")
                messages.error(request, "Invalid data! Please check the fields.")
        else:
            form = TimeSlotForm()
        return render(request, 'appointments/create_timeslot.html', {'form': form})
    except Exception as e:
        messages.error(request, f"An error occurred while creating the timeslot: {e}")
        logger.error(f"Error creating timeslot for user {request.user.username}: {e}")
        return redirect('timeslot_list')
    
@login_required
def timeslot_list(request):
    slots = TimeSlot.objects.filter(provider=request.user)
    return render(request, 'appointments/timeslot_list.html', {'slots': slots})