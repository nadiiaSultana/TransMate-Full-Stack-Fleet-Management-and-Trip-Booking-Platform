from rest_framework import serializers
from .models import VehicleMaintenance
class VehicleMaintenanceSerializer(serializers.ModelSerializer):
    vehicle_registration_number=serializers.CharField(source='vehicle.registration_number',read_only=True); vehicle_model=serializers.CharField(source='vehicle.model',read_only=True)
    class Meta: model=VehicleMaintenance; fields=['id','vehicle','vehicle_registration_number','vehicle_model','maintenance_type','title','description','cost','scheduled_date','completed_date','service_provider','status','created_at']; read_only_fields=['id','created_at']
