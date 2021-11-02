from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpRequest
import requests

url = 'http://localhost:5000/'

def inicio(request):
    return HttpResponse("<h3>Vistas</h3>")

def index(request):
    sali=""
    if request.method == 'POST':
        envio = {
            'name':request.POST['cuerpo'],
        }
        r = requests.post(url+'procesar',json=envio,verify=True)
        sali=r.text
    return render(request,'app/index.html')

    #return render(request,'app/index.html?salida='+sali)
    
#Intento pasarle un parametro que es lo que retorna el proceso para luego tomarlo en la url del index.html y llenar el cuadro de salida.
#para ejectuarlo: python manage.py runserver

# Create your views here.
