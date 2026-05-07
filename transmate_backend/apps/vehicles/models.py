from django.db import models
from apps.users.models import User
class VehicleType(models.Model):
    name=models.CharField(max_length=100, unique=True); base_fare=models.DecimalField(max_digits=10, decimal_places=2); per_km_rate=models.DecimalField(max_digits=10, decimal_places=2); capacity=models.PositiveIntegerField(); description=models.TextField(null=True, blank=True); is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
class Vehicle(models.Model):
    STATUS_CHOICES=(('AVAILABLE','Available'),('BUSY','Busy'),('INACTIVE','Inactive'),('MAINTENANCE','Maintenance'))
    vehicle_type=models.ForeignKey(VehicleType,on_delete=models.CASCADE, related_name='vehicles')
    driver=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_vehicle',limit_choices_to={'role':'DRIVER'})
    registration_number=models.CharField(max_length=50, unique=True); model=models.CharField(max_length=100); color=models.CharField(max_length=50,null=True,blank=True); capacity=models.PositiveIntegerField(); status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='AVAILABLE'); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.registration_number} - {self.vehicle_type.name}"
