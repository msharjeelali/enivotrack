from .models import Camera

from rest_framework import serializers

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'