from django.db import models
from accounts.models import User

class TimeSlot(models.Model):
    provider = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'provider'})
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.provider.username}: {self.start} - {self.end}"
    
class Booking(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', limit_choices_to={'role': 'client'})
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.client.username} reserved: {self.timeslot}"