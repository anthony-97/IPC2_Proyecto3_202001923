from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpRequest
import requests

url = 'http://localhost:5000/'

def inicio(request):
    return HttpResponse("Esto es un ejemplo IPC2")

def login(request):
    if request.method == 'POST':
        envio = {
            'name':request.POST['nombreUsuario'],
            'password':request.POST['contrasena']
        }
        r = requests.post(url+'procesar',json=envio,verify=True)
        print(r.text)
    return render(request,'app/login.html')


#para ejectuarlo: python manage.py runserver

# Create your views here.
