from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from core.models import Consumer, Gru, Transaction

def index(request):
    return render(request, 'application/index.html')



### Authentication ###
def operators_login(request):
    error = ""
    if request.method == 'POST':
        user = authenticate(request, cpf=request.POST['cpf'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error = "Usuario ou Senha Incorretos!"
    return render(request, 'application/operators_login.html', {'error':error})

def operators_new(request):
    if request.method == 'POST':
        form = operatorsNewForm(request.POST or None)
        if form.is_valid():
            form.save()
            cpf = form.cleaned_data.get('cpf')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(cpf=cpf, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = operatorsNewForm()
    return render(request, 'application/operators_new.html', {'form':form})

def operators_logout(request):
    logout(request)
    return redirect('index')

### Consumers ###
@login_required(login_url='operators_login')
def consumers(request):
    consumers = Consumer.objects.all()
    data = {}
    data['object_list'] = consumers
    return render(request, 'application/consumers.html', data)

@login_required(login_url='operators_login')
def consumers_new(request):
    error = ""
    if request.method == 'POST':
        consumer = Consumer(name=request.POST['name'], cpf=request.POST['cpf'], credit=0, has_studentship=False)
        if consumer:
            consumer.save()
            return redirect('consumers')
    return render(request, 'application/consumers_new.html', { 'error':error })

@login_required(login_url='operators_login')
def consumers_delete(request, pk):
    error = ""
    try:
        consumer = Consumer.objects.get(pk=pk)
        consumer.delete()
        return redirect('consumers')
    except Consumer.DoesNotExist:
        error = "Pessoa Não Cadastrada!"
        return render(request, 'application/consumers.html', { 'error':error })

### Grus ###
@login_required(login_url='operators_login')
def grus(request):
    grus = Gru.objects.all()
    data = {}
    data['object_list'] = grus
    return render(request, 'application/grus.html', data)

@login_required(login_url='operators_login')
def grus_new(request):
    error = ""
    if request.method == 'POST':
        gru = Gru(code=request.POST['code'],value=request.POST['value'], consumer_cpf=request.POST['consumer_cpf'], operator=request.user.name)
        if gru:
            try:
                consumer = Consumer.objects.get(cpf=gru.consumer_cpf)
                transaction = Transaction(type=Transaction.Type.Input.value, value=gru.value)
                consumer.credit += int(gru.value)
                transaction.save()
                consumer.save()
                gru.save()
                return redirect('grus')
            except Consumer.DoesNotExist:
                error = "Pessoa Não Cadastrada!"

    return render(request, 'application/grus_new.html', { 'error':error })

@login_required(login_url='operators_login')
def grus_debit(request):
    error = ""
    if request.method == 'POST':
        value = int(request.POST['quantity']) * int(request.POST['value'])
        try:
            consumer = Consumer.objects.get(cpf=request.POST['cpf'])
            if consumer.credit >= value:
                transaction = Transaction(type=Transaction.Type.Output.value, value=value)
                consumer.credit -= value
                transaction.save()
                consumer.save()
                return redirect('index')
            else:
                error = "Pessoa não Possui Saldo!"
        except Consumer.DoesNotExist:
            error = "Pessoa Não Cadastrada!"

    return render(request, 'application/grus_debit.html', {'error':error})

@login_required(login_url='operators_login')
def grus_delete(request, pk):
    error = ""
    try:
        gru = Gru.objects.get(pk=pk)
        gru.delete()
        return redirect('grus')
    except Gru.DoesNotExist:
        error = "Gru não Existe!"
        return render(request, 'application/grus.html', { 'error':error })

### Transactions ###
@login_required(login_url='operators_login')
def transactions(request):
    transaction = Transaction.objects.all()
    data = {}
    data['object_list'] = transaction
    return render(request, 'application/transactions.html', data)
