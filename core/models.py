from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from enum import Enum
from .managers import OperatorManager

# Create your models here.
class Operator(AbstractUser):
    username = None
    cpf = models.CharField(max_length=14, unique=True)
    name = models.CharField(max_length=50)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['name']

    objects = OperatorManager()

    class Meta:
        verbose_name = 'operator'
        verbose_name_plural = 'operators'

class Consumer(models.Model):
    class Type(Enum):
        Graduate = 'Graduate'
        Post_Graduate = 'Post_Graduate'
        Teacher = 'Teacher'
        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    name = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14, unique=True)
    credit = models.IntegerField(default=0)
    has_studentship = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=20, choices=Type.choices())

    def get_studentship(self):
        if self.has_studentship:
            return "Sim"
        else:
            return "Não"

    def get_type(self):
        if self.type == Consumer.Type.Graduate.value:
            return "Graduando"
        elif self.type == Consumer.Type.Post_Graduate.value:
            return "Pós Graduando"
        else:
            return "Servidor/Professor"

    def get_meal_value(self, meal_kind):
        if self.type == Consumer.Type.Graduate.value:
            if meal_kind == "lunch":
                return 3
            else:
                return 1
        elif self.type == Consumer.Type.Post_Graduate.value:
            if meal_kind == "lunch":
                return 5
            else:
                return 3
        else:
            if meal_kind == "lunch":
                return 8
            else:
                return 5

class Gru(models.Model):
    code = models.CharField(max_length=20)
    value = models.IntegerField(default=0)
    consumer_cpf = models.CharField(max_length=14)
    operator = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def get_consumer_name(self):
        try:
            consumer = Consumer.objects.get(cpf=self.consumer_cpf)
            return consumer.name
        except Consumer.DoesNotExist:
            return "None"

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
    consumer_cpf = models.CharField(max_length=14)
    operator = models.CharField(max_length=50)

    def get_type(self):
        if self.type == Transaction.Type.Input.value:
            return "Entrada"
        else:
            return "Saida"
