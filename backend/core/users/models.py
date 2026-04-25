import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.functions import Lower
from django.db import models


class CustomUserManager(UserManager):
    """
    We keep Django's `AbstractUser` for admin compatibility, but treat `email`
    as the login identifier. We also normalize email and ensure `username`
    is always populated to satisfy `AbstractUser` constraints.
    """

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("The email address must be set.")
        email = self.normalize_email(email).lower()
        if not username:
            username = email
        return super()._create_user(username=username, email=email, password=password, **extra_fields)

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username=username, email=email, password=password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        return self._create_user(username=username, email=email, password=password, **extra_fields)


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        USER = "user", "User"

    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255, blank=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        db_index=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    class Meta:
        db_table = "users"
        constraints = [
            # Enforce case-insensitive uniqueness at the DB level.
            models.UniqueConstraint(Lower("email"), name="users_email_ci_unique"),
        ]
        permissions = [
            ("is_admin", "General Administrative Access"),
        ]


