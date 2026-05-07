from django.db import models
from apps.users.models import User
from apps.trips.models import Trip
class Rating(models.Model):
    trip=models.OneToOneField(Trip,on_delete=models.CASCADE,related_name='rating'); customer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='given_ratings',limit_choices_to={'role':'CUSTOMER'}); driver=models.ForeignKey(User,on_delete=models.CASCADE,related_name='received_ratings',limit_choices_to={'role':'DRIVER'}); rating=models.PositiveIntegerField(); review=models.TextField(null=True,blank=True); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Rating {self.rating} for {self.driver.username}"
