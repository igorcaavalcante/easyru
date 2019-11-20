from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('login', views.home, name='login'),
    path('students', views.home, name='students'),
    path('new-meal', views.home, name='newMeal'),
]
