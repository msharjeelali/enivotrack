import logging

from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Camera
from .serializers import (
    CameraSerializer,
    CreateCameraSerializer,
    UpdateCameraSerializer,
)

logger = logging.getLogger(__name__)


class CameraListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Camera.objects.all().order_by("-created_at")

        status_param = self.request.query_params.get("status")
        location = self.request.query_params.get("location")

        if status_param:
            if status_param not in Camera.Status.values:
                raise ValidationError(
                    {"status": f"Invalid status. Choose from: {Camera.Status.values}"}
                )
            queryset = queryset.filter(status=status_param)

        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateCameraSerializer
        return CameraSerializer


class CameraRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        return Camera.objects.all()

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound({"detail": "Camera not found."})

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateCameraSerializer
        return CameraSerializer

    def destroy(self, request, *args, **kwargs):
        camera = self.get_object()

        if camera.status == Camera.Status.REMOVED:
            raise ValidationError({"detail": "Camera is already removed."})

        camera.status = Camera.Status.REMOVED
        camera.save()
        logger.info(f"Camera {camera.id} removed")
        return Response(status=status.HTTP_204_NO_CONTENT)