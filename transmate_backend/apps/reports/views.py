from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.models import User
from apps.bookings.models import Booking
from apps.trips.models import Trip
from apps.payments.models import Payment
from apps.vehicles.models import Vehicle, VehicleType
from apps.ratings.models import Rating
from apps.complaints.models import Complaint
from apps.users.permissions import IsAdminUserRole
class AdminDashboardSummaryView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request):
        last_30=timezone.now()-timedelta(days=30)
        avg=Rating.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        return Response({'users':{'total_customers':User.objects.filter(role='CUSTOMER').count(),'total_drivers':User.objects.filter(role='DRIVER').count(),'approved_drivers':User.objects.filter(role='DRIVER',is_verified=True).count()},'vehicles':{'total_vehicle_types':VehicleType.objects.count(),'total_vehicles':Vehicle.objects.count(),'available_vehicles':Vehicle.objects.filter(status='AVAILABLE').count(),'busy_vehicles':Vehicle.objects.filter(status='BUSY').count()},'bookings':{'total_bookings':Booking.objects.count(),'pending_bookings':Booking.objects.filter(status='PENDING').count(),'completed_bookings':Booking.objects.filter(status='COMPLETED').count(),'cancelled_bookings':Booking.objects.filter(status='CANCELLED').count()},'trips':{'total_trips':Trip.objects.count(),'ongoing_trips':Trip.objects.filter(status='ONGOING').count(),'completed_trips':Trip.objects.filter(status='COMPLETED').count()},'payments':{'total_payments':Payment.objects.count(),'paid_payments':Payment.objects.filter(status='PAID').count(),'total_revenue':Payment.objects.filter(status='PAID').aggregate(total=Sum('amount'))['total'] or 0,'last_30_days_revenue':Payment.objects.filter(status='PAID',paid_at__gte=last_30).aggregate(total=Sum('amount'))['total'] or 0},'ratings':{'average_rating':round(avg,2)},'complaints':{'open_complaints':Complaint.objects.filter(status='OPEN').count(),'resolved_complaints':Complaint.objects.filter(status='RESOLVED').count()}})
class AdminBookingReportView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request): return Response({'booking_status_report':list(Booking.objects.values('status').annotate(count=Count('id')))})
class AdminPaymentReportView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request): return Response({'payment_report':list(Payment.objects.values('payment_method','status').annotate(count=Count('id'),total_amount=Sum('amount')))})
class AdminVehicleUsageReportView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request): return Response({'vehicle_usage_report':list(Vehicle.objects.values('id','registration_number','vehicle_type__name','status').annotate(total_trips=Count('trips')))})
