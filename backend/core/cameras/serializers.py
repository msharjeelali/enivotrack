from rest_framework import serializers
from .models import Camera


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = (
            "id",
            "stream_url",
            "location",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class CreateCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ("id", "stream_url", "location", "status")
        read_only_fields = ("id",)

    def validate_stream_url(self, value):
        if Camera.objects.filter(stream_url=value).exists():
            raise serializers.ValidationError("A camera with this stream URL already exists.")
        return value

    def validate_status(self, value):
        if value == Camera.Status.REMOVED:
            raise serializers.ValidationError("Cannot create a camera with status 'removed'.")
        return value


class UpdateCameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ("stream_url", "location", "status")

    def validate_stream_url(self, value):
        camera = self.instance
        if Camera.objects.filter(stream_url=value).exclude(pk=camera.pk).exists():
            raise serializers.ValidationError("A camera with this stream URL already exists.")
        return value

    def validate_status(self, value):
        camera = self.instance
        if camera.status == Camera.Status.REMOVED:
            raise serializers.ValidationError("Cannot update a removed camera.")
        return value