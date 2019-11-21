from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('application/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))

def home(request):
    return HttpResponse("<h1>Falta colocar os templates</h1>")

def login(request):
    return HttpResponse("<h1>Falta colocar os templates</h1>")

<<<<<<< HEAD
def new_user(request):
    return HttpResponse("<h1>Falta colocar os templates</h1>")

def students(request):
    return HttpResponse("<h1>Falta colocar os templates</h1>")

def new_meal(request):
=======
def students(request):
    return HttpResponse("<h1>Falta colocar os templates</h1>")

def newMeal(request):
>>>>>>> 1d808b6176d63a79c45012b53999506013a73a23
    return HttpResponse("<h1>Falta colocar os templates</h1>")
