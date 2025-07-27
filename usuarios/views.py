# usuarios/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cursos.models import Curso, Matricula, Aula

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

    for curso in cursos:
        curso.matriculado = Matricula.objects.filter(aluno=request.user, curso=curso).exists()
        if curso.matriculado:
            # Busca a primeira aula do curso
            curso.proxima_aula = Aula.objects.filter(modulo__curso=curso).order_by('id').first()
        else:
            curso.proxima_aula = None

    return render(request, 'usuarios/painel.html', {
        'usuario': request.user,
        'cursos': cursos
    })


@login_required
def matricular(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    Matricula.objects.get_or_create(aluno=request.user, curso=curso)
    messages.success(request, f'Você foi matriculado no curso: {curso.titulo}')
    return redirect('usuarios:painel')


@login_required(login_url='/usuarios/login/')
def acessar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    # Verifica se o usuário está matriculado
    if not Matricula.objects.filter(aluno=request.user, curso=curso).exists():
        messages.error(request, 'Você não está matriculado neste curso.')
        return redirect('usuarios:painel')

    return render(request, 'usuarios/aula.html', {
        'curso': curso
    })


@login_required(login_url='/usuarios/login/')
def menu_principal(request):
    return render(request, 'usuarios/menu_principal.html')


