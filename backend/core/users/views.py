from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
import logging

from .models import User
from .serializers import (
    ChangePasswordSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    UserSerializer,
)

logger = logging.getLogger(__name__)


class UserListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = User.objects.all().order_by("-date_joined")
        role = self.request.query_params.get("role")
        is_active = self.request.query_params.get("is_active")

        if role:
            if role not in User.Role.values:
                raise ValidationError(
                    {"role": f"Invalid role. Choose from: {User.Role.values}"}
                )
            queryset = queryset.filter(role=role)

        if is_active is not None:
            if is_active.lower() not in ("true", "false"):
                raise ValidationError({"is_active": "Must be 'true' or 'false'"})
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateUserSerializer
        return UserSerializer


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    http_method_names = ["get", "patch", "delete"]

    def get_queryset(self):
        return User.objects.all()

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFound({"detail": "User not found."})

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UpdateUserSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.is_active:
            raise ValidationError({"detail": "User is already deactivated."})
        user.is_active = False
        user.save()
        logger.info(f"User {user.email} deactivated")
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=UserSerializer)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(request=UpdateUserSerializer, responses=UserSerializer)
    def patch(self, request):
        serializer = UpdateUserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(responses={204: None})
    def delete(self, request):
        user = request.user
        if not user.is_active:
            raise ValidationError({"detail": "Account is already deactivated."})
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=ChangePasswordSerializer, responses={200: None})
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Password changed successfully."})