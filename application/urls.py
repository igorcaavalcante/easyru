from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('search/cpf/', views.search_cpf, name='search_cpf'),
    path('operators/login/', views.operators_login, name='operators_login'),
    path('operators/new/', views.operators_new, name='operators_new'),
    path('operators/logout/', views.operators_logout, name='operators_logout'),
    path('consumers/', views.consumers, name='consumers'),
    path('consumers/new/', views.consumers_new, name='consumers_new'),
    path('consumers/delete/<int:pk>', views.consumers_delete, name='consumers_delete'),
    path('grus/', views.grus, name='grus'),
    path('grus/new/', views.grus_new, name='grus_new'),
    path('grus/delete/<int:pk>', views.grus_delete, name='grus_delete'),
    path('transactions/', views.transactions, name='transactions'),
]
