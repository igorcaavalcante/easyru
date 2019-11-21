from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('application/index.html')
    context = {}
    return HttpResponse(template.render(context, request))

def login(request):
    template = loader.get_template('application/login.html')
    context = {}
    return HttpResponse(template.render(context, request))

def new_user(request):
    template = loader.get_template('application/new_user.html')
    context = {}
    return HttpResponse(template.render(context, request))

def home(request):
    template = loader.get_template('application/home.html')
    context = {}
    return HttpResponse(template.render(context, request))

def student(request):
    template = loader.get_template('application/student.html')
    context = {}
    return HttpResponse(template.render(context, request))

def new_student(request):
    template = loader.get_template('application/new_student.html')
    context = {}
    return HttpResponse(template.render(context, request))

def meal(request):
    template = loader.get_template('application/meal.html')
    context = {}
    return HttpResponse(template.render(context, request))

def new_meal(request):
    template = loader.get_template('application/new_meal.html')
    context = {}
    return HttpResponse(template.render(context, request))
