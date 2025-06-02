from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from appointments.models import TimeSlot, Booking

class RegistrationTest(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'tesztuser',
            'email': 'teszt@teszt.hu',
            'password1': 'Tesztjelszo123',
            'password2': 'Tesztjelszo123',
            'role': 'client',
        })
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue(User.objects.filter(username='tesztuser').exists())

class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tesztuser', password='Tesztjelszo123', role='client')

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'tesztuser',
            'password': 'Tesztjelszo123',
        })
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue('_auth_user_id' in self.client.session)

class BookingTest(TestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(username='client', password='Tesztjelszo123', role='client')
        self.provider = User.objects.create_user(username='provider', password='Tesztjelszo123', role='provider')
        self.slot = TimeSlot.objects.create(provider=self.provider, start='2025-06-01 10:00', end='2025-06-01 11:00')

    def test_booking(self):
        self.client.login(username='client', password='Tesztjelszo123')
        response = self.client.post(reverse('book_slot', args=[self.slot.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Booking.objects.filter(client=self.client_user, timeslot=self.slot).exists())