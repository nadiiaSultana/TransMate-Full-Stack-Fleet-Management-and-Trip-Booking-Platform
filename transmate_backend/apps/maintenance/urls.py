from django.urls import path
from .views import *
urlpatterns=[path('admin/all/',AdminMaintenanceListCreateView.as_view()),path('admin/<int:maintenance_id>/',AdminMaintenanceDetailView.as_view()),path('admin/report/',AdminMaintenanceReportView.as_view())]
