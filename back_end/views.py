from django.shortcuts import render, redirect

from .models import Ativo
from .forms import AtivoForm

import environ

env = environ.Env()
environ.Env.read_env()

def lista_ativos(request):
    ativos = Ativo.objects.all()
    return render(request, 'front_end/lista_ativos.html', {'ativos': ativos})

def adicionar_ativo(request):
    if request.method == 'POST':
        form = AtivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_ativos')
    else:
        form = AtivoForm()
    return render(request, 'front_end/adicionar_ativo.html', {'form': form})






