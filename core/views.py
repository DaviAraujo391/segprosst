# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'core/home.html')

def sobre(request):
    return render(request, 'core/sobre.html')

def contato(request):
    return render(request, 'core/contato.html')

@login_required(login_url='/usuarios/login/')
def acesso_portal(request):
    return redirect('usuarios:menu_principal')


