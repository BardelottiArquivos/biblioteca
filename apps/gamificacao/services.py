# apps/gamificacao/services.py
# ================================================
# SERVIÇO DE GAMIFICAÇÃO
# ================================================
import logging
from django.db import transaction

from .models import Acao, PontuacaoUsuario, HistoricoPontos

logger = logging.getLogger(__name__)


class GamificacaoService:
    """Serviço para gerenciar a gamificação."""

    @staticmethod
    @transaction.atomic
    def conceder_pontos(usuario, tipo, objeto=None, descricao=None):
        """Concede pontos a um usuário por uma ação específica."""
        try:
            acao = Acao.objects.get(tipo=tipo, ativo=True)
        except Acao.DoesNotExist:
            logger.error(f'Ação não encontrada ou inativa: {tipo}')
            return False

        try:
            pontuacao, _ = PontuacaoUsuario.objects.get_or_create(usuario=usuario)

            HistoricoPontos.objects.create(
                usuario=usuario,
                acao=acao,
                pontos=acao.pontos,
                descricao=descricao or acao.descricao,
                object_id=objeto.id if objeto else None,
                content_type=objeto.__class__.__name__ if objeto else '',
            )

            pontuacao.pontos_totais += acao.pontos
            pontuacao.save(update_fields=['pontos_totais'])
            pontuacao.calcular_nivel()

            logger.info(
                f'Pontos concedidos: {usuario.username} +{acao.pontos} pts ({tipo})'
            )
            return True

        except Exception as e:
            logger.error(f'Erro ao conceder pontos: {str(e)}')
            return False

    @staticmethod
    def get_ranking(limit=10):
        """Retorna o ranking dos usuários."""
        return PontuacaoUsuario.objects.filter(
            pontos_totais__gt=0
        ).select_related('usuario').order_by('-pontos_totais')[:limit]

    @staticmethod
    def get_posicao(usuario):
        """Retorna a posição do usuário no ranking."""
        try:
            pontuacao = PontuacaoUsuario.objects.get(usuario=usuario)
            usuarios_acima = PontuacaoUsuario.objects.filter(
                pontos_totais__gt=pontuacao.pontos_totais
            ).count()
            return usuarios_acima + 1
        except PontuacaoUsuario.DoesNotExist:
            return None

    @staticmethod
    def get_proxima_conquista(usuario):
        """Retorna a próxima conquista a ser desbloqueada."""
        try:
            pontuacao = PontuacaoUsuario.objects.get(usuario=usuario)
            niveis = [
                {'nivel': 2, 'pontos': 50, 'titulo': 'Leitor Iniciante'},
                {'nivel': 3, 'pontos': 200, 'titulo': 'Leitor Ávido'},
                {'nivel': 4, 'pontos': 500, 'titulo': 'Leitor Experiente'},
                {'nivel': 5, 'pontos': 1000, 'titulo': 'Mestre Bibliotecário'},
            ]
            for n in niveis:
                if pontuacao.pontos_totais < n['pontos']:
                    n['faltam'] = n['pontos'] - pontuacao.pontos_totais
                    return n
            return None
        except PontuacaoUsuario.DoesNotExist:
            return None