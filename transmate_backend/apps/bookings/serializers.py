from rest_framework import serializers
from .models import Booking
class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking; fields=['id','vehicle_type','pickup_location','dropoff_location','pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude','distance_km','estimated_fare','status','booking_time']; read_only_fields=['id','estimated_fare','status','booking_time']
    def validate_vehicle_type(self, v):
        if not v.is_active: raise serializers.ValidationError('This vehicle type is currently inactive.')
        return v
    def validate_distance_km(self, d):
        if d <= 0: raise serializers.ValidationError('Distance must be greater than 0.')
        return d
    def create(self, data):
        vt=data['vehicle_type']; d=data['distance_km']; fare=vt.base_fare+(d*vt.per_km_rate)
        return Booking.objects.create(customer=self.context['request'].user, estimated_fare=fare, status='PENDING', **data)
class BookingListSerializer(serializers.ModelSerializer):
    customer_name=serializers.CharField(source='customer.username',read_only=True); customer_phone=serializers.CharField(source='customer.phone',read_only=True); vehicle_type_name=serializers.CharField(source='vehicle_type.name',read_only=True)
    class Meta: model=Booking; fields=['id','customer','customer_name','customer_phone','vehicle_type','vehicle_type_name','pickup_location','dropoff_location','distance_km','estimated_fare','status','booking_time','updated_at']
class BookingDetailSerializer(BookingListSerializer):
    customer_email=serializers.CharField(source='customer.email',read_only=True); vehicle_base_fare=serializers.DecimalField(source='vehicle_type.base_fare',max_digits=10,decimal_places=2,read_only=True); vehicle_per_km_rate=serializers.DecimalField(source='vehicle_type.per_km_rate',max_digits=10,decimal_places=2,read_only=True)
    class Meta: model=Booking; fields=['id','customer','customer_name','customer_email','customer_phone','vehicle_type','vehicle_type_name','vehicle_base_fare','vehicle_per_km_rate','pickup_location','dropoff_location','pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude','distance_km','estimated_fare','status','cancellation_reason','booking_time','updated_at']
class BookingCancelSerializer(serializers.Serializer): cancellation_reason=serializers.CharField(required=False, allow_blank=True)
class BookingStatusUpdateSerializer(serializers.Serializer): status=serializers.ChoiceField(choices=['PENDING','ACCEPTED','ASSIGNED','ONGOING','COMPLETED','CANCELLED'])
