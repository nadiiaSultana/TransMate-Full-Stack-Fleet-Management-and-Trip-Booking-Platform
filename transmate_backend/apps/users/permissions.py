from rest_framework.permissions import BasePermission
class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view): return bool(request.user and request.user.is_authenticated and request.user.role == 'ADMIN')
class IsDriverUserRole(BasePermission):
    def has_permission(self, request, view): return bool(request.user and request.user.is_authenticated and request.user.role == 'DRIVER')
class IsCustomerUserRole(BasePermission):
    def has_permission(self, request, view): return bool(request.user and request.user.is_authenticated and request.user.role == 'CUSTOMER')
