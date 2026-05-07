from django.db import models
from apps.users.models import User
from apps.bookings.models import Booking
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES=(('CASH','Cash'),('BKASH','bKash'),('NAGAD','Nagad'),('ROCKET','Rocket'),('CARD','Card'))
    STATUS_CHOICES=(('PENDING','Pending'),('INITIATED','Initiated'),('PAID','Paid'),('FAILED','Failed'),('REFUNDED','Refunded'))
    booking=models.OneToOneField(Booking,on_delete=models.CASCADE,related_name='payment'); customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='payments',limit_choices_to={'role':'CUSTOMER'}); amount=models.DecimalField(max_digits=10,decimal_places=2); payment_method=models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES); transaction_id=models.CharField(max_length=100,null=True,blank=True); gateway_payment_id=models.CharField(max_length=255,null=True,blank=True); gateway_callback_url=models.URLField(null=True,blank=True); gateway_response=models.JSONField(null=True,blank=True); status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDING'); paid_at=models.DateTimeField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Payment #{self.id} - {self.payment_method} - {self.status}"
