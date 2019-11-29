from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Operator

class operatorsNewForm(UserCreationForm):
    class Meta:
        model = Operator
        fields = ('cpf', 'name',)
        labels = {
            'cpf' : 'CPF',
            'name' : 'Nome',
        }
