from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cursos.models import Matricula  # Importa os cursos matriculados

def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email    = request.POST.get('email')
        senha1   = request.POST.get('senha1')
        senha2   = request.POST.get('senha2')

        if senha1 != senha2:
            messages.error(request, 'As senhas não conferem.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email já está cadastrado.')
        else:
            user = User.objects.create_user(username=username, email=email, password=senha1)
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('usuarios:painel')

    return render(request, 'usuarios/cadastro.html')


@login_required
def painel(request):
    cursos = Matricula.objects.filter(aluno=request.user)
    return render(request, 'usuarios/painel.html', {
        'usuario': request.user,
        'cursos': cursos
    })


