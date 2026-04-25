from rest_framework.permissions import BasePermission


class IsRoleAdmin(BasePermission):
    """
    Authorization is based on our domain role, not Django `is_staff`.
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and getattr(user, "role", None) == "admin")

