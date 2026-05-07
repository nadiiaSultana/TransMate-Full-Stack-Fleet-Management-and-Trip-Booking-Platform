from django.urls import path
from .views import *
urlpatterns=[path('types/',PublicVehicleTypeListView.as_view()),path('admin/types/',AdminVehicleTypeListCreateView.as_view()),path('admin/types/<int:vehicle_type_id>/',AdminVehicleTypeDetailView.as_view()),path('admin/vehicles/',AdminVehicleListCreateView.as_view()),path('admin/vehicles/<int:vehicle_id>/',AdminVehicleDetailView.as_view()),path('admin/vehicles/<int:vehicle_id>/assign-driver/',AdminAssignDriverToVehicleView.as_view())]
