from django.db import models
from django.contrib.auth.models import User

# Curso base
class Curso(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    instrutor = models.CharField(max_length=100)
    carga_horaria = models.PositiveIntegerField()
    imagem = models.ImageField(upload_to='cursos/imagens/', blank=True, null=True)
    publicado = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


# Matrícula do aluno
class Matricula(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    data_matricula = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['aluno', 'curso']

    def __str__(self):
        return f'{self.aluno.username} em {self.curso.titulo}'


# Organização de módulos
class Modulo(models.Model):
    curso = models.ForeignKey(Curso, related_name='modulos', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f'{self.ordem}. {self.titulo}'


# Aulas dentro dos módulos
class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, related_name='aulas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, null=True)
    texto = models.TextField(blank=True)
    arquivo = models.FileField(upload_to='cursos/materiais/', blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return self.titulo


# Progresso do aluno em cada aula
class Progresso(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    concluido = models.BooleanField(default=False)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.aluno.username} - {self.aula.titulo}"


# Questionário associado a uma aula
class Questionario(models.Model):
    aula = models.OneToOneField(Aula, on_delete=models.CASCADE)
    pergunta = models.TextField()
    resposta_correta = models.CharField(max_length=255)

    def __str__(self):
        return f'Pergunta - {self.aula.titulo}'


# Resposta do aluno ao questionário
class Resposta(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    resposta = models.CharField(max_length=255)
    acertou = models.BooleanField(default=False)
    respondido_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.aluno.username} - {self.questionario.aula.titulo}'


# Certificado de conclusão do curso
class Certificado(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    emitido_em = models.DateTimeField(auto_now_add=True)
    codigo_validacao = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return f'Certificado - {self.aluno.username} - {self.curso.titulo}'



