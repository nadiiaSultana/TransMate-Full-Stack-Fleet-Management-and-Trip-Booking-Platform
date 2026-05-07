from django.contrib import admin
from .models import Trip
@admin.register(Trip)
class TripAdmin(admin.ModelAdmin): list_display=('id','booking','driver','vehicle','status','start_time','end_time'); list_filter=('status',)
