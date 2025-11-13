from django.db import models

class Classroom(models.Model):
    name = models.CharField(max_length = 250, unique = True)
    created_at = models.DateTimeField(auto_now_add=True)
    