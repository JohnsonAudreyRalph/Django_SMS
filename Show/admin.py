from django.contrib import admin
from .models import User_manager

# Register your models here.
@admin.register(User_manager)
class Admin_model(admin.ModelAdmin):
    list_display = ('id', 'Creat_day', 'user', 'password', 'phone_number')