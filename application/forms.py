from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Operator, Consumer, Gru

class operatorsNewForm(UserCreationForm):
    password1 = forms.CharField(label='Senha', strip=False, widget=forms.PasswordInput,)
    password2 = forms.CharField(label='Confirme sua Senha', strip=False, widget=forms.PasswordInput,)
    class Meta:
        model = Operator
        fields = ('cpf', 'name',)
        labels = {
            'cpf' : 'CPF',
            'name' : 'Nome',
        }

class consumerNewForm(forms.ModelForm):
    class Meta:
        model = Consumer
        fields = ('name', 'cpf', 'has_studentship')
        labels = {
            'name' : 'Nome',
            'cpf' : 'CPF',
            'has_studentship' : 'Possui Bolsa Alimentação?',
        }

class gruNewForm(forms.ModelForm):
    class Meta:
        model = Gru
        fields = ('code', 'value', 'consumer_cpf', 'operator')
        labels = {
            'code' : 'Código de Barras',
            'value' : 'Valor',
            'consumer_cpf' : 'CPF do Consumidor',
        }
        widgets = {
            'operator': forms.HiddenInput()
        }
