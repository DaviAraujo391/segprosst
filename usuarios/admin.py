# usuarios/admin.py

from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'cpf')
    search_fields = ('user__username', 'cpf')






