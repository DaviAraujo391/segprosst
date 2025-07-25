import openpyxl
from io import BytesIO

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from .forms import EntregaEPIForm
from .models import EntregaEPI, Equipamento, LogEntrega, Funcionario

@login_required
def registrar_entrega(request):
    if request.method == 'POST':
        form = EntregaEPIForm(request.POST)
        if form.is_valid():
            entrega = form.save(commit=False)
            equipamento = entrega.equipamento
            if entrega.quantidade > equipamento.quantidade_estoque:
                messages.error(request, "Estoque insuficiente para essa entrega.")
            else:
                equipamento.quantidade_estoque -= entrega.quantidade
                equipamento.save()
                entrega.responsavel_entrega = request.user
                entrega.assinatura_confirmada = True
                entrega.save()

                # Registro de log
                LogEntrega.objects.create(
                    usuario=request.user,
                    entrega=entrega,
                    acao=f"Registrou entrega de {entrega.quantidade}x {entrega.equipamento} para {entrega.funcionario}"
                )

                messages.success(request, "Entrega registrada com sucesso!")
                return redirect('epi:historico')
    else:
        form = EntregaEPIForm()
    return render(request, 'epi/registrar_entrega.html', {'form': form})

@login_required
def historico_entregas(request):
    entregas = EntregaEPI.objects.select_related('funcionario', 'equipamento').order_by('-data_entrega')
    return render(request, 'epi/historico.html', {'entregas': entregas})

@login_required
def historico_funcionario(request, funcionario_id):
    entregas = EntregaEPI.objects.filter(funcionario_id=funcionario_id).order_by('-data_entrega')
    funcionario = Funcionario.objects.filter(id=funcionario_id).first()
    return render(request, 'epi/historico_funcionario.html', {
        'entregas': entregas,
        'funcionario': funcionario,
    })

@login_required
def exportar_entregas_excel(request):
    entregas = EntregaEPI.objects.select_related('funcionario', 'equipamento').all()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Entregas de EPI"

    headers = ["Funcionário", "Matrícula", "Equipamento", "Quantidade", "Data Entrega", "Responsável"]
    ws.append(headers)

    for e in entregas:
        ws.append([
            e.funcionario.nome,
            e.funcionario.matricula,
            e.equipamento.nome,
            e.quantidade,
            e.data_entrega.strftime('%d/%m/%Y'),
            e.responsavel_entrega.username if e.responsavel_entrega else "N/A"
        ])

    response = HttpResponse(content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename="entregas_epi.xlsx"'
    wb.save(response)
    return response

@login_required
def exportar_entregas_pdf(request):
    entregas = EntregaEPI.objects.select_related('funcionario', 'equipamento').all()
    template = get_template('epi/entregas_pdf.html')
    html = template.render({'entregas': entregas})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="entregas_epi.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response






