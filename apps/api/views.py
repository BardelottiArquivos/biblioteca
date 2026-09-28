# apps/api/views.py
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from apps.acervo.models import Livro
from apps.gamificacao.models import PontuacaoUsuario
from apps.gamificacao.services import GamificacaoService
from apps.emprestimos.models import SolicitacaoEmprestimo

from .serializers import (
    LivroSerializer, PontuacaoUsuarioSerializer, EmprestimoSerializer,
)


class LivroViewSet(viewsets.ModelViewSet):
    """API para consulta e gerenciamento de livros."""

    queryset = Livro.objects.filter(ativo=True).select_related('doador')
    serializer_class = LivroSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['genero', 'status', 'tipo_midia']
    search_fields = ['titulo', 'autor', 'isbn']
    ordering_fields = ['data_cadastro', 'titulo']
    lookup_field = 'slug'

    @action(detail=False, methods=['get'])
    def acessiveis(self, request):
        livros = self.get_queryset().filter(possui_braille=True)
        serializer = self.get_serializer(livros, many=True)
        return Response(serializer.data)


class RankingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PontuacaoUsuario.objects.filter(
        pontos_totais__gt=0
    ).select_related('usuario')
    serializer_class = PontuacaoUsuarioSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def top10(self, request):
        top = GamificacaoService.get_ranking(limit=10)
        serializer = self.get_serializer(top, many=True)
        return Response(serializer.data)


class EmprestimoViewSet(viewsets.ModelViewSet):
    serializer_class = EmprestimoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SolicitacaoEmprestimo.objects.filter(
            solicitante=self.request.user
        ).select_related('livro')

    def perform_create(self, serializer):
        serializer.save(solicitante=self.request.user)