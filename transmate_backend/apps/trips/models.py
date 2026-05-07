from django.db import models
from apps.bookings.models import Booking
from apps.users.models import User
from apps.vehicles.models import Vehicle
class Trip(models.Model):
    STATUS_CHOICES=(('ASSIGNED','Assigned'),('ACCEPTED','Accepted'),('ONGOING','Ongoing'),('COMPLETED','Completed'),('CANCELLED','Cancelled'))
    booking=models.OneToOneField(Booking,on_delete=models.CASCADE,related_name='trip')
    driver=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='driver_trips',limit_choices_to={'role':'DRIVER'})
    vehicle=models.ForeignKey(Vehicle,on_delete=models.SET_NULL,null=True,related_name='trips')
    start_time=models.DateTimeField(null=True,blank=True); end_time=models.DateTimeField(null=True,blank=True); actual_distance_km=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True); final_fare=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True); status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='ASSIGNED'); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return f"Trip #{self.id} - Booking #{self.booking.id} - {self.status}"
