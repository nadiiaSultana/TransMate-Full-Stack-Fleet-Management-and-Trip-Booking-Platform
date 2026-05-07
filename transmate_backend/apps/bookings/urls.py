from django.urls import path
from .views import *
urlpatterns=[path('',CustomerBookingListCreateView.as_view()),path('<int:booking_id>/',CustomerBookingDetailView.as_view()),path('<int:booking_id>/cancel/',CustomerCancelBookingView.as_view()),path('admin/all/',AdminBookingListView.as_view()),path('admin/<int:booking_id>/',AdminBookingDetailView.as_view()),path('admin/<int:booking_id>/accept/',AdminAcceptBookingView.as_view()),path('admin/<int:booking_id>/cancel/',AdminCancelBookingView.as_view()),path('admin/<int:booking_id>/status/',AdminUpdateBookingStatusView.as_view())]
