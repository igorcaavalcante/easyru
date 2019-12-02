from rest_framework import serializers
from .models import Consumer, Transaction

class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ['name', 'cpf', 'credit', 'has_studentship', 'created_at', 'type']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['type', 'value', 'created_at', 'consumer_cpf', 'operator']
