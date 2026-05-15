from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CameraViewSet

router = DefaultRouter()
router.register("cameras", CameraViewSet, basename="camera")

urlpatterns = [
    path("", include(router.urls)),
]