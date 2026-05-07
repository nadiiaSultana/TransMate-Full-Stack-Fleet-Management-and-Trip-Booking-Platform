from django.db import models
from apps.users.models import User
from apps.vehicles.models import VehicleType
class Booking(models.Model):
    STATUS_CHOICES=(('PENDING','Pending'),('ACCEPTED','Accepted'),('ASSIGNED','Assigned'),('ONGOING','Ongoing'),('COMPLETED','Completed'),('CANCELLED','Cancelled'))
    customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='bookings',limit_choices_to={'role':'CUSTOMER'})
    vehicle_type=models.ForeignKey(VehicleType,on_delete=models.SET_NULL,null=True,related_name='bookings')
    pickup_location=models.TextField(); dropoff_location=models.TextField()
    pickup_latitude=models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True); pickup_longitude=models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    dropoff_latitude=models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True); dropoff_longitude=models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    distance_km=models.DecimalField(max_digits=10, decimal_places=2); estimated_fare=models.DecimalField(max_digits=10, decimal_places=2)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDING'); booking_time=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True); cancellation_reason=models.TextField(null=True, blank=True)
    def __str__(self): return f"Booking #{self.id} - {self.customer.username} - {self.status}"
