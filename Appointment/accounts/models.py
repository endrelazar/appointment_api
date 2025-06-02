from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('provider', 'Provider'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')