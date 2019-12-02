from django.urls import path
from . import views

urlpatterns = [
    path('consumer/new', views.consumer_new, name='consumer_new'),
    path('consumer/<str:consumer_cpf>', views.consumer_views, name='consumer_views'),
    path('transactions/<str:consumer_cpf>', views.transaction_views, name='transaction_views'),
]
