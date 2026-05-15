from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Camera
from .services.redis_publisher import publish_camera_event


@receiver(post_save, sender=Camera)
def camera_saved(sender, instance: Camera, created: bool, **kwargs):
    action = "created" if created else "updated"
    publish_camera_event(instance, action)


@receiver(post_delete, sender=Camera)
def camera_deleted(sender, instance: Camera, **kwargs):
    publish_camera_event(instance, "deleted")

