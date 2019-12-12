from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('user/me/', views.user_me, name='user_me'),
    path('transactions/', views.transaction, name='transaction'),
    path('transactions/<int:id>', views.transaction_views, name='transaction_views'),
    path('gru/', views.gru, name='gru'),
]
