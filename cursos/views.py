# cursos/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

from .models import (
    Curso, Matricula, Modulo, Aula,
    Progresso, Questionario, Resposta, Certificado
)
from .forms import CursoForm, AulaForm
from usuarios.models import Perfil


def lista_cursos(request):
    cursos = Curso.objects.filter(publicado=True)
    return render(request, 'cursos/lista.html', {'cursos': cursos})


def detalhe_curso(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    modulos = curso.modulos.all()
    return render(request, 'cursos/detalhe.html', {'curso': curso, 'modulos': modulos})


@login_required
def matricular(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    matricula, created = Matricula.objects.get_or_create(aluno=request.user, curso=curso)
    
    if created:
        messages.success(request, 'Você foi matriculado com sucesso!')
    else:
        messages.info(request, 'Você já está matriculado neste curso.')
    
    return redirect('usuarios:painel')


@login_required
def visualizar_aula(request, modulo_id, aula_id):
    aula = get_object_or_404(Aula, pk=aula_id, modulo_id=modulo_id)
    curso = aula.modulo.curso

    if not Matricula.objects.filter(aluno=request.user, curso=curso).exists():
        messages.error(request, 'Você precisa estar matriculado neste curso para acessar esta aula.')
        return redirect('cursos:detalhe', curso_id=curso.id)

    progresso, _ = Progresso.objects.get_or_create(aluno=request.user, aula=aula)

    return render(request, 'cursos/aula.html', {'aula': aula, 'progresso': progresso})


@login_required
def concluir_aula(request, aula_id):
    aula = get_object_or_404(Aula, pk=aula_id)
    curso = aula.modulo.curso

    if not Matricula.objects.filter(aluno=request.user, curso=curso).exists():
        messages.error(request, 'Você precisa estar matriculado neste curso.')
        return redirect('cursos:detalhe', curso_id=curso.id)

    progresso, _ = Progresso.objects.get_or_create(aluno=request.user, aula=aula)
    progresso.concluido = True
    progresso.save()

    messages.success(request, f'Aula "{aula.titulo}" marcada como concluída.')
    return redirect('cursos:visualizar_aula', modulo_id=aula.modulo.id, aula_id=aula.id)


@login_required
def questionario(request, aula_id):
    aula = get_object_or_404(Aula, pk=aula_id)
    curso = aula.modulo.curso

    if not Matricula.objects.filter(aluno=request.user, curso=curso).exists():
        messages.error(request, 'Você precisa estar matriculado neste curso para acessar este questionário.')
        return redirect('cursos:detalhe', curso_id=curso.id)

    questionario = getattr(aula, 'questionario', None)

    if not questionario:
        messages.info(request, 'Esta aula não possui questionário.')
        return redirect('cursos:visualizar_aula', modulo_id=aula.modulo.id, aula_id=aula.id)

    if request.method == 'POST':
        resposta_texto = request.POST.get('resposta')
        acertou = resposta_texto.strip().lower() == questionario.resposta_correta.strip().lower()
        Resposta.objects.create(
            aluno=request.user,
            questionario=questionario,
            resposta=resposta_texto,
            acertou=acertou
        )
        if acertou:
            messages.success(request, 'Resposta correta!')
        else:
            messages.error(request, 'Resposta incorreta. Tente novamente.')

        return redirect('cursos:visualizar_aula', modulo_id=aula.modulo.id, aula_id=aula.id)

    return render(request, 'cursos/questionario.html', {'questionario': questionario})


@login_required
def emitir_certificado(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)

    if not Matricula.objects.filter(aluno=request.user, curso=curso).exists():
        messages.error(request, 'Você precisa estar matriculado neste curso.')
        return redirect('cursos:detalhe', curso_id=curso.id)

    aulas = Aula.objects.filter(modulo__curso=curso)
    aulas_concluidas = Progresso.objects.filter(
        aluno=request.user,
        aula__in=aulas,
        concluido=True
    ).count()

    if aulas_concluidas < aulas.count():
        messages.error(request, 'Você precisa concluir todas as aulas para obter o certificado.')
        return redirect('usuarios:painel')

    # Garante que o código de validação seja único
    codigo = get_random_string(16).upper()
    certificado, _ = Certificado.objects.get_or_create(
        curso=curso,
        aluno=request.user,
        defaults={'codigo_validacao': codigo}
    )

    perfil = get_object_or_404(Perfil, user=request.user)

    # Renderiza o HTML do certificado
    html_string = render_to_string('cursos/certificado_pdf.html', {
        'certificado': certificado,
        'aluno': request.user,
        'perfil': perfil,
        'curso': curso,
    })

    html = HTML(string=html_string)
    result = html.write_pdf()

    # Retorna o PDF como resposta
    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=certificado_{curso.id}_{request.user.id}.pdf'
    return response


@login_required
def criar_aula(request, modulo_id):
    modulo = get_object_or_404(Modulo, id=modulo_id)

    if request.method == 'POST':
        form = AulaForm(request.POST, request.FILES)
        if form.is_valid():
            aula = form.save(commit=False)
            aula.modulo = modulo

            if aula.video_upload:
                aula.video_url = None  # Prioriza o upload de vídeo

            aula.save()
            messages.success(request, 'Aula criada com sucesso!')
            return redirect('cursos:detalhe', curso_id=modulo.curso.id)
    else:
        form = AulaForm()

    return render(request, 'cursos/aula_form.html', {'form': form, 'modulo': modulo})


@login_required
def editar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso atualizado com sucesso!')
            return redirect('cursos:detalhe', curso_id=curso.id)
    else:
        form = CursoForm(instance=curso)

    return render(request, 'cursos/curso_form.html', {'form': form, 'curso': curso})



