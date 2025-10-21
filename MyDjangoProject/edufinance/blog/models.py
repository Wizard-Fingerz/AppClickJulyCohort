from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null = True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    number_of_likes = models.PositiveIntegerField(default = 0)
    number_of_shares = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    media = models.FileField(upload_to='posts_media/', null=True, blank=True)
    is_active = models.BooleanField(default= True)
    is_deleted = models.BooleanField(default= False)

    
    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField()
    reply = models.ManyToManyField('Reply')


class Reply(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField()