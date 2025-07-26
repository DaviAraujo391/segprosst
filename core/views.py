from django.shortcuts import render

from django.contrib.auth.models import User
from django.http import HttpResponse

def cria_superuser(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'davi.araujo18@gmail.com', '@Dm190621')
        return HttpResponse("✅ Superusuário criado com sucesso!")
    else:
        return HttpResponse("⚠️ Superusuário já existe.")

def home(request):
    return render(request, 'home.html')

def sobre(request):
    return render(request, 'sobre.html')

def contato(request):
    return render(request, 'contato.html')

