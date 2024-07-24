from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    number_plate = models.CharField(max_length=10, unique=True)
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
    VEHICLE_TYPE_CHOICES = [
        ('lorry', 'Lorry'),
        ('pickup', 'Pickup'),
        ('van', 'Van'),
    ]
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.vehicle_type} - {self.number_plate}"

class ServiceBooking(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('LongDistance', 'Long Distance'),
        ('LocalMoving', 'Local Moving'),
        ('MovingKits', 'Moving Kits'),
        ('StorageUnits', 'Storage Units'),
        ('BookDelivery', 'Book Delivery'),
        ('LoadingUnloading', 'Loading/Unloading')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100, choices=SERVICE_TYPE_CHOICES)
    source_location = models.CharField(max_length=255)
    destination_location = models.CharField(max_length=255)
    assigned_driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} - {self.service_type}"
