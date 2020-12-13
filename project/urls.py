"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:

    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url    
from django.contrib.auth.views import PasswordResetConfirmView
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from accounts import views as accounts_views
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()

urlpatterns = [

    path('api/v1/login/', accounts_views.LoginView.as_view(),name='login'),
    path('api/v1/', include('rest_auth.urls')),
    path('api/v1/registration/', accounts_views.UserRegister.as_view(), name='user_register'),   

    path('api/v1/check-user/',accounts_views.UserCheckApi.as_view(),name='check_user'),
    path('api/v1/user/change-password/', accounts_views.ChangePasswordView.as_view(), name='changepasswordView'),
    path('api/v1/logout/',accounts_views.UserLogout.as_view(), name='user_logout'),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('', include(router.urls)),

    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 

