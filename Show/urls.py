from django.urls import path
from .views import *
 
urlpatterns = [
    path('', Login.as_view(), name='Login'),
    path('Register/', Register.as_view(), name='Register'),
	path('index/', index, name='index'),
]