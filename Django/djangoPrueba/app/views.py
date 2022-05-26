from multiprocessing import context
from django.shortcuts import render

# Create your views here.
def index(request):
    context= {"nombre": request.GET.get("nombre"), "apellido": request.GET.get("apellido")}
    return render (request, "index.html",context=context)

def gato(request):
    return render(request, "gato.html")