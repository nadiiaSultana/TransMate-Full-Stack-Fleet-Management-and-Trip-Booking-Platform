from rest_framework import serializers
from .models import Trip
from apps.bookings.models import Booking
from apps.users.models import User
from apps.vehicles.models import Vehicle
class TripAssignSerializer(serializers.Serializer):
    booking_id=serializers.IntegerField(); driver_id=serializers.IntegerField(); vehicle_id=serializers.IntegerField()
    def validate_booking_id(self,id):
        try:b=Booking.objects.get(id=id)
        except Booking.DoesNotExist: raise serializers.ValidationError('Booking not found.')
        if b.status not in ['ACCEPTED','PENDING']: raise serializers.ValidationError('Only pending or accepted bookings can be assigned.')
        if hasattr(b,'trip'): raise serializers.ValidationError('This booking already has a trip assigned.')
        return id
    def validate_driver_id(self,id):
        try:d=User.objects.get(id=id,role='DRIVER')
        except User.DoesNotExist: raise serializers.ValidationError('Driver not found.')
        if not d.is_verified or not d.is_active: raise serializers.ValidationError('Driver is not approved or inactive.')
        return id
    def validate_vehicle_id(self,id):
        try:v=Vehicle.objects.get(id=id)
        except Vehicle.DoesNotExist: raise serializers.ValidationError('Vehicle not found.')
        if v.status!='AVAILABLE': raise serializers.ValidationError('Vehicle is not available.')
        return id
    def validate(self,a):
        v=Vehicle.objects.get(id=a['vehicle_id'])
        if v.driver and v.driver.id != a['driver_id']: raise serializers.ValidationError({'driver_id':'This vehicle is assigned to another driver.'})
        if Trip.objects.filter(driver_id=a['driver_id'], status__in=['ASSIGNED','ACCEPTED','ONGOING']).exists(): raise serializers.ValidationError({'driver_id':'This driver already has an active trip.'})
        return a
class TripListSerializer(serializers.ModelSerializer):
    booking_id=serializers.IntegerField(source='booking.id',read_only=True); customer_name=serializers.CharField(source='booking.customer.username',read_only=True); customer_phone=serializers.CharField(source='booking.customer.phone',read_only=True); pickup_location=serializers.CharField(source='booking.pickup_location',read_only=True); dropoff_location=serializers.CharField(source='booking.dropoff_location',read_only=True); driver_name=serializers.CharField(source='driver.username',read_only=True); driver_phone=serializers.CharField(source='driver.phone',read_only=True); vehicle_registration_number=serializers.CharField(source='vehicle.registration_number',read_only=True); vehicle_model=serializers.CharField(source='vehicle.model',read_only=True)
    class Meta: model=Trip; fields=['id','booking_id','customer_name','customer_phone','pickup_location','dropoff_location','driver','driver_name','driver_phone','vehicle','vehicle_registration_number','vehicle_model','actual_distance_km','final_fare','status','start_time','end_time','created_at','updated_at']
class TripDetailSerializer(TripListSerializer):
    booking_status=serializers.CharField(source='booking.status',read_only=True); estimated_fare=serializers.DecimalField(source='booking.estimated_fare',max_digits=10,decimal_places=2,read_only=True); distance_km=serializers.DecimalField(source='booking.distance_km',max_digits=10,decimal_places=2,read_only=True); customer_id=serializers.IntegerField(source='booking.customer.id',read_only=True); customer_email=serializers.CharField(source='booking.customer.email',read_only=True); pickup_latitude=serializers.DecimalField(source='booking.pickup_latitude',max_digits=10,decimal_places=7,read_only=True); pickup_longitude=serializers.DecimalField(source='booking.pickup_longitude',max_digits=10,decimal_places=7,read_only=True); dropoff_latitude=serializers.DecimalField(source='booking.dropoff_latitude',max_digits=10,decimal_places=7,read_only=True); dropoff_longitude=serializers.DecimalField(source='booking.dropoff_longitude',max_digits=10,decimal_places=7,read_only=True); driver_email=serializers.CharField(source='driver.email',read_only=True); vehicle_type=serializers.CharField(source='vehicle.vehicle_type.name',read_only=True); vehicle_color=serializers.CharField(source='vehicle.color',read_only=True)
    class Meta: model=Trip; fields=TripListSerializer.Meta.fields+['booking_status','estimated_fare','distance_km','customer_id','customer_email','pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude','driver_email','vehicle_type','vehicle_color']
class TripCompleteSerializer(serializers.Serializer):
    actual_distance_km=serializers.DecimalField(max_digits=10,decimal_places=2,required=False); final_fare=serializers.DecimalField(max_digits=10,decimal_places=2,required=False)
