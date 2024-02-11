# back_end/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_ativos, name='lista_ativos'),
    path('adicionar/', views.adicionar_ativo, name='adicionar_ativo'),
]
