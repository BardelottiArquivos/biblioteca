# apps/usuarios/models.py
# ===============================================
# PERFIL DO USUÁRIO (ESTENDE O USER DO DJANGO)
# ===============================================
from django.db import models
from django.contrib.auth.models import User

from apps.core.models import BaseModel, PhoneNumberMixin, AddressMixin


class Perfil(BaseModel, PhoneNumberMixin, AddressMixin):
    """Perfil estendido do usuário do Django."""

    TIPO_USUARIO = [
        ('LEITOR', 'Leitor'),
        ('DOADOR', 'Doador'),
        ('BIBLIOTECARIO', 'Bibliotecário'),
        ('ADMIN', 'Administrador'),
    ]

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil',
        verbose_name='Usuário',
    )
    tipo = models.CharField(
        'Tipo de Usuário',
        max_length=15,
        choices=TIPO_USUARIO,
        default='LEITOR',
        db_index=True,
    )
    bio = models.TextField('Biografia', blank=True, max_length=500)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    avatar = models.ImageField('Avatar', upload_to='avatars/%Y/%m/', blank=True, null=True)
    receber_notificacoes_email = models.BooleanField(
        'Receber notificações por email', default=True,
    )
    aceita_termos = models.BooleanField('Aceitou os Termos', default=False)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return f'Perfil de {self.usuario.username}'
