from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('consumer/', views.consumer, name='consumer'),
    path('consumer/home/', views.consumer_views, name='consumer_views'),
    path('transactions/', views.transaction, name='transaction'),
    path('transactions/<int:id>', views.transaction_views, name='transaction_views'),
]
