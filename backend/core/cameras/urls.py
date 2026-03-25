from django.urls import path
from . import views

urlpatterns = [
    path("", views.CameraListCreateView.as_view(), name="camera-list-create"),
    path("<uuid:pk>/", views.CameraRetrieveUpdateDestroyView.as_view(), name="camera-detail"),
]