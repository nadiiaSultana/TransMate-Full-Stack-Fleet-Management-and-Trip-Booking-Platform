from django.utils import timezone
from django.db import transaction
from django.db.models import Sum
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Trip
from .serializers import *
from apps.bookings.models import Booking
from apps.users.models import User
from apps.vehicles.models import Vehicle
from apps.payments.models import Payment
from apps.users.permissions import IsAdminUserRole, IsDriverUserRole, IsCustomerUserRole
from apps.notifications.utils import create_notification
class AdminAssignTripView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    @transaction.atomic
    def post(self,request):
        s=TripAssignSerializer(data=request.data)
        if s.is_valid():
            b=Booking.objects.get(id=s.validated_data['booking_id']); d=User.objects.get(id=s.validated_data['driver_id']); v=Vehicle.objects.get(id=s.validated_data['vehicle_id'])
            t=Trip.objects.create(booking=b,driver=d,vehicle=v,status='ASSIGNED'); b.status='ASSIGNED'; b.save(); v.status='BUSY'; v.driver=d; v.save()
            create_notification(b.customer,'Trip Assigned',f'Your booking #{b.id} has been assigned to driver {d.username}.', True); create_notification(d,'New Trip Assigned',f'You have been assigned trip #{t.id}. Pickup: {b.pickup_location}.', True)
            return Response({'message':'Trip assigned successfully.','trip':TripDetailSerializer(t).data}, status=201)
        return Response(s.errors,status=400)
class AdminTripListView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request):
        qs=Trip.objects.all().order_by('-created_at'); sf=request.query_params.get('status')
        if sf: qs=qs.filter(status=sf.upper())
        return Response(TripListSerializer(qs,many=True).data)
class AdminTripDetailView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request,trip_id):
        try:t=Trip.objects.get(id=trip_id)
        except Trip.DoesNotExist:return Response({'detail':'Trip not found.'},status=404)
        return Response(TripDetailSerializer(t).data)
class DriverAssignedTripListView(APIView):
    permission_classes=[IsAuthenticated, IsDriverUserRole]
    def get(self,request): return Response(TripListSerializer(Trip.objects.filter(driver=request.user).order_by('-created_at'),many=True).data)
class DriverActiveTripView(APIView):
    permission_classes=[IsAuthenticated, IsDriverUserRole]
    def get(self,request):
        t=Trip.objects.filter(driver=request.user,status__in=['ASSIGNED','ACCEPTED','ONGOING']).order_by('-created_at').first()
        return Response(TripDetailSerializer(t).data) if t else Response({'detail':'No active trip found.'},status=404)
class DriverTripDetailView(APIView):
    permission_classes=[IsAuthenticated, IsDriverUserRole]
    def get(self,request,trip_id):
        try:t=Trip.objects.get(id=trip_id,driver=request.user)
        except Trip.DoesNotExist:return Response({'detail':'Trip not found.'},status=404)
        return Response(TripDetailSerializer(t).data)
class DriverAcceptTripView(APIView):
    permission_classes=[IsAuthenticated, IsDriverUserRole]
    def patch(self,request,trip_id):
        try:t=Trip.objects.get(id=trip_id,driver=request.user)
        except Trip.DoesNotExist:return Response({'detail':'Trip not found.'},status=404)
        if t.status!='ASSIGNED': return Response({'detail':'Only assigned trips can be accepted.'},status=400)
        t.status='ACCEPTED'; t.save(); return Response({'message':'Trip accepted successfully.','trip':TripDetailSerializer(t).data})
class DriverStartTripView(APIView):
    permission_classes=[IsAuthenticated, IsDriverUserRole]
    @transaction.atomic
    def patch(self,request,trip_id):
        try:t=Trip.objects.get(id=trip_id,driver=request.user)
        except Trip.DoesNotExist:return Response({'detail':'Trip not found.'},status=404)
        if t.status not in ['ASSIGNED','ACCEPTED']: return Response({'detail':'Only assigned or accepted trips can be started.'},status=400)
        t.status='ONGOING'; t.start_time=timezone.now(); t.save(); t.booking.status='ONGOING'; t.booking.save(); create_notification(t.booking.customer,'Trip Started',f'Your trip #{t.id} has started.',True); return Response({'message':'Trip started successfully.','trip':TripDetailSerializer(t).data})
class DriverCompleteTripView(APIView):
    permission_classes=[IsAuthenticated, IsDriverUserRole]
    @transaction.atomic
    def patch(self,request,trip_id):
        try:t=Trip.objects.get(id=trip_id,driver=request.user)
        except Trip.DoesNotExist:return Response({'detail':'Trip not found.'},status=404)
        if t.status!='ONGOING': return Response({'detail':'Only ongoing trips can be completed.'},status=400)
        s=TripCompleteSerializer(data=request.data)
        if s.is_valid():
            t.status='COMPLETED'; t.end_time=timezone.now(); t.actual_distance_km=s.validated_data.get('actual_distance_km',t.booking.distance_km); t.final_fare=s.validated_data.get('final_fare',t.booking.estimated_fare); t.save(); t.booking.status='COMPLETED'; t.booking.save()
            if t.vehicle: t.vehicle.status='AVAILABLE'; t.vehicle.save()
            create_notification(t.booking.customer,'Trip Completed',f'Your trip #{t.id} has been completed. Final fare: BDT {t.final_fare}.',True); return Response({'message':'Trip completed successfully.','trip':TripDetailSerializer(t).data})
        return Response(s.errors,status=400)
class CustomerTripHistoryView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def get(self,request): return Response(TripListSerializer(Trip.objects.filter(booking__customer=request.user).order_by('-created_at'),many=True).data)
class CustomerTripDetailView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def get(self,request,trip_id):
        try:t=Trip.objects.get(id=trip_id,booking__customer=request.user)
        except Trip.DoesNotExist:return Response({'detail':'Trip not found.'},status=404)
        return Response(TripDetailSerializer(t).data)
class DriverEarningsReportView(APIView):
    permission_classes=[IsAuthenticated, IsDriverUserRole]
    def get(self,request):
        last_30=timezone.now()-timedelta(days=30); qs=Trip.objects.filter(driver=request.user,status='COMPLETED')
        return Response({'driver_id':request.user.id,'driver_name':request.user.username,'total_completed_trips':qs.count(),'total_earnings':qs.aggregate(total=Sum('final_fare'))['total'] or 0,'last_30_days_earnings':qs.filter(end_time__gte=last_30).aggregate(total=Sum('final_fare'))['total'] or 0,'pending_cash_collection':Payment.objects.filter(booking__trip__driver=request.user,payment_method='CASH',status__in=['PENDING','INITIATED']).aggregate(total=Sum('amount'))['total'] or 0})
