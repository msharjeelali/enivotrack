import uuid
from django.db import models


class SmokeEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    camera_id = models.UUIDField(null=True, blank=True)
    image = models.ImageField(upload_to="smoke_events/%Y/%m/%d/")
    detected_at = models.DateTimeField(auto_now_add=True)
    confidence = models.FloatField()
    intensity = models.FloatField()

    def __str__(self):
        return f"SmokeEvent {self.id} at {self.detected_at}"

    class Meta:
        db_table = "smoke_events"
        ordering = ["-detected_at"]