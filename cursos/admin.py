# Arquivo: cursos/admin.py

from django.contrib import admin 
from .models import (
    Curso, Matricula, Modulo, Aula,
    Progresso, Questionario, Resposta, Certificado
)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'instrutor', 'carga_horaria', 'publicado', 'criado_em')
    search_fields = ('titulo', 'instrutor')
    list_filter = ('publicado',)

@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'curso', 'data_matricula')
    search_fields = ('aluno__username', 'curso__titulo')
    list_filter = ('data_matricula',)

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'ordem')
    list_filter = ('curso',)
    ordering = ('curso', 'ordem')

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'ordem')
    list_filter = ('modulo__curso',)
    ordering = ('modulo', 'ordem')

@admin.register(Progresso)
class ProgressoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'aula', 'concluido', 'atualizado_em')
    list_filter = ('concluido',)
    search_fields = ('aluno__username', 'aula__titulo')

@admin.register(Questionario)
class QuestionarioAdmin(admin.ModelAdmin):
    list_display = ('aula', 'pergunta')

@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'questionario', 'resposta', 'acertou', 'respondido_em')
    list_filter = ('acertou',)
    search_fields = ('aluno__username', 'resposta')

@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('curso', 'aluno', 'emitido_em', 'codigo_validacao')
    search_fields = ('aluno__username', 'curso__titulo', 'codigo_validacao')
    list_filter = ('emitido_em',)





