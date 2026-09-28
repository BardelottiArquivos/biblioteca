# apps/reservas/models.py
from django.db import models
from django.contrib.auth.models import User
from apps.core.models import BaseModel
from apps.acervo.models import Livro


class Reserva(BaseModel):
    """Reserva de um livro popular (fila de espera)."""

    STATUS_CHOICES = [
        ('A', 'Aguardando'),
        ('C', 'Confirmada'),
        ('E', 'Expirada'),
        ('F', 'Finalizada'),
        ('X', 'Cancelada'),
    ]

    livro = models.ForeignKey(
        Livro, on_delete=models.CASCADE, related_name='reservas',
    )
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reservas',
    )
    data_reserva = models.DateTimeField('Data da Reserva', auto_now_add=True, db_index=True)
    status = models.CharField(
        'Status', max_length=1,
        choices=STATUS_CHOICES, default='A', db_index=True,
    )
    posicao_fila = models.IntegerField('Posição na Fila', default=0)
    notificado = models.BooleanField('Notificado', default=False)
    data_notificacao = models.DateTimeField('Data da Notificação', null=True, blank=True)
    data_expiracao = models.DateTimeField('Data de Expiração', null=True, blank=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['data_reserva']
        unique_together = [['livro', 'usuario']]
        indexes = [
            models.Index(fields=['status', 'posicao_fila']),
            models.Index(fields=['data_reserva']),
        ]

    def calcular_posicao(self):
        """Calcula a posição atual na fila."""
        # CORRIGIDO: status__in
        reservas_ativas = list(
            Reserva.objects.filter(
                livro=self.livro, status__in=['A', 'C'],
            ).order_by('data_reserva')
        )
        try:
            posicao = reservas_ativas.index(self) + 1
        except ValueError:
            posicao = len(reservas_ativas)

        self.posicao_fila = posicao
        self.save(update_fields=['posicao_fila'])
        return posicao

    def __str__(self):
        return f'{self.usuario.username} - {self.livro.titulo} (Posição: {self.posicao_fila})'