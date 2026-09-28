# apps/emprestimos/models.py
# ========================
# SOLICITAÇÃO DE EMPRÉSTIMO
# ========================
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from apps.core.models import BaseModel
from apps.acervo.models import Livro


class SolicitacaoEmprestimo(BaseModel):
    """Solicitação de empréstimo de um livro."""

    STATUS_CHOICES = [
        ('P', 'Pendente'),
        ('A', 'Aprovado'),
        ('R', 'Recusado'),
        ('D', 'Devolvido'),
        ('C', 'Cancelado'),
    ]

    solicitante = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='emprestimos', verbose_name='Solicitante',
    )
    livro = models.ForeignKey(
        Livro, on_delete=models.CASCADE,
        related_name='emprestimos', verbose_name='Livro',
    )
    status = models.CharField(
        'Status', max_length=1,
        choices=STATUS_CHOICES, default='P', db_index=True,
    )
    data_solicitacao = models.DateTimeField(
        'Data de Solicitação', auto_now_add=True, db_index=True,
    )
    data_aprovacao = models.DateTimeField('Data de Aprovação', null=True, blank=True)
    data_devolucao = models.DateTimeField('Data de Devolução', null=True, blank=True)
    observacoes = models.TextField('Observações', blank=True)

    class Meta:
        verbose_name = 'Solicitação de Empréstimo'
        verbose_name_plural = 'Solicitações de Empréstimo'
        ordering = ['-data_solicitacao']

    def clean(self):
        """Impede que o usuário solicite empréstimo do próprio livro."""
        super().clean()
        if self.livro_id and self.solicitante_id and self.livro.doador_id == self.solicitante_id:
            raise ValidationError('Você não pode solicitar empréstimo do seu próprio livro.')

    def __str__(self):
        return f'{self.solicitante.username} - {self.livro.titulo} ({self.get_status_display()})'