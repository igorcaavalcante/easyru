from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
from application.managers import OperatorManager

# Create your models here.
class Operator(AbstractUser):
    username = None
    cpf = models.CharField(max_length=11, unique=True, help_text='Digite seu CPF')
    name = models.CharField(max_length=50, help_text='Digite seu nome completo')

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = []

    objects = OperatorManager()

    class Meta:
        verbose_name = 'operator'
        verbose_name_plural = 'operators'

class Consumer(models.Model):
    name = models.CharField(max_length=50, help_text='Digite seu nome completo')
    cpf = models.CharField(max_length=11)
    credit = models.IntegerField()
    has_studentship = models.BooleanField(default=True)

class Gru(models.Model):
    code = models.CharField(max_length=20)
    value = models.IntegerField()
    consumer_name = models.CharField(max_length=50)
    competence = models.CharField(max_length=20)
    operator = models.CharField(max_length=20)

class Transaction(models.Model):
    class Type(Enum):
        Input = 'Input'
        Output = 'Output'
        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    type = models.CharField(max_length=10, choices=Type.choices())
    description = models.CharField(max_length=20)
    value = models.IntegerField()
