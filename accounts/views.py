from rest_framework import views,response,status,viewsets,permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from project.constants import * 
from rest_framework_jwt.views import *
from django.contrib.auth import authenticate,login,get_user_model,logout
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from _curses import OK
from .models import *
from .serializers import *
User = get_user_model()


"""
user login
"""
class LoginView(ObtainJSONWebToken):
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        data={}

        # full_name = request.data.get('full_name', None)
        if not request.data.get("username",None):
            return Response({"error":"Plese enter email"},status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get("password",None):
            return Response({"error":"Plese enter password"},status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(**request.data)

        if not user:
            return response.Response({"message":"Invalid login credentials."},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = Token.objects.get(user = user)
        except:
            token = Token.objects.create(user = user)
        
        try:
            device = Device.objects.get(created_by = user)
        except Device.DoesNotExist:
            device = Device.objects.create(created_by = user,device_type = 1)
            
        device.device_type = request.data['device_type']
        device.device_name = request.data['device_name']
        device.device_token = request.data['device_token']
        device.save()

        data = UserSerializer(user,context = {"request":request}).data
        data.update({"token":token.key})

        return Response({"data":data,"token":token.key,"status":status.HTTP_200_OK,"msg":"Login Successful",'url' : self.request.path}, status=status.HTTP_200_OK)

"""
delete user
"""
class DeleteUser(views.APIView):
    
    def post(self,request,*args,**kwargs):
        user = User.objects.filter(id = request.user.id)
        if not user:
            return response.Response({"msg":"You are not valid user"},status = status.HTTP_400_BAD_REQUEST)
        user = user[0]
        user.delete()
        return response.Response({"msg":"Successfully delete your self"},status = status.HTTP_200_OK)
    
"""
User registration
""" 
class UserRegister(views.APIView):
    def post(self,request,*args,**kwargs):
        if not request.data.get("full_name",None):
            return response.Response({"message":"Please enter full name of user."},status=status.HTTP_400_BAD_REQUEST)
        
        if not request.data.get("username",None):

            return response.Response({"message":"Please enter username of user."},status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get("email",None):
            return response.Response({"message":"Please enter email of user."},status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get("password",None):
            return response.Response({"message":"Please enter password ."},status=status.HTTP_400_BAD_REQUEST)

        if len(request.data.get("password")) < 8:
            return response.Response({"message":"Please enter minimum 8 digit password."},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=request.data.get("email")):
            return response.Response({"message":"User allready exist with same email."},status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=request.data.get("username")):
            return response.Response({"message":"User already exist with same username."},status=status.HTTP_400_BAD_REQUEST)
        dt={
            "full_name":request.data.get("full_name"),
            "username":"_".join(request.data.get("username").lower().split(" ")),
            "email":request.data.get("email"),
            "gender":request.data.get("gender"),
            "dob":request.data.get("dob"),
            "password":make_password(request.data['password']),
        }
        

        try:
            user = User.objects.get(**dt)
        except User.DoesNotExist:
            user = User.objects.create(**dt)        
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        data = UserSerializer(user,context={"request":request}).data
        data.update({"token":token.key})

        return Response({"data":data,"token":token.key,"status":status.HTTP_200_OK,"msg":"Registration done Successful",'url' : self.request.path}, status=status.HTTP_200_OK)


"""
user logout
"""
class UserLogout(views.APIView): 
    permission_classes = (permissions.IsAuthenticated,) 
        
    def get(self, request):
    	logout(request)

    	return Response("response")

"""
user check api
"""
class UserCheckApi(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        try:
            token = Token.objects.get(user = user)
        except:
            token = Token.objects.create(user = user)
        msg="Check User Api"
        data=UserSerializer(user,context = {"request":request}).data
        data.update({"token":token.key})
            
        response = {
            "data":data,
            'msg': msg,
            "status": status.HTTP_200_OK,
            'url' : request.path
        }   
        
        return Response(response)


"""
change password view
"""
class ChangePasswordView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not request.data.get("new_password", None):
            return Response({"message": "Please set a password"}, status=status.HTTP_400_BAD_REQUEST)

        self.user = request.user
        self.user.set_password(request.data.get("new_password"))
        self.user.save()
        try:
            self.user.auth_token.delete()
        except Exception as e:
            print(e)
            pass
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

