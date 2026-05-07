from django.contrib import admin
from .models import VehicleType, Vehicle
@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin): list_display=('id','name','base_fare','per_km_rate','capacity','is_active')
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin): list_display=('id','registration_number','vehicle_type','driver','status'); list_filter=('status','vehicle_type')
