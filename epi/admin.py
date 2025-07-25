from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Funcionario, Equipamento, EntregaEPI, LogEntrega

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'cargo', 'setor')
    search_fields = ('nome', 'matricula')
    list_filter = ('setor', 'cargo')
    ordering = ('nome',)

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade_estoque', 'validade_meses')
    search_fields = ('nome',)
    list_filter = ('validade_meses',)
    ordering = ('nome',)

@admin.register(EntregaEPI)
class EntregaEPIAdmin(admin.ModelAdmin):
    list_display = ('link_funcionario', 'equipamento', 'quantidade', 'data_entrega', 'responsavel_entrega', 'assinatura_confirmada')
    list_filter = ('data_entrega', 'equipamento', 'assinatura_confirmada')
    search_fields = ('funcionario__nome', 'equipamento__nome')
    autocomplete_fields = ('funcionario', 'equipamento', 'responsavel_entrega')
    readonly_fields = ('data_entrega',)
    date_hierarchy = 'data_entrega'
    ordering = ('-data_entrega',)

    def link_funcionario(self, obj):
        url = reverse('epi:historico_funcionario', args=[obj.funcionario.id])
        return format_html('<a href="{}">{}</a>', url, obj.funcionario.nome)
    link_funcionario.short_description = "Funcionário"

@admin.register(LogEntrega)
class LogEntregaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'entrega', 'acao', 'data')
    list_filter = ('usuario', 'data')
    search_fields = ('acao',)
    ordering = ('-data',)









