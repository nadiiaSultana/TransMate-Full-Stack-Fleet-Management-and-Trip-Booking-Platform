from django.contrib import admin
from .models import Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin): list_display=('id','booking','customer','amount','payment_method','status'); list_filter=('payment_method','status')
