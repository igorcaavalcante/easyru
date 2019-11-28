from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from enum import Enum
from application.managers import OperatorManager

# Create your models here.
class Operator(AbstractUser):
    username = None
    cpf = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=50)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = []

    objects = OperatorManager()

    class Meta:
        verbose_name = 'operator'
        verbose_name_plural = 'operators'

class Consumer(models.Model):
    name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11, unique=True)
    credit = models.IntegerField(default=0)
    has_studentship = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

class Gru(models.Model):
    code = models.CharField(max_length=20)
    value = models.IntegerField(default=0)
    consumer_cpf = models.CharField(max_length=11)
    operator = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def get_consumer_name():
        try:
            consumer = Consumer.objects.get(cpf=self.consumer_cpf)
            return consumer.name
        except Consumer.DoesNotExist:
            return None

class Transaction(models.Model):
    class Type(Enum):
        Input = 'Input'
        Output = 'Output'
        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    type = models.CharField(max_length=10, choices=Type.choices())
    value = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
