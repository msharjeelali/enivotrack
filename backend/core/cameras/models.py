import uuid

from django.db import models

# Create your models here.
class Camera(models.Model):
    
    CAMERA_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('removed', 'Removed'),
    ]

    stream_url = models.URLField(unique=True)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=50, choices=CAMERA_STATUS_CHOICES, default='active')