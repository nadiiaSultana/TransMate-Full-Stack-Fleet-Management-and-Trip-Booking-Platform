from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id','username','email','phone','role','is_verified','is_active')
    list_filter = ('role','is_verified','is_active')
    search_fields = ('username','email','phone')
    fieldsets = UserAdmin.fieldsets + (("TransMate Info", {'fields': ('phone','role','profile_image','address','is_verified')}),)
