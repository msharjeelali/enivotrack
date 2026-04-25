# core/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.permissions import AllowAny
from .views import HealthView

urlpatterns = [
    path("admin/", admin.site.urls),

    # health
    path("health/", HealthView.as_view(), name="health"),

    # v1
    path("api/<version>/users/", include("users.urls")),
    path("api/<version>/cameras/", include("cameras.urls")),

    # docs
    path("schema/", SpectacularAPIView.as_view(permission_classes=[AllowAny]), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]