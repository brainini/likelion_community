from django.db import models
from django.db.models.fields import TextField
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    college = models.CharField(max_length=20, blank=True, null=True)    
    major = models.CharField(max_length=20, blank=True, null=True)
    batch = models.SmallIntegerField(blank = True, null = True)
    tel = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    tmi = models.TextField()
    github_id = models.CharField(max_length = 30)

    def __str__(self):
        return f'id={self.id}, user_id={self.user.id}, college={self.college}, batch={self.batch}'

    @receiver(post_save, sender=User)  
    def create_user_profile(sender, instance, created, **kwargs):        
        if created:          
            Profile.objects.create(user=instance)  
    
    @receiver(post_save, sender=User)  
    def save_user_profile(sender, instance, **kwargs):        
        instance.profile.save()