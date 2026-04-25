from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .utils import token_generator, user_pk_to_uid, frontend_url

User = get_user_model()


def build_set_password_link(*, user) -> str:
    uid = user_pk_to_uid(user)
    token = token_generator.make_token(user)
    # Frontend typically consumes `uid` + `token` to render a "Set password" screen.
    return frontend_url(f"/set-password?uid={uid}&token={token}")


def build_reset_password_link(*, user) -> str:
    uid = user_pk_to_uid(user)
    token = token_generator.make_token(user)
    return frontend_url(f"/reset-password?uid={uid}&token={token}")


def send_invite_email(*, user, invited_by) -> None:
    """
    Uses Django's email backend abstraction. Tokens are never logged.
    """
    context = {
        "user": user,
        "invited_by": invited_by,
        "set_password_link": build_set_password_link(user=user),
        "support_email": getattr(settings, "SUPPORT_EMAIL", None),
    }
    subject = "You’ve been invited to Envirotrack"
    body = render_to_string("users/emails/invite.txt", context)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    msg = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=[user.email])
    msg.send(fail_silently=False)


def send_password_reset_email(*, user) -> None:
    context = {
        "user": user,
        "reset_password_link": build_reset_password_link(user=user),
        "support_email": getattr(settings, "SUPPORT_EMAIL", None),
    }
    subject = "Reset your Envirotrack password"
    body = render_to_string("users/emails/password_reset.txt", context)
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    msg = EmailMultiAlternatives(subject=subject, body=body, from_email=from_email, to=[user.email])
    msg.send(fail_silently=False)


def invalidate_user_sessions(*, user) -> int:
    """
    Best-effort session invalidation for the Django session backend.
    (No-op for JWT-only clients, but helps if you also use session auth.)
    """
    deleted = 0
    now = timezone.now()
    for session in Session.objects.filter(expire_date__gte=now):
        data = session.get_decoded()
        if str(data.get("_auth_user_id")) == str(user.pk):
            session.delete()
            deleted += 1
    return deleted

