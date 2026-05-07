from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Rating
from .serializers import *
from apps.users.permissions import IsCustomerUserRole, IsAdminUserRole
class CustomerRatingListCreateView(APIView):
    permission_classes=[IsAuthenticated, IsCustomerUserRole]
    def get(self,request): return Response(RatingDetailSerializer(Rating.objects.filter(customer=request.user).order_by('-created_at'),many=True).data)
    def post(self,request):
        s=RatingCreateSerializer(data=request.data,context={'request':request})
        if s.is_valid(): r=s.save(); return Response({'message':'Rating submitted successfully.','rating':RatingDetailSerializer(r).data},status=201)
        return Response(s.errors,status=400)
class DriverRatingListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,driver_id):
        qs=Rating.objects.filter(driver_id=driver_id).order_by('-created_at'); return Response({'average_rating':qs.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0,'ratings':RatingDetailSerializer(qs,many=True).data})
class AdminRatingListView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request): return Response(RatingDetailSerializer(Rating.objects.all().order_by('-created_at'),many=True).data)
