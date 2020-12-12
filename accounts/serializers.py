from rest_framework import serializers as Serializers
from rest_framework_jwt import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password, check_password
from .models import *


User = get_user_model()


"""
user serializer
"""
class UserSerializer(Serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','full_name','username','email','description','avatar','dob','mobile_no','gender','state',)
        read_only_fields=('username',)


        
"""
device serializer
"""
class DeviceSerializer(Serializers.ModelSerializer):
    
    class Meta:
       model = Device
       fields = "__all__"


"""
login serializer
"""
class LoginSerializer(serializers.JSONWebTokenSerializer):
    def validate_email(self,value):
        if not value or value == '':
            raise serializers.ValidationError("Please enter email.")
        return value
    
    def validate_password(self,value):
        if not value or value == '':
            raise serializers.ValidationError("Please enter password.")
        return value
    



