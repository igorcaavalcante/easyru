from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from core.forms import operatorsNewForm
from core.models import Consumer, Gru, Transaction
import json

def index(request):
    return render(request, 'application/index.html')

@login_required(login_url='operators_login')
def home(request):
    error = ""
    if request.method == 'POST':
        try:
            consumer = Consumer.objects.get(cpf=request.POST['cpf'])
            if consumer.credit >= value:
                transaction = Transaction(type=Transaction.Type.Output.value, value=value)
                consumer.credit -= value
                transaction.save()
                consumer.save()
                return redirect('home')
            else:
                error = "Pessoa não Possui Saldo!"
        except Consumer.DoesNotExist:
            error = "Pessoa Não Cadastrada!"
    return render(request, 'application/home.html', {'error':error})

@login_required(login_url='operators_login')
def search_cpf(request):
    data = ""
    if request.is_ajax():
        querry = request.GET.get('term', '')
        search_response = Consumer.objects.filter(cpf__startswith=querry)
        results = []
        for obj in search_response:
            results.append(obj.cpf)
        data = json.dumps(results)

    return HttpResponse(data)

### Authentication ###
def operators_login(request):
    error = ""
    if request.method == 'POST':
        user = authenticate(request, cpf=request.POST['cpf'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
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
            return redirect('home')
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
        try:
            consumer = Consumer(name=request.POST['name'], cpf=request.POST['cpf'], credit=0, has_studentship=False)
            consumer.save()
            return redirect('consumers')
        except Exception as e:
            error = "CPF Já Cadastrado!"

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
                transaction = Transaction(type=Transaction.Type.Input.value, value=gru.value, consumer_cpf=gru.consumer_cpf, operator=request.user.name)
                consumer.credit += int(gru.value)
                transaction.save()
                consumer.save()
                gru.save()
                return redirect('grus')
            except Consumer.DoesNotExist:
                error = "Pessoa Não Cadastrada!"

    return render(request, 'application/grus_new.html', { 'error':error })

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
