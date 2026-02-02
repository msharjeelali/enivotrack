import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "OPERATOR", "Operator"

    email = models.EmailField(unique=True)
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.ADMIN
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        permissions = [
            ("is_admin", "General Administrative Access"),
            ("can_add_user", "Can add new user (Admin / Operator)")
        ]

