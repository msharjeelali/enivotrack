from rest_framework import serializers
from .models import Camera


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = (
            "id",
            "name",
            "rtsp_url",
            "location",
            "is_active",
            "created_at",
            "updated_at",
            "owner",
        )
        read_only_fields = ("id", "created_at", "updated_at", "owner")

    def validate_rtsp_url(self, value):
        value = (value or "").strip()
        if not value:
            raise serializers.ValidationError("rtsp_url must not be empty.")
        return value