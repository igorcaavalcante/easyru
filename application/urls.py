from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('home/', views.home, name='home'),
    path('operators/login/', views.operators_login, name='operators_login'),
    path('operators/new/', views.operators_new, name='operators_new'),
    path('operators/logout/', views.operators_logout, name='operators_logout'),
    path('consumers/', views.consumers, name='consumers'),
    path('consumers/new/', views.consumers_new, name='consumers_new'),
    path('grus/debit/', views.grus_debit, name='grus_debit'),
    path('grus/new/', views.grus_new, name='grus_new'),
]
