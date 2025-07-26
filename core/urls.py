from django.urls import path
from . import views
from django.urls import path
from .views import cria_superuser

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('cria-superuser/', cria_superuser, name='cria_superuser'),
]
