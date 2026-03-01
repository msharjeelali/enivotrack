from django.contrib import admin

# Register your models here.
from .models import Owner, Vehicle

admin.site.register(Owner)
admin.site.register(Vehicle)