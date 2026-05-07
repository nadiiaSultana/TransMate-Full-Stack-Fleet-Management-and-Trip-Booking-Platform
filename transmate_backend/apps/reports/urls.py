from django.urls import path
from .views import *
urlpatterns=[path('admin/summary/',AdminDashboardSummaryView.as_view()),path('admin/bookings/',AdminBookingReportView.as_view()),path('admin/payments/',AdminPaymentReportView.as_view()),path('admin/vehicles/',AdminVehicleUsageReportView.as_view())]
