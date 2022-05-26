from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):
    #return HttpResponse("Hola chavales!")
    context = {"nombre":request.GET.get("nombre"), \
    "apellido":request.GET.get("apellido")}
    return render(request,"index.html",context=context) # Jinja2

def gato(request):
    return render(request, 'gato.html')