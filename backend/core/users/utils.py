import uuid

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User


token_generator = PasswordResetTokenGenerator()


def user_pk_to_uid(user: User) -> str:
    return urlsafe_base64_encode(force_bytes(str(user.pk)))


def uid_to_user(uid: str) -> User | None:
    try:
        raw = force_str(urlsafe_base64_decode(uid))
        user_id = uuid.UUID(raw)
    except Exception:
        return None
    return User.objects.filter(pk=user_id).first()


def frontend_url(path: str) -> str:
    base = getattr(settings, "FRONTEND_BASE_URL", "").rstrip("/")
    path = "/" + path.lstrip("/")
    return f"{base}{path}" if base else path

