from django.shortcuts import render, redirect, HttpResponse
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import Consumer, Gru, Transaction, User
from core.forms import UserNewForm
import json, re

def index(request):
    return render(request, 'application/index.html')

@login_required(login_url='operators_login')
def home(request):
    error = ""

    if request.method == 'POST':
        if is_cpf_valid(request.POST['cpf']):
            try:
                consumer = Consumer.objects.get(user__username=request.POST['cpf'])
                return redirect('home_meal', consumer.user.username)
            except Consumer.DoesNotExist:
                error = "Pessoa Não Cadastrada!"
        else:
            error = "CPF Inválido!"
    return render(request, 'application/home.html', {'error':error})

@login_required(login_url='operators_login')
def home_meal(request, consumer_cpf):
    error = ""
    if request.method == 'POST':
        try:
            consumer = Consumer.objects.get(user__username=consumer_cpf)
            if consumer.has_studentship:
                value = 0
            else:
                value = consumer.get_meal_value(request.POST['meal_kind']) * int(request.POST['quantity'])
            if consumer.credit >= value:
                transaction = Transaction(
                    type=Transaction.Type.Output.value,
                    value=value,
                    consumer_cpf=consumer.user.username,
                    operator=request.user.get_full_name())

                consumer.credit -= value
                transaction.save()
                consumer.save()
                return redirect('home')
            else:
                error = "Pessoa não Possui Saldo!"
        except Consumer.DoesNotExist:
            error = "Pessoa Não Cadastrada!"
    return render(request, 'application/home_meal.html', {'error':error})

@login_required(login_url='operators_login')
def search_cpf(request):
    data = ""
    if request.is_ajax():
        querry = request.GET.get('term', '')
        search_response = Consumer.objects.filter(user__username__startswith=querry)
        results = []
        for obj in search_response:
            results.append(obj.user.username)
        data = json.dumps(results)

    return HttpResponse(data)

### Authentication ###
def operators_login(request):
    error = ""
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None and not user.is_consumer:
            login(request, user)
            return redirect('home')
        else:
            error = "Usuario ou Senha Incorretos!"
    return render(request, 'application/operators_login.html', {'error':error})

def operators_new(request):
    error = ""
    if request.method == 'POST':
        form = UserNewForm(request.POST or None)
        if form.is_valid():
            if is_cpf_valid(form.cleaned_data.get('username')):
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
            else:
                error = "CPF Inválido!"
    else:
        form = UserNewForm()
    return render(request, 'application/operators_new.html', {'form':form, 'error':error})

def operators_logout(request):
    logout(request)
    return redirect('index')

### Consumers ###
@login_required(login_url='operators_login')
def consumers(request):
    consumers_raw = Consumer.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(consumers_raw, 10)
    try:
        consumers = paginator.page(page)
    except PageNotAnInteger:
        consumers = paginator.page(1)
    except EmptyPage:
        consumers = paginator.page(paginator.num_pages)

    return render(request, 'application/consumers.html', { 'consumers':consumers })

@login_required(login_url='operators_login')
def consumers_new(request):
    error = ""
    if request.method == 'POST':
        if is_cpf_valid(request.POST['username']):
            try:
                user = User(
                    username=request.POST['username'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    is_consumer=True
                )
                user.set_password(request.POST['password'])
                user.save()

                consumer = Consumer(
                    credit=0,
                    has_studentship=request.POST['has_studentship'],
                    type=request.POST['type'],
                    user=User.objects.get(username=request.POST['username'])
                )

                consumer.save()
                return redirect('consumers')
            except Exception as e:
                error = "CPF Já Cadastrado!"
        else:
            error = "CPF Invalido!"

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
    grus_raw = Gru.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(grus_raw, 10)
    try:
        grus = paginator.page(page)
    except PageNotAnInteger:
        grus = paginator.page(1)
    except EmptyPage:
        grus = paginator.page(paginator.num_pages)

    return render(request, 'application/grus.html', { 'grus':grus })

@login_required(login_url='operators_login')
def grus_new(request):
    error = ""
    if request.method == 'POST':
        gru = Gru(
            code=request.POST['code'],
            value=request.POST['value'],
            consumer_cpf=request.POST['consumer_cpf'],
            operator=request.user.get_full_name()
            )

        try:
            gru.save()
            return redirect('grus')
        except Consumer.DoesNotExist:
            error = "Pessoa Não Cadastrada!"
        except IntegrityError:
            error = "Essa Gru Já Foi Cadastrada!"

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
    order_by = request.GET.get('order_by', 'pk')
    transactions_raw = Transaction.objects.all().order_by(order_by)
    page = request.GET.get('page', 1)

    paginator = Paginator(transactions_raw, 10)
    try:
        transactions = paginator.page(page)
    except PageNotAnInteger:
        transactions = paginator.page(1)
    except EmptyPage:
        transactions = paginator.page(paginator.num_pages)

    return render(request, 'application/transactions.html', { 'transactions':transactions })

### Validate CPF ###
def is_cpf_valid(cpf):
    if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
        return False

    numbers = [int(digit) for digit in cpf if digit.isdigit()]
    count = 0
    zero = numbers[0]

    for i in numbers:
        if zero == numbers[i] and i != 0:
            count += 1

    if len(numbers) != 11 or count == 11:
        return False

    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[9] != expected_digit:
        return False

    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True
