from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import *
from apps.users.permissions import IsCustomerUserRole, IsAdminUserRole
class CustomerBookingListCreateView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def get(self,request): return Response(BookingListSerializer(Booking.objects.filter(customer=request.user).order_by('-booking_time'), many=True).data)
    def post(self,request):
        s=BookingCreateSerializer(data=request.data, context={'request':request})
        if s.is_valid(): b=s.save(); return Response({'message':'Booking created successfully.','booking':BookingDetailSerializer(b).data}, status=201)
        return Response(s.errors,status=400)
class CustomerBookingDetailView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def get(self,request,booking_id):
        try:b=Booking.objects.get(id=booking_id, customer=request.user)
        except Booking.DoesNotExist:return Response({'detail':'Booking not found.'}, status=404)
        return Response(BookingDetailSerializer(b).data)
class CustomerCancelBookingView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def patch(self,request,booking_id):
        try:b=Booking.objects.get(id=booking_id, customer=request.user)
        except Booking.DoesNotExist:return Response({'detail':'Booking not found.'}, status=404)
        if b.status in ['ONGOING','COMPLETED','CANCELLED']: return Response({'detail':f'Booking cannot be cancelled because it is already {b.status}.'}, status=400)
        s=BookingCancelSerializer(data=request.data)
        if s.is_valid(): b.status='CANCELLED'; b.cancellation_reason=s.validated_data.get('cancellation_reason',''); b.save(); return Response({'message':'Booking cancelled successfully.','booking':BookingDetailSerializer(b).data})
        return Response(s.errors,status=400)
class AdminBookingListView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request):
        qs=Booking.objects.all().order_by('-booking_time'); sf=request.query_params.get('status')
        if sf: qs=qs.filter(status=sf.upper())
        return Response(BookingListSerializer(qs,many=True).data)
class AdminBookingDetailView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request,booking_id):
        try:b=Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:return Response({'detail':'Booking not found.'}, status=404)
        return Response(BookingDetailSerializer(b).data)
class AdminAcceptBookingView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def patch(self,request,booking_id):
        try:b=Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:return Response({'detail':'Booking not found.'}, status=404)
        if b.status!='PENDING': return Response({'detail':'Only pending bookings can be accepted.'}, status=400)
        b.status='ACCEPTED'; b.save(); return Response({'message':'Booking accepted successfully.','booking':BookingDetailSerializer(b).data})
class AdminCancelBookingView(CustomerCancelBookingView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def patch(self,request,booking_id):
        try:b=Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:return Response({'detail':'Booking not found.'}, status=404)
        if b.status in ['COMPLETED','CANCELLED']: return Response({'detail':f'Booking cannot be cancelled because it is already {b.status}.'}, status=400)
        s=BookingCancelSerializer(data=request.data)
        if s.is_valid(): b.status='CANCELLED'; b.cancellation_reason=s.validated_data.get('cancellation_reason',''); b.save(); return Response({'message':'Booking cancelled successfully by admin.','booking':BookingDetailSerializer(b).data})
        return Response(s.errors,status=400)
class AdminUpdateBookingStatusView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def patch(self,request,booking_id):
        try:b=Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:return Response({'detail':'Booking not found.'}, status=404)
        s=BookingStatusUpdateSerializer(data=request.data)
        if s.is_valid():
            if b.status in ['COMPLETED','CANCELLED']: return Response({'detail':f'{b.status.title()} booking status cannot be changed.'}, status=400)
            b.status=s.validated_data['status']; b.save(); return Response({'message':'Booking status updated successfully.','booking':BookingDetailSerializer(b).data})
        return Response(s.errors,status=400)
