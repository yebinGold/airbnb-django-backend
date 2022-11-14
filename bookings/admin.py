from django.contrib import admin
from .models import Booking

# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("kind", "user", "room", "experience", "guests")
    list_filter = ("kind",)