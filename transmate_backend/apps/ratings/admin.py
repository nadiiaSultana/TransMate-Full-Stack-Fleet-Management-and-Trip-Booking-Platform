from django.contrib import admin
from .models import Rating
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin): list_display=('id','trip','customer','driver','rating','created_at'); list_filter=('rating',)
