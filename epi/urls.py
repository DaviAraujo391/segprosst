from django.urls import path
from . import views

app_name = 'epi'

urlpatterns = [
    path('entrega/', views.registrar_entrega, name='registrar_entrega'),
    path('historico/', views.historico_entregas, name='historico'),
    path('exportar/excel/', views.exportar_entregas_excel, name='exportar_excel'),
    path('exportar/pdf/', views.exportar_entregas_pdf, name='exportar_pdf'),
    path('historico/funcionario/<int:funcionario_id>/', views.historico_funcionario, name='historico_funcionario'),
]


