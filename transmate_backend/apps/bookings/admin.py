from django.contrib import admin
from .models import Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin): list_display=('id','customer','vehicle_type','status','estimated_fare','booking_time'); list_filter=('status','vehicle_type')
