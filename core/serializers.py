from rest_framework import serializers
from .models import Consumer, Transaction, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class ConsumerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Consumer
        fields = ['credit', 'has_studentship', 'created_at', 'type', 'user']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['type', 'value', 'created_at', 'consumer_cpf', 'operator']
