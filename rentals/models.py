from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Bike(models.Model):
    STATUS_CHOICES = (
        ('rented', 'Rented'),
        ('available', 'Available'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rentals')
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='bike_rentals')
    start_time = models.DateField(auto_now_add=True)
    end_time = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
