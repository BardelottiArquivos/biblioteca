# apps/usuarios/forms.py
from django import forms
from .models import Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = [
            'bio', 'data_nascimento', 'avatar', 'telefone',
            'logradouro', 'numero', 'complemento', 'bairro',
            'cidade', 'estado', 'cep', 'receber_notificacoes_email',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'data_nascimento': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica classe Bootstrap em todos os campos
        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'