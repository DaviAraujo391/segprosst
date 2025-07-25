from django.db import models
from django.contrib.auth.models import User

class Funcionario(models.Model):
    nome = models.CharField(max_length=255)
    matricula = models.CharField(max_length=50, unique=True)
    cargo = models.CharField(max_length=100)
    setor = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

    class Meta:
        ordering = ['nome']
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    validade_meses = models.PositiveIntegerField(default=12)
    quantidade_estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"

class EntregaEPI(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    data_entrega = models.DateField(auto_now_add=True)
    quantidade = models.PositiveIntegerField(default=1)
    responsavel_entrega = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    assinatura_confirmada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.equipamento} → {self.funcionario} em {self.data_entrega.strftime('%d/%m/%Y')}"

    class Meta:
        ordering = ['-data_entrega']
        verbose_name = "Entrega de EPI"
        verbose_name_plural = "Entregas de EPI"

class LogEntrega(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data = models.DateTimeField(auto_now_add=True)
    acao = models.TextField()
    entrega = models.ForeignKey(EntregaEPI, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.usuario} - {self.acao} em {self.data.strftime('%d/%m/%Y %H:%M')}"







