from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    number_of_likes = models.PositiveIntegerField(default = 0)
    number_of_shares = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField()