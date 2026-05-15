import uuid

from django.db import models


# Create your models here.
class Owner(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    name = models.CharField(
        max_length=100
        )
    email = models.EmailField(
        unique=True
        )

    def __str__(self):
        return f"Owner: {self.name}, Email: {self.email}"

class Vehicle(models.Model):

    BODY_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('wagon', 'Wagon'),
        ('hatchback', 'Hatchback'),
        ('bus', 'Bus'),
        ('motorcycle', 'Motorcycle'),
        ('rickshaw', 'Rickshaw'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
        )
    plate = models.CharField(
        max_length=10,
        unique=True
        )
    year = models.IntegerField()
    make = models.CharField(
        max_length=50
        )
    model = models.CharField(
        max_length=50
        )
    capacity = models.IntegerField()
    body_type = models.CharField(
        max_length=50,
        choices=BODY_TYPE_CHOICES
        )
    date = models.DateTimeField(
        auto_now_add=True
        )
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        related_name='vehicles',
        null=True,
        blank=True
        )


