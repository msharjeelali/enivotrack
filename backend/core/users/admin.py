from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserModelAdmin(UserAdmin):
    model = User
    list_display = ("email", "username", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active", "is_staff")
    search_fields = ("email", "name")
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("name",)}),
        ("Access Control", {"fields": ("role",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("name", "role")}),
    )


admin.site.register(User, UserModelAdmin)