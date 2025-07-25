from django.shortcuts import render, get_object_or_404, redirect
from .models import Documento
from django.contrib import messages
from django.core.mail import send_mail  # opcional

def lista_documentos(request):
    documentos = Documento.objects.all().order_by('titulo')
    return render(request, 'documentos/lista.html', {'documentos': documentos})

def solicitar_orcamento(request, documento_id):
    doc = get_object_or_404(Documento, id=documento_id)

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')

        # Exemplo: envio de e-mail (ativo se configurado no settings.py)
        # send_mail(
        #     subject=f'Solicitação de orçamento - {doc.titulo}',
        #     message=f'De: {nome} <{email}>\n\n{mensagem}',
        #     from_email='nao-responder@segprosst.com',
        #     recipient_list=['orcamentos@segprosst.com'],
        # )

        messages.success(request, 'Solicitação enviada com sucesso!')
        return redirect('documentos:lista')

    return render(request, 'documentos/solicitar.html', {'documento': doc})


