from django.db import models
from django.db.models.fields import TextField
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):   # 추가
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    college = models.CharField(max_length=20, blank=True, null=True)    
    major = models.CharField(max_length=20, blank=True, null=True)
    batch = models.SmallIntegerField(blank = True, null = True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    tmi = models.TextField()
    github_id = models.CharField(max_length = 30)
    
