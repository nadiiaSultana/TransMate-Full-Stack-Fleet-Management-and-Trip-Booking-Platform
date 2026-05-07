from django.db import models
from apps.users.models import User
from apps.bookings.models import Booking
class Complaint(models.Model):
    STATUS_CHOICES=(('OPEN','Open'),('IN_REVIEW','In Review'),('RESOLVED','Resolved'),('REJECTED','Rejected'))
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='complaints'); booking=models.ForeignKey(Booking,on_delete=models.SET_NULL,null=True,blank=True,related_name='complaints'); subject=models.CharField(max_length=255); message=models.TextField(); status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='OPEN'); admin_reply=models.TextField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    def __str__(self): return self.subject
