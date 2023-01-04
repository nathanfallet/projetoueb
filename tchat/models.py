from django.db import models
from django.utils import timezone
import datetime 

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    biography = models.TextField()
    avatar = models.TextField()
    join_date = models.DateTimeField('inscrit depuis le')
    last_active = models.DateTimeField()


class Channel(models.Model):
    name = models.CharField(max_length=50)
    logo = models.TextField()
    created = models.DateTimeField("channel crée le")

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.TextField()
    published = models.DateTimeField("message publié le")

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    last_read = models.DateTimeField()
