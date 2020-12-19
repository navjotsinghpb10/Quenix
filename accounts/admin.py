from django.contrib import admin
from .models import *

"""
show User on admin panel
"""
class UserAdmin(admin.ModelAdmin):
	list_display = ['full_name','email']

admin.site.register(User, UserAdmin)

class DeviceAdmin(admin.ModelAdmin):
	pass

admin.site.register(Device, DeviceAdmin)
