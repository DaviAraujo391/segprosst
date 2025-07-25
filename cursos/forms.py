from django import forms
from .models import Curso, Aula

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo', 'descricao', 'imagem', 'carga_horaria', 'publicado']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'imagem': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'carga_horaria': forms.NumberInput(attrs={'class': 'form-control'}),
            'publicado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AulaForm(forms.ModelForm):
    video_upload = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Aula
        fields = ['modulo', 'titulo', 'texto', 'arquivo', 'video_url', 'video_upload', 'ordem']
        widgets = {
            'modulo': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'arquivo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        video_url = cleaned_data.get("video_url")
        video_upload = self.files.get("video_upload")

        if not video_url and not video_upload:
            raise forms.ValidationError("Você deve fornecer um URL de vídeo ou fazer upload de um vídeo.")

        if video_url and video_upload:
            raise forms.ValidationError("Escolha apenas uma opção: URL ou upload de vídeo.")



