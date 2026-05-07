from django.utils import timezone
from django.db.models import Sum, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import VehicleMaintenance
from .serializers import VehicleMaintenanceSerializer
from apps.users.permissions import IsAdminUserRole
class AdminMaintenanceListCreateView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request):
        qs=VehicleMaintenance.objects.all().order_by('-created_at'); sf=request.query_params.get('status'); vid=request.query_params.get('vehicle_id')
        if sf: qs=qs.filter(status=sf.upper())
        if vid: qs=qs.filter(vehicle_id=vid)
        return Response(VehicleMaintenanceSerializer(qs,many=True).data)
    def post(self,request):
        s=VehicleMaintenanceSerializer(data=request.data)
        if s.is_valid():
            r=s.save();
            if r.status in ['SCHEDULED','IN_PROGRESS']: r.vehicle.status='MAINTENANCE'; r.vehicle.save()
            return Response({'message':'Maintenance record created successfully.','maintenance':VehicleMaintenanceSerializer(r).data},status=201)
        return Response(s.errors,status=400)
class AdminMaintenanceDetailView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def obj(self,id):
        try:return VehicleMaintenance.objects.get(id=id)
        except VehicleMaintenance.DoesNotExist:return None
    def get(self,request,maintenance_id):
        r=self.obj(maintenance_id); return Response(VehicleMaintenanceSerializer(r).data) if r else Response({'detail':'Maintenance record not found.'},status=404)
    def patch(self,request,maintenance_id):
        r=self.obj(maintenance_id)
        if not r:return Response({'detail':'Maintenance record not found.'},status=404)
        s=VehicleMaintenanceSerializer(r,data=request.data,partial=True)
        if s.is_valid():
            r=s.save()
            if r.status in ['SCHEDULED','IN_PROGRESS']: r.vehicle.status='MAINTENANCE'; r.vehicle.save()
            if r.status=='COMPLETED':
                if not r.completed_date: r.completed_date=timezone.now().date(); r.save()
                r.vehicle.status='AVAILABLE'; r.vehicle.save()
            return Response({'message':'Maintenance record updated successfully.','maintenance':VehicleMaintenanceSerializer(r).data})
        return Response(s.errors,status=400)
    def delete(self,request,maintenance_id):
        r=self.obj(maintenance_id)
        if not r:return Response({'detail':'Maintenance record not found.'},status=404)
        r.status='CANCELLED'; r.save();
        if r.vehicle.status=='MAINTENANCE': r.vehicle.status='AVAILABLE'; r.vehicle.save()
        return Response({'message':'Maintenance record cancelled successfully.'})
class AdminMaintenanceReportView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request):
        by_type=VehicleMaintenance.objects.values('maintenance_type').annotate(count=Count('id'),total_cost=Sum('cost'))
        return Response({'total_records':VehicleMaintenance.objects.count(),'scheduled':VehicleMaintenance.objects.filter(status='SCHEDULED').count(),'in_progress':VehicleMaintenance.objects.filter(status='IN_PROGRESS').count(),'completed':VehicleMaintenance.objects.filter(status='COMPLETED').count(),'total_completed_cost':VehicleMaintenance.objects.filter(status='COMPLETED').aggregate(total=Sum('cost'))['total'] or 0,'by_type':list(by_type)})
