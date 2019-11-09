from django.db import models
from enum import Enum

# Create your models here.
class Funcionario(models.Model):
    nome = models.CharField(max_length=50, help_text='Digite seu nome completo')
    cpf = models.CharField(max_length=11)

class Usuario(models.Model):
    nome = models.CharField(max_length=50, help_text='Digite seu nome completo')
    cpf = models.CharField(max_length=11)
    senha = models.CharField(max_length=50, help_text='Digite sua senha')

class Consumidor(models.Model):
    nome = models.CharField(max_length=50, help_text='Digite seu nome completo')
    cpf = models.CharField(max_length=11)
    credito = models.IntegerField()
    bolsista = models.BooleanField(default=True)

class Gru(models.Model):
    codigo = models.CharField(max_length=20)
    valor = models.IntegerField()
    nome_comprador = models.CharField(max_length=50)
    competencia = models.CharField(max_length=20)
    funcionario = models.CharField(max_length=20)

class Transacao(models.Model):
    class Tipo(Enum):
        Entrada = 'Entrada'
        Saida = 'Saida'
        @classmethod
        def choices(cls):
            return tuple((i.name, i.value) for i in cls)

    tipo = models.CharField(max_length=10, choices=Tipo.choices(), default=Tipo.Entrada)
    descricao = models.CharField(max_length=20)
    valor = models.IntegerField()
