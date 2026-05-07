from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import VehicleType, Vehicle
from .serializers import VehicleTypeSerializer, VehicleSerializer, VehicleAssignDriverSerializer
from apps.users.models import User
from apps.users.permissions import IsAdminUserRole
class PublicVehicleTypeListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request): return Response(VehicleTypeSerializer(VehicleType.objects.filter(is_active=True).order_by('name'), many=True).data)
class AdminVehicleTypeListCreateView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self, request): return Response(VehicleTypeSerializer(VehicleType.objects.all().order_by('-created_at'), many=True).data)
    def post(self, request):
        s=VehicleTypeSerializer(data=request.data)
        if s.is_valid(): s.save(); return Response({'message':'Vehicle type created successfully.','vehicle_type':s.data}, status=201)
        return Response(s.errors, status=400)
class AdminVehicleTypeDetailView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def obj(self,id):
        try:return VehicleType.objects.get(id=id)
        except VehicleType.DoesNotExist:return None
    def get(self,request,vehicle_type_id):
        o=self.obj(vehicle_type_id); return Response(VehicleTypeSerializer(o).data) if o else Response({'detail':'Vehicle type not found.'}, status=404)
    def patch(self,request,vehicle_type_id):
        o=self.obj(vehicle_type_id)
        if not o: return Response({'detail':'Vehicle type not found.'}, status=404)
        s=VehicleTypeSerializer(o,data=request.data,partial=True)
        if s.is_valid(): s.save(); return Response({'message':'Vehicle type updated successfully.','vehicle_type':s.data})
        return Response(s.errors,status=400)
    def delete(self,request,vehicle_type_id):
        o=self.obj(vehicle_type_id)
        if not o: return Response({'detail':'Vehicle type not found.'}, status=404)
        o.is_active=False; o.save(); return Response({'message':'Vehicle type deactivated successfully.'})
class AdminVehicleListCreateView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request): return Response(VehicleSerializer(Vehicle.objects.all().order_by('-created_at'), many=True).data)
    def post(self,request):
        s=VehicleSerializer(data=request.data)
        if s.is_valid(): s.save(); return Response({'message':'Vehicle created successfully.','vehicle':s.data}, status=201)
        return Response(s.errors,status=400)
class AdminVehicleDetailView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def obj(self,id):
        try:return Vehicle.objects.get(id=id)
        except Vehicle.DoesNotExist:return None
    def get(self,request,vehicle_id):
        o=self.obj(vehicle_id); return Response(VehicleSerializer(o).data) if o else Response({'detail':'Vehicle not found.'}, status=404)
    def patch(self,request,vehicle_id):
        o=self.obj(vehicle_id)
        if not o:return Response({'detail':'Vehicle not found.'}, status=404)
        s=VehicleSerializer(o,data=request.data,partial=True)
        if s.is_valid(): s.save(); return Response({'message':'Vehicle updated successfully.','vehicle':s.data})
        return Response(s.errors,status=400)
    def delete(self,request,vehicle_id):
        o=self.obj(vehicle_id)
        if not o:return Response({'detail':'Vehicle not found.'}, status=404)
        o.status='INACTIVE'; o.save(); return Response({'message':'Vehicle deactivated successfully.'})
class AdminAssignDriverToVehicleView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def patch(self, request, vehicle_id):
        try: v=Vehicle.objects.get(id=vehicle_id)
        except Vehicle.DoesNotExist: return Response({'detail':'Vehicle not found.'}, status=404)
        s=VehicleAssignDriverSerializer(data=request.data)
        if s.is_valid():
            d=User.objects.get(id=s.validated_data['driver_id'], role='DRIVER')
            if Vehicle.objects.filter(driver=d).exclude(id=v.id).exists(): return Response({'detail':'This driver is already assigned to another vehicle.'}, status=400)
            v.driver=d; v.save(); return Response({'message':'Driver assigned to vehicle successfully.','vehicle':VehicleSerializer(v).data})
        return Response(s.errors,status=400)
