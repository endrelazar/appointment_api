from rest_framework import generics, permissions, status, viewsets
from .permissions import IsProvider
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import TimeSlot, Booking
from .serializers import BookingSerializer, TimeSlotSerializer
from rest_framework.response import Response
import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger('appointments')

class BookingListCreateAPI(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save(client=self.request.user)
        send_mail(
            'Foglalás visszaigazolás',
            f'Sikeresen lefoglaltad az időpontot: {booking.timeslot}',
            settings.DEFAULT_FROM_EMAIL,
            [self.request.user.email],
            fail_silently=True,
        )

    def get_queryset(self):
        return Booking.objects.filter(client=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
           
            slot_id = request.data.get('timeslot')
            if not slot_id:
                logger.warning(f"API: User {request.user.username} tried to book without timeslot.")
                return Response({'error': 'Missing time identifier'}, status=status.HTTP_400_BAD_REQUEST)
            logger.info(f"API:User {request.user.username} is attempting to create a booking for slot {slot_id}.")
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"API: Error creating booking: {str(e)}")
            return Response({'error': f'An error occured: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer

    def get_permissions(self):
        # Csak provider hozhat létre, módosíthat, törölhet
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsProvider()]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Az időpont provider mezőjét automatikusan a bejelentkezett userre állítjuk
        serializer.save(provider=self.request.user)

    def get_queryset(self):
        # Csak a saját időpontjait lássa a provider, egyébként mindenki láthatja
        user = self.request.user
        if user.is_authenticated and getattr(user, 'role', None) == 'provider':
            return TimeSlot.objects.filter(provider=user)
        return TimeSlot.objects.all()


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(client=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, client=request.user)
        except Booking.DoesNotExist:
            return Response({'detail': 'Foglalás nem található.'}, status=status.HTTP_404_NOT_FOUND)
        booking.status = 'cancelled'
        booking.save()
        return Response({'detail': 'Foglalás lemondva.'}, status=status.HTTP_200_OK)
    
class CancelledBookingsForProviderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Csak provider szerepű felhasználó
        if getattr(request.user, 'role', None) != 'provider':
            return Response({'detail': 'Csak szolgáltatók számára elérhető!'}, status=403)
        # A provider saját időpontjaihoz tartozó lemondott foglalások
        cancelled_bookings = Booking.objects.filter(
            timeslot__provider=request.user,
            status='cancelled'
        ).select_related('client', 'timeslot')
        serializer = BookingSerializer(cancelled_bookings, many=True)
        return Response(serializer.data)
