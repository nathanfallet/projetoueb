from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Channel(models.Model):
    name = models.CharField(max_length=50)
    logo = models.TextField()
    created = models.DateTimeField("channel crée le")

    def __str__(self):
        return 'Channel: ' + self.name

    def lastMessage(self):
        return self.message_set.order_by('-published').first()

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.TextField()
    published = models.DateTimeField("message publié le")

    def __str__(self):
        return 'Message from ' + self.user.username + ' in ' + self.channel.name + ': ' + self.content

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    last_read = models.DateTimeField()

    def __str__(self):
        return 'Membership: ' + str(self.user.username) + ' in ' + str(self.channel.name)
