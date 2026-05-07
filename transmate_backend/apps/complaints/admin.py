from django.contrib import admin
from .models import Complaint
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin): list_display=('id','user','subject','status','created_at'); list_filter=('status',)
