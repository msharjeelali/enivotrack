import logging
from django.db import transaction
from django.http import Http404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsRoleAdmin
from .serializers import (
    AdminInviteUserSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    ResendInviteSerializer,
    SetPasswordSerializer,
    UpdateUserSerializer,
    UserSerializer,
)
from .services import (
    invalidate_user_sessions,
    send_invite_email,
    send_password_reset_email,
)
from .utils import token_generator, uid_to_user

logger = logging.getLogger(__name__)


@extend_schema(tags=["users"])
class AdminUserListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsRoleAdmin]

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
        return UserSerializer


@extend_schema(tags=["users"])
class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsRoleAdmin]
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


@extend_schema(tags=["users"])
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

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


@extend_schema(tags=["users"])
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

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


@extend_schema(tags=["users"])
class AdminInviteUserView(APIView):
    permission_classes = [IsAuthenticated, IsRoleAdmin]

    @extend_schema(request=AdminInviteUserSerializer, responses={201: None})
    def post(self, request):
        serializer = AdminInviteUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        name = serializer.validated_data["name"]
        role = serializer.validated_data.get("role") or User.Role.USER

        with transaction.atomic():
            if User.objects.filter(email__iexact=email).exists():
                raise ValidationError({"email": "A user with this email already exists."})

            user = User(
                email=email,
                username=email,  # kept for AbstractUser compatibility
                name=name,
                role=role,
                is_active=False,
            )
            user.set_unusable_password()
            user.full_clean(exclude=["password"])
            user.save()

        send_invite_email(user=user, invited_by=request.user)
        return Response(status=status.HTTP_201_CREATED)


@extend_schema(tags=["users"])
class AdminResendInviteView(APIView):
    permission_classes = [IsAuthenticated, IsRoleAdmin]

    @extend_schema(request=ResendInviteSerializer, responses={200: None})
    def post(self, request):
        serializer = ResendInviteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError({"detail": "User not found."})
        if user.is_active:
            raise ValidationError({"detail": "User is already active."})

        send_invite_email(user=user, invited_by=request.user)
        return Response({"detail": "Invite link sent."})


@extend_schema(tags=["users"])
class SetPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=SetPasswordSerializer, responses={200: None})
    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = uid_to_user(serializer.validated_data["uid"])
        if not user:
            raise ValidationError({"detail": "Invalid link."})

        token = serializer.validated_data["token"]
        if not token_generator.check_token(user, token):
            raise ValidationError({"detail": "This link is invalid or has expired."})

        user.name = serializer.validated_data["name"]
        user.set_password(serializer.validated_data["password"])
        user.is_active = True
        user.save(update_fields=["name", "password", "is_active"])

        return Response({"detail": "Password set successfully."})


@extend_schema(tags=["users"])
class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: None})
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )


@extend_schema(tags=["users"])
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=ForgotPasswordSerializer, responses={200: None})
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = User.objects.filter(email__iexact=email).first()
        if user and user.is_active:
            send_password_reset_email(user=user)

        # Always succeed to prevent email enumeration.
        return Response({"detail": "If that email exists, a reset link has been sent."})


@extend_schema(tags=["users"])
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=ResetPasswordSerializer, responses={200: None})
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = uid_to_user(serializer.validated_data["uid"])
        if not user:
            raise ValidationError({"detail": "Invalid link."})

        token = serializer.validated_data["token"]
        if not token_generator.check_token(user, token):
            raise ValidationError({"detail": "This link is invalid or has expired."})

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])
        invalidate_user_sessions(user=user)

        return Response({"detail": "Password reset successfully."})