from rest_framework import serializers
from .models import Consumer, Transaction, User, Gru

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_consumer']

class ConsumerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Consumer
        fields = ['credit', 'has_studentship', 'created_at', 'type', 'user', 'user_hash']

    def create(self, validated_data):
        user = User(
                    username=validated_data['username'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    is_consumer=validated_data['is_consumer']
                )
        user.set_password(validated_data['password'])
        user.save()
        consumer = Consumer(
                            user=user,
                            credit=validated_data['credit'],
                            has_studentship=validated_data['has_studentship'],
                            type=validated_data['type']
                        )
        consumer.save()

        return consumer

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['type', 'value', 'created_at', 'consumer_cpf', 'operator']

    def create(self, validated_data):
        transaction = Transaction(
            type = validated_data['type'],
            value = validated_data['value'],
            consumer_cpf = validated_data['consumer_cpf'],
            operator = validated_data['operator'],
            )
        transaction.save()
        return transaction

class GruSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gru
        fields = ['code', 'value', 'created_at', 'consumer_cpf', 'operator']

    def create(self, validated_data):
        gru = Gru(
            code=validated_data['code'],
            value=validated_data['value'],
            consumer_cpf=validated_data['consumer_cpf'],
            operator=validated_data['operator']
            )

        gru.save()

        return gru
