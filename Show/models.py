from django.db import models

# Create your models here.
class User_manager(models.Model):
    Creat_day = models.DateField(auto_now_add=True)
    user = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=8, blank=True)