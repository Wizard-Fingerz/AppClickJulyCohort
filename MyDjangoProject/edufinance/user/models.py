from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    ROLE_CHOICES = [
        ('Admin', 'ADMIN'),
        ('Teacher', 'TEACHER'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length = 200, choices = GENDER_CHOICES)
    role = models.CharField(max_length = 200, choices = ROLE_CHOICES)