from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
urlpatterns = [
    path('register/customer/', CustomerRegisterView.as_view()), path('register/driver/', DriverRegisterView.as_view()),
    path('login/', LoginView.as_view()), path('token/refresh/', TokenRefreshView.as_view()), path('profile/', ProfileView.as_view()),
    path('admin/users/', AdminUserListView.as_view()), path('admin/drivers/', AdminDriverListView.as_view()), path('admin/drivers/<int:driver_id>/approve/', AdminApproveDriverView.as_view()),
    path('admin/users/<int:user_id>/suspend/', AdminSuspendUserView.as_view()), path('admin/users/<int:user_id>/activate/', AdminActivateUserView.as_view()),
]
