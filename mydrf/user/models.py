from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Student(User):
    address = models.CharField(max_length = 250, blank = True, null = True)
    date_of_birth  = models.DateField(blank = True, null = True)
    profile_image = models.ImageField(upload_to= 'profile', blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add=True)


