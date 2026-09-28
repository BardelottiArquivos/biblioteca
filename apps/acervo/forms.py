# apps/acervo/forms.py
import re
from django import forms
from django.core.exceptions import ValidationError

from .models import Livro, Avaliacao, GeneroLiterario
from apps.core.validators import ISBNValidator, SecurityValidator


class LivroForm(forms.ModelForm):
    """Formulário para cadastro/edição de livros."""

    class Meta:
        model = Livro
        fields = [
            'titulo', 'autor', 'isbn', 'resumo', 'editora',
            'ano_publicacao', 'paginas', 'genero', 'idioma',
            'status', 'tipo_midia', 'possui_braille',
            'possui_fonte_ampliada', 'possui_audio',
            'possui_formato_digital_acessivel',
            'arquivo_digital', 'arquivo_audio', 'capa',
            'logradouro', 'numero', 'complemento', 'bairro',
            'cidade', 'estado', 'cep',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Título do livro'
            }),
            'autor': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Nome do autor'
            }),
            'resumo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '978-85-1234-567-8'
            }),
            'ano_publicacao': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 1000
            }),
            'paginas': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 1
            }),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        # Aplica classe Bootstrap em campos que ainda não têm
        for field_name, field in self.fields.items():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'

    def clean_isbn(self):
        """Valida e formata ISBN."""
        isbn = self.cleaned_data.get('isbn', '').strip()
        if not isbn:
            return ''

        isbn_clean = re.sub(r'[^0-9Xx]', '', isbn.upper())

        # Valida formato
        ISBNValidator.validate_isbn(isbn_clean)

        # Verifica duplicidade
        qs = Livro.objects.filter(isbn=isbn_clean)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Este ISBN já está cadastrado.')

        return isbn_clean

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo', '').strip()
        if titulo:
            SecurityValidator.validate_xss_safe(titulo)
            return SecurityValidator.sanitize_html(titulo)
        return titulo

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.usuario and not instance.pk:
            instance.doador = self.usuario
        if commit:
            instance.save()
        return instance


class AvaliacaoForm(forms.ModelForm):
    """Formulário para avaliação de livros."""

    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        widgets = {
            'nota': forms.Select(attrs={'class': 'form-control'}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        self.livro = kwargs.pop('livro', None)
        super().__init__(*args, **kwargs)
        # Popula as opções de nota
        self.fields['nota'].choices = [(i, f'{i} ★') for i in range(1, 6)]

    def clean_comentario(self):
        comentario = self.cleaned_data.get('comentario', '').strip()
        if comentario:
            SecurityValidator.validate_xss_safe(comentario)
            return SecurityValidator.sanitize_html(comentario)
        return ''

    def clean(self):
        cleaned_data = super().clean()
        if self.usuario and self.livro and not self.instance.pk:
            if Avaliacao.objects.filter(usuario=self.usuario, livro=self.livro).exists():
                raise ValidationError('Você já avaliou este livro.')
        return cleaned_data


class BuscaAvancadaForm(forms.Form):
    """Formulário de busca avançada com filtros."""
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Buscar livros...'
        }),
    )
    genero = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos os gêneros')] + list(GeneroLiterario.choices),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    autor = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Autor'
        }),
    )