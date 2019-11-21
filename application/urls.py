from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('new_user', views.new_user, name='new_user'),
    path('students', views.students, name='students'),
    path('new_meal', views.new_meal, name='new_meal'),
]
