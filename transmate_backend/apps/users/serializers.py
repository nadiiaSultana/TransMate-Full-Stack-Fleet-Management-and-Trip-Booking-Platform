from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    class Meta:
        model = User; fields = ['id','username','email','phone','password','confirm_password','address']
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'): raise serializers.ValidationError({'password':'Passwords do not match.'})
        return attrs
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(role='CUSTOMER', is_verified=True, **validated_data)

class DriverRegisterSerializer(CustomerRegisterSerializer):
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(role='DRIVER', is_verified=False, **validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(); password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        user = authenticate(username=attrs.get('username'), password=attrs.get('password'))
        if not user: raise serializers.ValidationError({'detail':'Invalid username or password.'})
        if not user.is_active: raise serializers.ValidationError({'detail':'This account is inactive.'})
        attrs['user'] = user; return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','phone','role','profile_image','address','is_verified','is_active','created_at','updated_at']
        read_only_fields = ['id','role','is_verified','is_active','created_at','updated_at']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','phone','role','is_verified','is_active','created_at']
