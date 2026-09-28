# apps/reservas/services.py
# ==============================================
# GERENCIADOR DE FILA DE RESERVAS
# ==============================================
import logging
from datetime import timedelta
from django.utils import timezone

from .models import Reserva

logger = logging.getLogger(__name__)


class GerenciadorFila:
    """Gerencia a fila de reservas de livros populares."""

    @staticmethod
    def processar_liberacao_livro(livro):
        """Processa a liberação de um livro, notificando o próximo da fila."""
        proxima_reserva = Reserva.objects.filter(
            livro=livro, status='A',
        ).order_by('data_reserva').first()

        if proxima_reserva:
            proxima_reserva.status = 'C'
            proxima_reserva.data_expiracao = timezone.now() + timedelta(days=3)
            proxima_reserva.save(update_fields=['status', 'data_expiracao'])

            # Atualiza status do livro para RESERVADO
            livro.status = 'RE'
            livro.save(update_fields=['status'])

            GerenciadorFila._atualizar_posicoes_fila(livro)
            GerenciadorFila._notificar_usuario(proxima_reserva)

            logger.info(f'Reserva confirmada: {proxima_reserva.usuario.username}')
            return proxima_reserva
        else:
            livro.status = 'DD'
            livro.save(update_fields=['status'])
            logger.info(f'Livro disponível novamente: {livro.titulo}')
            return None

    @staticmethod
    def _atualizar_posicoes_fila(livro):
        reservas = Reserva.objects.filter(livro=livro, status='A').order_by('data_reserva')
        for i, reserva in enumerate(reservas, 1):
            reserva.posicao_fila = i
            reserva.save(update_fields=['posicao_fila'])

    @staticmethod
    def _notificar_usuario(reserva):
        reserva.notificado = True
        reserva.data_notificacao = timezone.now()
        reserva.save(update_fields=['notificado', 'data_notificacao'])

        try:
            from apps.notificacoes.services import NotificacaoService
            NotificacaoService.enviar_notificacao(
                usuario=reserva.usuario,
                tipo='RESERVA_CONFIRMADA',
                titulo='📚 Sua reserva foi confirmada!',
                mensagem=(
                    f'O livro "{reserva.livro.titulo}" está disponível para você. '
                    f'Você tem até {reserva.data_expiracao.strftime("%d/%m/%Y %H:%M")} '
                    f'para confirmar o empréstimo.'
                ),
            )
        except Exception as e:
            logger.error(f'Erro ao notificar reserva: {e}')

    @staticmethod
    def expirar_reservas():
        """Expira reservas não confirmadas após o prazo."""
        data_limite = timezone.now()
        reservas_expiradas = Reserva.objects.filter(
            status='C', data_expiracao__lt=data_limite,
        )

        for reserva in reservas_expiradas:
            reserva.status = 'E'
            reserva.save(update_fields=['status'])

            try:
                from apps.notificacoes.services import NotificacaoService
                NotificacaoService.enviar_notificacao(
                    usuario=reserva.usuario,
                    tipo='RESERVA_EXPIRADA',
                    titulo='⏰ Sua reserva expirou',
                    mensagem=f'O livro "{reserva.livro.titulo}" não foi retirado a tempo.',
                )
            except Exception as e:
                logger.error(f'Erro ao notificar expiração: {e}')

            GerenciadorFila.processar_liberacao_livro(reserva.livro)
            logger.info(f'Reserva expirada: {reserva.usuario.username}')