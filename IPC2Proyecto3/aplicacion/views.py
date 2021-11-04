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
        r = requests.get(url+'procesar',verify=True)
        print(r.text)
    return render(request,'app/index.html')

def resumen_iva(request):
    if request.method == 'GET':
        r = requests.get(url+'resumen_iva',verify=True)
        print(r.text)
    return render(request,'app/resumen_iva.html')
#Para las autorizaciones, cambiar el ResumenIva con ConsultaDatos

def rango_total(request):
    if request.method == 'GET':
            r = requests.get(url+'rango_total',verify=True)
    return render(request,'app/rango_total.html')

def rango_sin_iva(request):
    if request.method == 'GET':
            r = requests.get(url+'rango_sin_iva',verify=True)
    return render(request,'app/rango_sin_iva.html')

def agregar_fechas(request):
    if request.method == 'GET':
        r = requests.get(url+'agregar_fechas',verify=True)
    return render(request,'app/agregar_fechas.html')

def rango_fechas(request):
    if request.method == 'GET':
        r = requests.get(url+'rango_fechas',verify=True)
    return render(request,'app/rango_fechas.html')

def ayuda(request):
    if request.method == 'GET':
        r = requests.get(url+'ayuda',verify=True)
    return render(request,'app/ayuda.html')

#para ejectuarlo: python manage.py runserver

# Create your views here.