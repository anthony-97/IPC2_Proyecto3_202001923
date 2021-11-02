from django.urls import path
from django.urls.resolvers import URLPattern
from .views import inicio,index

urlpatterns = [
    path('',inicio),
    path('index',index)
]
