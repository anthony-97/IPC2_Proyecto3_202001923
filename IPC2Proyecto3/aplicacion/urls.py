from os import confstr
from django.urls import path
from django.urls.resolvers import URLPattern
from .views import consulta_datos, inicio,index,resumen_iva, rango_total, rango_sin_iva, agregar_fechas, rango_fechas, ayuda

urlpatterns = [
    path('',inicio),
    path('index', index, name='index'),
    path('index', consulta_datos, name='index'),
    path('agregar_fechas', agregar_fechas, name='agregar_fechas'),
    path('rango_fechas', rango_fechas, name='rango_fechas'),
    path('resumen_iva', resumen_iva, name='resumen_iva'),
    path('rango_total', rango_total, name='rango_total'),
    path('rango_sin_iva', rango_sin_iva, name='rango_sin_iva'),
    path('ayuda', ayuda, name='ayuda'),
]