from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Complaint
from .serializers import *
from apps.users.permissions import IsAdminUserRole
class MyComplaintListCreateView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request): return Response(ComplaintDetailSerializer(Complaint.objects.filter(user=request.user).order_by('-created_at'),many=True).data)
    def post(self,request):
        s=ComplaintCreateSerializer(data=request.data,context={'request':request})
        if s.is_valid(): c=s.save(); return Response({'message':'Complaint submitted successfully.','complaint':ComplaintDetailSerializer(c).data},status=201)
        return Response(s.errors,status=400)
class MyComplaintDetailView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,complaint_id):
        try:c=Complaint.objects.get(id=complaint_id,user=request.user)
        except Complaint.DoesNotExist:return Response({'detail':'Complaint not found.'},status=404)
        return Response(ComplaintDetailSerializer(c).data)
class AdminComplaintListView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request):
        qs=Complaint.objects.all().order_by('-created_at'); sf=request.query_params.get('status')
        if sf: qs=qs.filter(status=sf.upper())
        return Response(ComplaintDetailSerializer(qs,many=True).data)
class AdminComplaintDetailView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def get(self,request,complaint_id):
        try:c=Complaint.objects.get(id=complaint_id)
        except Complaint.DoesNotExist:return Response({'detail':'Complaint not found.'},status=404)
        return Response(ComplaintDetailSerializer(c).data)
class AdminComplaintReplyView(APIView):
    permission_classes=[IsAuthenticated, IsAdminUserRole]
    def patch(self,request,complaint_id):
        try:c=Complaint.objects.get(id=complaint_id)
        except Complaint.DoesNotExist:return Response({'detail':'Complaint not found.'},status=404)
        s=ComplaintReplySerializer(data=request.data)
        if s.is_valid(): c.status=s.validated_data['status']; c.admin_reply=s.validated_data.get('admin_reply',c.admin_reply); c.save(); return Response({'message':'Complaint updated successfully.','complaint':ComplaintDetailSerializer(c).data})
        return Response(s.errors,status=400)
