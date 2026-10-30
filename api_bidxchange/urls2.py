from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('verificando_conta/', views.verificando_conta, name='verificando_conta'), # testado 
    path('criar_conta/', views.criarConta, name='criarConta'), # testado
    path('verificadoEmail/', views.verificadoEmail, name='verificadoEmail'), # testado
    path('mudandoSenha/', views.mudandoSenha, name='mudandoSenha') # testado
]
