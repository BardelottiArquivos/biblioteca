# apps/gamificacao/signals.py
# ==============================================
# SIGNALS DE GAMIFICAÇÃO
# ⚠️ CORRIGIDO: imports faltando no documento original
# ==============================================
import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from apps.acervo.models import Livro
from apps.emprestimos.models import SolicitacaoEmprestimo

from .models import Acao, PontuacaoUsuario, HistoricoPontos
from .services import GamificacaoService

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def criar_pontuacao_usuario(sender, instance, created, **kwargs):
    """Ao criar um usuário, concede pontos de cadastro."""
    if not created:
        return

    try:
        pontuacao, _ = PontuacaoUsuario.objects.get_or_create(usuario=instance)

        acao = Acao.objects.filter(tipo='CADASTRO', ativo=True).first()
        if not acao:
            # Se a Ação CADASTRO não existe, não faz nada (evita erro)
            logger.warning('Ação CADASTRO não cadastrada. Rode run_populate.py')
            return

        HistoricoPontos.objects.create(
            usuario=instance, acao=acao, pontos=acao.pontos,
            descricao='Cadastro na plataforma',
        )
        pontuacao.pontos_totais = acao.pontos
        pontuacao.save(update_fields=['pontos_totais'])
        pontuacao.calcular_nivel()
        logger.info(f'Pontuação criada para {instance.username}')

    except Exception as e:
        logger.error(f'Erro ao criar pontuação: {str(e)}')


@receiver(post_save, sender=Livro)
def pontos_doacao_livro(sender, instance, created, **kwargs):
    """Ao cadastrar um livro, concede pontos de doação."""
    if not created or not instance.doador_id:
        return

    try:
        GamificacaoService.conceder_pontos(
            usuario=instance.doador,
            tipo='DOACAO',
            objeto=instance,
            descricao=f'Doação do livro: {instance.titulo}',
        )
    except Exception as e:
        logger.error(f'Erro ao conceder pontos de doação: {str(e)}')


@receiver(post_save, sender=SolicitacaoEmprestimo)
def pontos_emprestimo(sender, instance, created, **kwargs):
    """Ao aprovar um empréstimo, concede pontos."""
    # Só concede se o status é 'A' (Aprovado) e ainda não tem data_aprovacao
    if instance.status != 'A' or instance.data_aprovacao:
        return

    try:
        # Atualiza a data sem disparar o signal novamente
        SolicitacaoEmprestimo.objects.filter(pk=instance.pk).update(
            data_aprovacao=timezone.now()
        )

        GamificacaoService.conceder_pontos(
            usuario=instance.solicitante,
            tipo='EMPRESTIMO',
            objeto=instance,
            descricao=f'Empréstimo do livro: {instance.livro.titulo}',
        )
    except Exception as e:
        logger.error(f'Erro ao conceder pontos de empréstimo: {str(e)}')