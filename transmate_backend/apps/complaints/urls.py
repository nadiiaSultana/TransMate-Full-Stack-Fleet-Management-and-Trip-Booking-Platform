from django.urls import path
from .views import *
urlpatterns=[path('',MyComplaintListCreateView.as_view()),path('<int:complaint_id>/',MyComplaintDetailView.as_view()),path('admin/all/',AdminComplaintListView.as_view()),path('admin/<int:complaint_id>/',AdminComplaintDetailView.as_view()),path('admin/<int:complaint_id>/reply/',AdminComplaintReplyView.as_view())]
