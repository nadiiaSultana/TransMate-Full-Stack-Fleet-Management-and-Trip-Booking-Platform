from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import CustomerRegisterSerializer, DriverRegisterSerializer, LoginSerializer, UserProfileSerializer, UserListSerializer
from .permissions import IsAdminUserRole

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'refresh': str(refresh), 'access': str(refresh.access_token)}

class CustomerRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        s=CustomerRegisterSerializer(data=request.data)
        if s.is_valid():
            u=s.save(); return Response({'message':'Customer registered successfully.','user':UserProfileSerializer(u).data,'tokens':get_tokens_for_user(u)}, status=201)
        return Response(s.errors, status=400)
class DriverRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        s=DriverRegisterSerializer(data=request.data)
        if s.is_valid():
            u=s.save(); return Response({'message':'Driver registration submitted successfully. Wait for admin approval.','user':UserProfileSerializer(u).data}, status=201)
        return Response(s.errors, status=400)
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        s=LoginSerializer(data=request.data)
        if s.is_valid():
            u=s.validated_data['user']
            if u.role=='DRIVER' and not u.is_verified: return Response({'detail':'Driver account is not approved by admin yet.'}, status=403)
            return Response({'message':'Login successful.','user':UserProfileSerializer(u).data,'tokens':get_tokens_for_user(u)})
        return Response(s.errors, status=400)
class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request): return Response(UserProfileSerializer(request.user).data)
    def patch(self, request):
        s=UserProfileSerializer(request.user, data=request.data, partial=True)
        if s.is_valid(): s.save(); return Response({'message':'Profile updated successfully.','user':s.data})
        return Response(s.errors, status=400)
class AdminUserListView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self, request): return Response(UserListSerializer(User.objects.all().order_by('-created_at'), many=True).data)
class AdminDriverListView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self, request): return Response(UserListSerializer(User.objects.filter(role='DRIVER').order_by('-created_at'), many=True).data)
class AdminApproveDriverView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def patch(self, request, driver_id):
        try: d=User.objects.get(id=driver_id, role='DRIVER')
        except User.DoesNotExist: return Response({'detail':'Driver not found.'}, status=404)
        d.is_verified=True; d.is_active=True; d.save(); return Response({'message':'Driver approved successfully.','driver':UserProfileSerializer(d).data})
class AdminSuspendUserView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def patch(self, request, user_id):
        try: u=User.objects.get(id=user_id)
        except User.DoesNotExist: return Response({'detail':'User not found.'}, status=404)
        u.is_active=False; u.save(); return Response({'message':'User suspended successfully.','user':UserProfileSerializer(u).data})
class AdminActivateUserView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def patch(self, request, user_id):
        try: u=User.objects.get(id=user_id)
        except User.DoesNotExist: return Response({'detail':'User not found.'}, status=404)
        u.is_active=True; u.save(); return Response({'message':'User activated successfully.','user':UserProfileSerializer(u).data})
