from django.db import models

class Documento(models.Model):
    CATEGORIAS = [
        ('CIPA', 'Comissão Interna de Prevenção de Acidente e Assédio'),
        ('OS', 'Ordem de Serviço'),
        ('PGR', 'Programa de Gerenciamento de Riscos'),
        ('PCMSO', 'Programa de Controle Médico de Saúde Ocupacional'),
        ('AVCB', 'Auto de Vistoria do Corpo de Bombeiros'),
        ('PAE', 'Plano de Atendimento a Emergência'),
        ('OUTRO', 'Outro'),
    ]

    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    arquivo = models.FileField(upload_to='documentos/', blank=True, null=True)  # Agora opcional
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo



