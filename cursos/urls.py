# cursos/urls.py

from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    # Lista todos os cursos
    path('', views.lista_cursos, name='lista'),

    # Detalhe do curso e matrícula
    path('<int:curso_id>/', views.detalhe_curso, name='detalhe'),
    path('<int:curso_id>/matricular/', views.matricular, name='matricular'),

    # Aulas
    path('modulo/<int:modulo_id>/aula/<int:aula_id>/', views.visualizar_aula, name='aula'),
    path('aula/<int:aula_id>/concluir/', views.concluir_aula, name='concluir_aula'),

    # Questionário da aula
    path('aula/<int:aula_id>/questionario/', views.questionario, name='questionario'),

    # Certificado do curso
    path('<int:curso_id>/certificado/', views.emitir_certificado, name='certificado'),

    # Administração de aulas e cursos (instrutor)
    path('modulo/<int:modulo_id>/aula/nova/', views.criar_aula, name='nova_aula'),
    path('<int:curso_id>/editar/', views.editar_curso, name='editar_curso'),
]


