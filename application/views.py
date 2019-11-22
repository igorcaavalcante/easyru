from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('application/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def operators_login(request):
    template = loader.get_template('application/operators_login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def operators_new(request):
    template = loader.get_template('application/operators_new.html')
    context = {}
    return HttpResponse(template.render(context, request))

def home(request):
    template = loader.get_template('application/home.html')
    context = {}
    return HttpResponse(template.render(context, request))

def consumers(request):
    template = loader.get_template('application/consumers.html')
    context = {}
    return HttpResponse(template.render(context, request))

def consumers_new(request):
    template = loader.get_template('application/consumers_new.html')
    context = {}
    return HttpResponse(template.render(context, request))

def grus_debit(request):
    template = loader.get_template('application/grus_debit.html')
    context = {}
    return HttpResponse(template.render(context, request))

def grus_new(request):
    template = loader.get_template('application/grus_new.html')
    context = {}
    return HttpResponse(template.render(context, request))
