from django import forms
from .models import EntregaEPI

class EntregaEPIForm(forms.ModelForm):
    class Meta:
        model = EntregaEPI
        fields = ['funcionario', 'equipamento', 'quantidade']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        equipamento = self.cleaned_data.get('equipamento')
        
        if equipamento and quantidade:
            if quantidade > equipamento.quantidade_estoque:
                raise forms.ValidationError(
                    f"Quantidade ({quantidade}) excede o estoque disponível ({equipamento.quantidade_estoque})."
                )
        return quantidade


