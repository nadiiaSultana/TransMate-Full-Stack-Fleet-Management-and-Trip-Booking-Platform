from django.contrib import admin
from .models import VehicleMaintenance
@admin.register(VehicleMaintenance)
class VehicleMaintenanceAdmin(admin.ModelAdmin): list_display=('id','vehicle','maintenance_type','title','cost','scheduled_date','completed_date','status'); list_filter=('status','maintenance_type','scheduled_date')
