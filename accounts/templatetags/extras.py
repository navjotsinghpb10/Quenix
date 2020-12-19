from django import template
from django.db.models import Q,Count
from django.contrib.auth import get_user_model
from accounts.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
import datetime

User = get_user_model()

register = template.Library()


@register.filter(name='total_user')
def total_user(key):
    return User.objects.all().count()


@register.filter(name='total_active_user')
def total_active_user(key):
    return User.objects.filter(is_active=True).count()

@register.filter(name='total_inactive_user')
def total_inactive_user(key):
    return User.objects.filter(is_active=False).count()





