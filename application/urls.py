from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('login', views.home, name='login'),
    path('new_user', views.home, name='new_user'),
    path('students', views.home, name='students'),
    path('new_meal', views.home, name='new_meal'),
]
