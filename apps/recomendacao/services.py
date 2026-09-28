# apps/recomendacao/services.py
# ============================================
# SERVIÇO DE RECOMENDAÇÃO
# ============================================
import logging

from django.db.models import Count
from django.contrib.auth.models import User

from apps.acervo.models import Livro, Avaliacao
from apps.emprestimos.models import SolicitacaoEmprestimo

logger = logging.getLogger(__name__)


class RecomendadorLivros:
    """Sistema de recomendação baseado em histórico e preferências."""

    def __init__(self, usuario):
        self.usuario = usuario
        self.livros_vistos = self._get_livros_vistos()
        self.generos_preferidos = self._get_generos_preferidos()
        self.autores_preferidos = self._get_autores_preferidos()

    def _get_livros_vistos(self):
        emprestimos = SolicitacaoEmprestimo.objects.filter(
            solicitante=self.usuario, status__in=['A', 'D'],
        ).values_list('livro_id', flat=True)

        avaliacoes = Avaliacao.objects.filter(
            usuario=self.usuario
        ).values_list('livro_id', flat=True)

        return set(list(emprestimos) + list(avaliacoes))

    def _get_generos_preferidos(self):
        if not self.livros_vistos:
            return []

        livros_interagidos = Livro.objects.filter(id__in=self.livros_vistos)
        generos = livros_interagidos.values('genero').annotate(
            total=Count('id')
        ).order_by('-total')
        return [item['genero'] for item in generos[:3]]

    def _get_autores_preferidos(self):
        if not self.livros_vistos:
            return []

        livros_interagidos = Livro.objects.filter(id__in=self.livros_vistos)
        autores = livros_interagidos.values('autor').annotate(
            total=Count('id')
        ).order_by('-total')
        return [item['autor'] for item in autores[:3]]

    def recomendar_por_genero(self, limite=10):
        if not self.generos_preferidos:
            return Livro.objects.filter(
                status__in=['DD', 'DE']
            ).order_by('?')[:limite]

        recomendacoes = Livro.objects.filter(
            genero__in=self.generos_preferidos,
            status__in=['DD', 'DE'],
        ).exclude(id__in=self.livros_vistos)

        return recomendacoes[:limite]

    def recomendar_por_autor(self, limite=10):
        if not self.autores_preferidos:
            return Livro.objects.filter(
                status__in=['DD', 'DE']
            ).order_by('?')[:limite]

        return Livro.objects.filter(
            autor__in=self.autores_preferidos,
            status__in=['DD', 'DE'],
        ).exclude(id__in=self.livros_vistos)[:limite]

    def recomendar_por_similaridade(self, limite=10):
        if not self.livros_vistos:
            return Livro.objects.none()

        usuarios_similares = User.objects.exclude(
            id=self.usuario.id
        ).filter(
            emprestimos__livro__in=self.livros_vistos,
        ).annotate(
            similaridade=Count('emprestimos')
        ).order_by('-similaridade')[:5]

        livros_similares = Livro.objects.filter(
            emprestimos__solicitante__in=usuarios_similares,
            status__in=['DD', 'DE'],
        ).exclude(id__in=self.livros_vistos)

        return livros_similares[:limite]

    def recomendar_mistos(self, limite=15):
        recomendacoes = []
        ids_vistos = set()

        estrategias = [
            self.recomendar_por_genero(5),
            self.recomendar_por_autor(5),
            self.recomendar_por_similaridade(5),
        ]

        for estrategia in estrategias:
            for livro in estrategia:
                if livro.id not in ids_vistos:
                    recomendacoes.append(livro)
                    ids_vistos.add(livro.id)
                if len(recomendacoes) >= limite:
                    break
            if len(recomendacoes) >= limite:
                break

        return recomendacoes[:limite]