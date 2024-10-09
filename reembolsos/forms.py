from django import forms
from .models import Reembolso

class ReembolsoForm(forms.ModelForm):
    class Meta:
        model = Reembolso
        fields = ['nome', 'email', 'descricao_produto', 'categoria', 'valor_nf', 'data_pagamento', 'comprovante']
        widgets = {
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
        }

class ComprovanteForm(forms.Form):
    comprovante_reembolso = forms.FileField(label='Anexar Comprovante de Reembolso')