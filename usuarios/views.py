# usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from cursos.models import Curso, Matricula

def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')

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


@login_required(login_url='/usuarios/login/')
def painel(request):
    cursos = Curso.objects.all()

    lista = []
    for curso in cursos:
        matriculado = Matricula.objects.filter(aluno=request.user, curso=curso).exists()
        lista.append({
            'curso': curso,
            'matriculado': matriculado
        })

    return render(request, 'usuarios/painel.html', {
        'usuario': request.user,
        'cursos': lista
    })


@login_required
def matricular(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    Matricula.objects.get_or_create(aluno=request.user, curso=curso)
    messages.success(request, f'Você foi matriculado no curso: {curso.titulo}')
    return redirect('usuarios:painel')

@login_required(login_url='/usuarios/login/')
def menu_principal(request):
    return render(request, 'usuarios/menu_principal.html')

