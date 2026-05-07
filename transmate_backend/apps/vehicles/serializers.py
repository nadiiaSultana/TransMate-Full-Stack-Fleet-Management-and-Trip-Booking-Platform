from rest_framework import serializers
from .models import VehicleType, Vehicle
from apps.users.models import User
class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=VehicleType; fields='__all__'; read_only_fields=['id','created_at']
class VehicleSerializer(serializers.ModelSerializer):
    vehicle_type_name=serializers.CharField(source='vehicle_type.name', read_only=True); driver_name=serializers.CharField(source='driver.username', read_only=True); driver_phone=serializers.CharField(source='driver.phone', read_only=True)
    class Meta:
        model=Vehicle; fields=['id','vehicle_type','vehicle_type_name','driver','driver_name','driver_phone','registration_number','model','color','capacity','status','created_at']; read_only_fields=['id','created_at']
    def validate_driver(self, driver):
        if driver and driver.role!='DRIVER': raise serializers.ValidationError('Selected user is not a driver.')
        if driver and not driver.is_verified: raise serializers.ValidationError('Driver is not approved yet.')
        return driver
class VehicleAssignDriverSerializer(serializers.Serializer):
    driver_id=serializers.IntegerField()
    def validate_driver_id(self, driver_id):
        try: driver=User.objects.get(id=driver_id, role='DRIVER')
        except User.DoesNotExist: raise serializers.ValidationError('Driver not found.')
        if not driver.is_verified: raise serializers.ValidationError('Driver is not approved yet.')
        return driver_id
