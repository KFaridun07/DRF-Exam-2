from django.db import models
from accounts.models import User 

# Create your models here.

class Channel(models.Model):
    TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE,related_name='channels')
    title = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(max_length=10,choices=TYPE_CHOICES,default='public')
    link = models.CharField(max_length=100, unique=True, blank=True)
    cr_at = models.DateTimeField(auto_now_add=True)


class ChannelFollow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='channel_follows')
    channel = models.ForeignKey(Channel,on_delete=models.CASCADE,related_name='followers')
    cr_at = models.DateTimeField(auto_now_add=True)


