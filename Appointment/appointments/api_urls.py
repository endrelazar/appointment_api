from django.urls import path
from .api_views import BookingListCreateAPI

urlpatterns = [
    path('bookings/', BookingListCreateAPI.as_view(), name='api-booking-list-create'),
]