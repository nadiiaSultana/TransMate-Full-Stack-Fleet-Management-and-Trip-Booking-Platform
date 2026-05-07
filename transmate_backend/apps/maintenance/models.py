from django.db import models
from apps.vehicles.models import Vehicle
class VehicleMaintenance(models.Model):
    STATUS_CHOICES=(('SCHEDULED','Scheduled'),('IN_PROGRESS','In Progress'),('COMPLETED','Completed'),('CANCELLED','Cancelled'))
    MAINTENANCE_TYPE_CHOICES=(('GENERAL_SERVICE','General Service'),('ENGINE','Engine'),('TIRE','Tire'),('BRAKE','Brake'),('OIL_CHANGE','Oil Change'),('BODY_REPAIR','Body Repair'),('OTHER','Other'))
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE,related_name='maintenance_records'); maintenance_type=models.CharField(max_length=30,choices=MAINTENANCE_TYPE_CHOICES); title=models.CharField(max_length=255); description=models.TextField(null=True,blank=True); cost=models.DecimalField(max_digits=10,decimal_places=2,default=0); scheduled_date=models.DateField(); completed_date=models.DateField(null=True,blank=True); service_provider=models.CharField(max_length=255,null=True,blank=True); status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='SCHEDULED'); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.vehicle.registration_number} - {self.title}"
