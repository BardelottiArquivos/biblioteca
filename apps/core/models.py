# apps/core/models.py
# ===========================================
# MODELOS BASE REUTILIZÁVEIS
# Todos os modelos do sistema herdam destas classes abstratas.
# ===========================================
import re
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """
    Modelo base abstrato com campos comuns.
    Todos os modelos do sistema herdam desta classe.
    """
    criado_em = models.DateTimeField(_('Criado em'), auto_now_add=True, db_index=True)
    atualizado_em = models.DateTimeField(_('Atualizado em'), auto_now=True, db_index=True)
    ativo = models.BooleanField(_('Ativo'), default=True, db_index=True)

    class Meta:
        abstract = True

    def clean(self):
        """Validação personalizada (pode ser sobrescrita)."""
        super().clean()

    def save(self, *args, **kwargs):
        """Salva com validação obrigatória."""
        self.full_clean()
        super().save(*args, **kwargs)


class PhoneNumberMixin(models.Model):
    """Mixin para telefone com validação."""
    telefone = models.CharField(
        _('Telefone'), max_length=15, blank=True,
        help_text='(DDD) 99999-9999'
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if self.telefone:
            # Remove tudo que não for dígito
            cleaned = re.sub(r'[^0-9]', '', self.telefone)
            if len(cleaned) not in [10, 11]:
                raise ValidationError({
                    'telefone': _('Número de telefone inválido. Deve ter 10 ou 11 dígitos.')
                })
            self.telefone = cleaned


class CEPMixin(models.Model):
    """Mixin para CEP com validação."""
    cep = models.CharField(
        _('CEP'), max_length=8, blank=True,
        help_text='Apenas números'
    )

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if self.cep:
            cleaned = re.sub(r'[^0-9]', '', self.cep)
            if len(cleaned) != 8:
                raise ValidationError({
                    'cep': _('CEP deve ter 8 dígitos.')
                })
            self.cep = cleaned


class AddressMixin(CEPMixin):
    """Mixin para endereço completo."""
    logradouro = models.CharField(_('Logradouro'), max_length=200, blank=True)
    numero = models.CharField(_('Número'), max_length=10, blank=True)
    complemento = models.CharField(_('Complemento'), max_length=100, blank=True)
    bairro = models.CharField(_('Bairro'), max_length=100, blank=True)
    cidade = models.CharField(_('Cidade'), max_length=100, blank=True)
    estado = models.CharField(
        _('Estado'),
        max_length=2,
        blank=True,
        choices=[
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
            ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
            ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
        ],
    )

    class Meta:
        abstract = True

    @property
    def endereco_completo(self):
        """Retorna endereço formatado para exibição."""
        partes = []
        if self.logradouro:
            partes.append(self.logradouro)
        if self.numero:
            partes.append(f', {self.numero}')
        if self.complemento:
            partes.append(f' - {self.complemento}')
        if self.bairro:
            partes.append(f', {self.bairro}')
        if self.cidade:
            partes.append(f' - {self.cidade}')
        if self.estado:
            partes.append(f'/{self.estado}')
        if self.cep:
            partes.append(f' - CEP: {self.cep}')
        return ''.join(partes)
