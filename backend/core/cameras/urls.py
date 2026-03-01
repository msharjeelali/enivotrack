from .views import CameraViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cameras', CameraViewSet, basename='camera')

urlpatterns = router.urls