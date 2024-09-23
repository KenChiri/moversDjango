from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from booking.models import *


class MoversAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active']
    list_filter = ['is_active']  # Ensure this is a list or tuple
    search_fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
admin.site.register(ServiceBooking)
admin.site.register(Driver)
admin.site.register(Vehicle)