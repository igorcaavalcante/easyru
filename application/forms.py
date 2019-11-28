from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Operator

class operatorsNewForm(UserCreationForm):
    password1 = forms.CharField(label='Senha', strip=False, widget=forms.PasswordInput,)
    password2 = forms.CharField(label='Confirmar Senha', strip=False, widget=forms.PasswordInput,)
    class Meta:
        model = Operator
        fields = ('cpf', 'name',)
        labels = {
            'cpf' : 'CPF',
            'name' : 'Nome',
        }
