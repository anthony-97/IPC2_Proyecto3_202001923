from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpRequest
import requests

url = 'http://localhost:5000/'

def inicio(request):
    return HttpResponse("<h3>Vistas</h3>")

def index(request):
    if request.method == 'POST':
        envio = {
            'name':request.POST['cuerpo'],
        }
        r = requests.post(url+'procesar',json=envio,verify=True)
    return render(request,'app/index.html')

def consulta_datos(request):
    if request.method == 'GET':
        r = requests.get(url+'ConsultaDatos',verify=True)
        print(r.text)
    return render(request,'app/index.html')

def resumen_iva(request):
    if request.method == 'GET':
        r = requests.get(url+'ResumenIva',verify=True)
        print(r.text)
    return render(request,'app/resumen_iva.html')
#Para las autorizaciones, cambiar el ResumenIva con ConsultaDatos

def rango_total(request):
    if request.method == 'GET':
            r = requests.get(url+'ResumenRango1',verify=True)
    return render(request,'app/rango_total.html')

def rango_sin_iva(request):
    if request.method == 'GET':
            r = requests.get(url+'ResumenRango2',verify=True)
    return render(request,'app/rango_sin_iva.html')

#para ejectuarlo: python manage.py runserver

# Create your views here.