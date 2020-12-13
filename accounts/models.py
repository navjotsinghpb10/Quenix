from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser, BaseUserManager
from django.contrib.auth import update_session_auth_hash
from project.constants import *
from django.contrib.auth import password_validation,logout
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
alphanumeric = RegexValidator(r'^[a-zA-Z ]*$', 'Only characters are allowed.')
_alphanumeric = RegexValidator(r'^[a-zA-Z0-9!@#$&()\\-`.+,/\"]*$', 'Only contains alphanumeric and special characters.')


USER_STATE=((1,"Active"),(2,"Block"))

USER_GENDER=(("Male","Male"),("Female","Female") , ("Prefer not to say","Prefer not to say"))

"""
user model
"""
class User(AbstractUser):
    username = models.CharField(max_length=150,unique=True,validators=[_alphanumeric])
    full_name = models.CharField(max_length=150,validators=[alphanumeric],null=True,blank=True)
    first_name = models.CharField(max_length=150,validators=[alphanumeric],null=True,blank=True)
    last_name = models.CharField(max_length=150,validators=[alphanumeric],null=True,blank=True)
    email = models.EmailField("email address",unique=True)
    description = models.CharField(max_length=256, blank=True,null=True)
    avatar = models.FileField(upload_to="profile_pic",null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    mobile_no = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20,null=True,blank=True, choices=USER_GENDER)    
    state = models.PositiveIntegerField(default=1,choices=USER_STATE)

    class Meta:
        managed = True
        db_table = 'tbl_user'

    def clean(self):
        if not self.username:
            raise ValidationError('Please enter username.')
        if self.email and self.state == 2:
            if User.objects.filter(email=self.email,is_superuser=True):
                raise ValidationError('Your are a admin user. you can not change your state into block state.')
        if len(self.password) < 8:
            raise ValidationError('Please type minimum 8 digit password.')
        
    def save(self,*args,**kwargs):
        if self.state == 1:
            self.is_active= True
        else:
            self.is_active= False
            
        return super().save(*args,**kwargs)

DEVICE_TYPE = [
    (ANDROID,'Android'),
    (IOS,'ios'),
        ] 

"""
device type model
"""
class Device(models.Model):
       
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='device')
    device_type = models.PositiveIntegerField(choices=DEVICE_TYPE,null=True,blank=True)
    device_name = models.CharField(max_length=50,null=True,blank=True)
    device_token = models.CharField(max_length=500,null=True,blank=True)
    
    class Meta:
        managed = True
        db_table = 'tbl_device'