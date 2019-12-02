from django.urls import path
from . import views

urlpatterns = [
    path('consumer/', views.consumer, name='consumer'),
    path('consumer/<str:consumer_cpf>', views.consumer_views, name='consumer_views'),
    path('transactions/<str:consumer_cpf>', views.transaction_views, name='transaction_views'),
    path('transactions/id/<int:id>', views.transaction, name='transaction'),
]
