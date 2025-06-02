from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from appointments.models import TimeSlot, Booking

class BookingAPITest(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(username='client', password='Tesztjelszo123', role='client')
        self.provider = User.objects.create_user(username='provider', password='Tesztjelszo123', role='provider')
        self.slot = TimeSlot.objects.create(provider=self.provider, start='2025-06-01 10:00', end='2025-06-01 11:00')
        self.api_client = APIClient()

    def test_api_booking_create(self):
        self.api_client.login(username='client', password='Tesztjelszo123')
        response = self.api_client.post(
            reverse('api-booking-list-create'),
            {'timeslot': self.slot.id}
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Booking.objects.filter(client=self.client_user, timeslot=self.slot).exists())