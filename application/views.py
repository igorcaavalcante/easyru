from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

# Create your views here.
def index(request):
    template = loader.get_template('application/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def operators_login(request):
    if request.method == 'POST':
        cpf = request.POST['cpf']
        password = request.POST['password']
        user = authenticate(request, cpf=cpf, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('operators_login')
    else:
        return render(request, 'application/operators_login.html')

def operators_new(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            cpf = form.cleaned_data.get('cpf')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(cpf=cpf, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'application/operators_new.html', {'form': form})

def operators_logout(request):
    logout(request)
    return redirect('index')

def home(request):
    template = loader.get_template('application/home.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required(login_url='operators_login')
def consumers(request):
    template = loader.get_template('application/consumers.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required(login_url='operators_login')
def consumers_new(request):
    template = loader.get_template('application/consumers_new.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required(login_url='operators_login')
def grus_debit(request):
    template = loader.get_template('application/grus_debit.html')
    context = {}
    return HttpResponse(template.render(context, request))

@login_required(login_url='operators_login')
def grus_new(request):
    template = loader.get_template('application/grus_new.html')
    context = {}
    return HttpResponse(template.render(context, request))
