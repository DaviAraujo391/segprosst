from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def sobre(request):
    return render(request, 'sobre.html')

def contato(request):
    return render(request, 'contato.html')

def acesso_portal(request):
    if request.user.is_authenticated:
        return redirect('usuarios:painel')
    return redirect('/accounts/login/?next=/usuarios/painel/')

