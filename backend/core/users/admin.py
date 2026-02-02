from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Register your models here.
class UserModelAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Access Control', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(User, UserModelAdmin)