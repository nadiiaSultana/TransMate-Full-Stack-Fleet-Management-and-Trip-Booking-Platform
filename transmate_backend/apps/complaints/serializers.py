from rest_framework import serializers
from .models import Complaint
class ComplaintCreateSerializer(serializers.ModelSerializer):
    class Meta: model=Complaint; fields=['id','booking','subject','message','status','admin_reply','created_at','updated_at']; read_only_fields=['id','status','admin_reply','created_at','updated_at']
    def create(self,d): return Complaint.objects.create(user=self.context['request'].user,status='OPEN',**d)
class ComplaintDetailSerializer(serializers.ModelSerializer):
    user_name=serializers.CharField(source='user.username',read_only=True); user_role=serializers.CharField(source='user.role',read_only=True)
    class Meta: model=Complaint; fields=['id','user','user_name','user_role','booking','subject','message','status','admin_reply','created_at','updated_at']
class ComplaintReplySerializer(serializers.Serializer):
    status=serializers.ChoiceField(choices=['OPEN','IN_REVIEW','RESOLVED','REJECTED']); admin_reply=serializers.CharField(required=False,allow_blank=True)
