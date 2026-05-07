from django.urls import path
from .views import *
urlpatterns=[path('',CustomerRatingListCreateView.as_view()),path('driver/<int:driver_id>/',DriverRatingListView.as_view()),path('admin/all/',AdminRatingListView.as_view())]
