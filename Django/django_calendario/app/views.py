from django.shortcuts import render
from django.http import HttpResponse
import calendar
from datetime import date

# Create your views here.

def index(request):
    #return HttpResponse("Hola chavales!")
    context = {"nombre":request.GET.get("nombre"), \
    "apellido":request.GET.get("apellido")}
    return render(request,"index.html",context=context) # Jinja2

def gato(request):
    return render(request, 'gato.html')



def calendario(request):
    calendario = calendar.HTMLCalendar(firstweekday = 0)
    try:
        mes, anio = int(request.GET.get("mes")), int(request.GET.get("anio"))
    except:
        mes, anio = date.today().month, date.today().year
    
    context = {"calendario":calendario.formatmonth(anio, mes)}
    return render(request,"calendario.html",context=context)
