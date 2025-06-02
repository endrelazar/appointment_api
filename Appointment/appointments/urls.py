from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_timeslot, name='create_timeslot'),
    path('my-slots/', views.timeslot_list, name='timeslot_list'),
    path('available/', views.available_slots, name='available_slots'),
    path('book/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('calendar-api/', views.calendar_api, name='calendar_api'),
]