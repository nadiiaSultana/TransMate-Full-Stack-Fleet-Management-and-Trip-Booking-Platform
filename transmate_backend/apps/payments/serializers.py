from rest_framework import serializers
from .models import Payment
from apps.bookings.models import Booking
class PaymentCreateSerializer(serializers.ModelSerializer):
    booking_id=serializers.IntegerField(write_only=True)
    class Meta: model=Payment; fields=['id','booking_id','amount','payment_method','transaction_id','status','paid_at','created_at']; read_only_fields=['id','amount','status','paid_at','created_at']
    def validate_booking_id(self,id):
        try:b=Booking.objects.get(id=id,customer=self.context['request'].user)
        except Booking.DoesNotExist: raise serializers.ValidationError('Booking not found.')
        if b.status!='COMPLETED': raise serializers.ValidationError('Payment can only be made for completed bookings.')
        if hasattr(b,'payment'): raise serializers.ValidationError('Payment already exists for this booking.')
        return id
    def create(self,d):
        bid=d.pop('booking_id'); b=Booking.objects.get(id=bid); amt=b.trip.final_fare if hasattr(b,'trip') and b.trip.final_fare else b.estimated_fare
        return Payment.objects.create(booking=b,customer=self.context['request'].user,amount=amt,status='PENDING',**d)
class PaymentDetailSerializer(serializers.ModelSerializer):
    booking_id=serializers.IntegerField(source='booking.id',read_only=True); customer_name=serializers.CharField(source='customer.username',read_only=True); pickup_location=serializers.CharField(source='booking.pickup_location',read_only=True); dropoff_location=serializers.CharField(source='booking.dropoff_location',read_only=True)
    class Meta: model=Payment; fields=['id','booking_id','customer','customer_name','pickup_location','dropoff_location','amount','payment_method','transaction_id','gateway_payment_id','gateway_callback_url','status','paid_at','created_at']
class PaymentConfirmSerializer(serializers.Serializer): transaction_id=serializers.CharField(required=False, allow_blank=True)
class PaymentRefundSerializer(serializers.Serializer): reason=serializers.CharField(required=False, allow_blank=True)
