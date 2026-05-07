from rest_framework import serializers
from .models import Rating
from apps.trips.models import Trip
class RatingCreateSerializer(serializers.ModelSerializer):
    trip_id=serializers.IntegerField(write_only=True)
    class Meta: model=Rating; fields=['id','trip_id','rating','review','created_at']; read_only_fields=['id','created_at']
    def validate_trip_id(self,id):
        try:t=Trip.objects.get(id=id,booking__customer=self.context['request'].user)
        except Trip.DoesNotExist: raise serializers.ValidationError('Trip not found.')
        if t.status!='COMPLETED': raise serializers.ValidationError('Only completed trips can be rated.')
        if hasattr(t,'rating'): raise serializers.ValidationError('This trip has already been rated.')
        return id
    def validate_rating(self,r):
        if r<1 or r>5: raise serializers.ValidationError('Rating must be between 1 and 5.')
        return r
    def create(self,d):
        t=Trip.objects.get(id=d.pop('trip_id')); return Rating.objects.create(trip=t,customer=self.context['request'].user,driver=t.driver,**d)
class RatingDetailSerializer(serializers.ModelSerializer):
    trip_id=serializers.IntegerField(source='trip.id',read_only=True); customer_name=serializers.CharField(source='customer.username',read_only=True); driver_name=serializers.CharField(source='driver.username',read_only=True)
    class Meta: model=Rating; fields=['id','trip_id','customer','customer_name','driver','driver_name','rating','review','created_at']
