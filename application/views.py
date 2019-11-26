from django.shortcuts import render, redirect, get_object_or_404
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
    return render(request, 'application/operators_login.html', {'error' : error})

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
    return render(request, 'application/operators_new.html', {'form': form})

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
    form = consumerNewForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('consumers')
    return render(request, 'application/consumers_new.html', { 'form':form })

@login_required(login_url='operators_login')
def consumers_delete(request, pk):
    consumer = get_object_or_404(Consumer, pk=pk)
    if consumer:
        consumer.delete()
        return redirect('consumers')
    return render(request, 'application/consumers.html', { 'object':consumer })

### Grus ###
@login_required(login_url='operators_login')
def grus(request):
    grus = Gru.objects.all()
    data = {}
    data['object_list'] = grus
    return render(request, 'application/grus.html', data)

@login_required(login_url='operators_login')
def grus_new(request):
    form = gruNewForm(request.POST or None)
    form.fields['operator'].initial = request.user.name

    if form.is_valid():
        consumer = get_object_or_404(Consumer, cpf=form.data['consumer_cpf'])
        transaction = Transaction(type=Transaction.Type.Input.value, value=form.data['value'])
        if consumer:
            consumer.credit += int(form.data['value'])
            transaction.save()
            consumer.save()
            form.save()
            return redirect('grus')
    return render(request, 'application/grus_new.html', { 'form':form })

@login_required(login_url='operators_login')
def grus_debit(request):
    error = ""
    if request.method == 'POST':
        value = int(request.POST['quantity']) * int(request.POST['value'])
        try:
            consumer = Consumer.objects.get(cpf=request.POST['cpf'])
            if consumer.credit >= value:
                transaction = Transaction(type=Transaction.Type.Output.value, value= value)
                consumer.credit -= value
                transaction.save()
                consumer.save()
                return redirect('index')
            else:
                error = "Consumidor não Possui Saldo!"
        except Consumer.DoesNotExist:
            error = "Consumidor não Existe!"

    return render(request, 'application/grus_debit.html', {'error':error})

@login_required(login_url='operators_login')
def grus_delete(request, pk):
    gru = get_object_or_404(Gru, pk=pk)
    if gru:
        gru.delete()
        return redirect('grus')
    return render(request, 'application/grus.html', { 'object':gru })
