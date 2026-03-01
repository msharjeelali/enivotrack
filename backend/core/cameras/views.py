from .models import Camera
from .serializers import CameraSerializer

from rest_framework import viewsets
from rest_framework.response import Response

class CameraViewSet(viewsets.ModelViewSet):
    serializer_class = CameraSerializer

    def get_queryset(self):
        return Camera.objects.all()