from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer
class MyNotificationListView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        qs=Notification.objects.filter(user=request.user).order_by('-created_at')
        return Response({'unread_count':qs.filter(is_read=False).count(),'notifications':NotificationSerializer(qs,many=True).data})
class MarkNotificationReadView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request,notification_id):
        try:n=Notification.objects.get(id=notification_id,user=request.user)
        except Notification.DoesNotExist:return Response({'detail':'Notification not found.'},status=404)
        n.is_read=True; n.save(); return Response({'message':'Notification marked as read.','notification':NotificationSerializer(n).data})
class MarkAllNotificationsReadView(APIView):
    permission_classes=[IsAuthenticated]
    def patch(self,request): Notification.objects.filter(user=request.user,is_read=False).update(is_read=True); return Response({'message':'All notifications marked as read.'})
