# apps/chat/models.py
from django.db import models
from django.contrib.auth.models import User

from apps.core.models import BaseModel
from apps.acervo.models import Livro


class Conversa(BaseModel):
    """Conversa entre dois ou mais usuários."""

    participantes = models.ManyToManyField(User, related_name='conversas')
    livro = models.ForeignKey(
        Livro, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='conversas',
    )
    data_atualizacao = models.DateTimeField(
        'Última Atualização', auto_now=True, db_index=True,
    )

    class Meta:
        verbose_name = 'Conversa'
        verbose_name_plural = 'Conversas'
        ordering = ['-data_atualizacao']

    def __str__(self):
        nomes = ', '.join([u.username for u in self.participantes.all()])
        return f'Conversa: {nomes}'


class Mensagem(BaseModel):
    """Mensagem dentro de uma conversa."""

    conversa = models.ForeignKey(
        Conversa, on_delete=models.CASCADE, related_name='mensagens',
    )
    remetente = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mensagens_enviadas',
    )
    conteudo = models.TextField('Mensagem')
    data_envio = models.DateTimeField('Data de Envio', auto_now_add=True, db_index=True)
    lida = models.BooleanField('Lida', default=False)
    data_leitura = models.DateTimeField('Data de Leitura', null=True, blank=True)

    class Meta:
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        ordering = ['data_envio']

    def __str__(self):
        return f'{self.remetente.username}: {self.conteudo[:30]}...'