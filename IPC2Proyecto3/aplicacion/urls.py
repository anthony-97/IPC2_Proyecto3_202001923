from django.urls import path
from django.urls.resolvers import URLPattern
from .views import inicio,login

urlpatterns = [
    path('',inicio),
    path('login',login)
]
