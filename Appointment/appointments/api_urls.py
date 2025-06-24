from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import BookingListCreateAPI, TimeSlotViewSet, BookingViewSet, MyBookingsView, CancelBookingView, CancelledBookingsForProviderView

router = DefaultRouter()
router.register(r'timeslots', TimeSlotViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('bookings/', BookingListCreateAPI.as_view(), name='api-booking-list-create'),
    path('bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='api-booking-cancel'),
    path('bookings/my/', MyBookingsView.as_view(), name='api-my-bookings'),
    path('', include(router.urls)),
    path('bookings/cancelled/', CancelledBookingsForProviderView.as_view(), name='api-cancelled-bookings-provider'),
]