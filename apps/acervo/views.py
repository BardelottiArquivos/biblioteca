# apps/acervo/views.py
import logging

from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, CreateView, ListView
from django.http import JsonResponse
from django.urls import reverse
from django_ratelimit.decorators import ratelimit

from .models import Livro
from .forms import LivroForm, AvaliacaoForm

logger = logging.getLogger(__name__)


class AcervoListView(ListView):
    """Lista de livros com busca, filtros e paginação."""
    model = Livro
    template_name = 'acervo/lista.html'
    context_object_name = 'livros'
    paginate_by = 12

    def get_queryset(self):
        # CORRIGIDO: usa status__in (duplo underscore)
        queryset = Livro.objects.filter(
            status__in=['DD', 'DE']
        ).select_related('doador')

        # Filtro de busca textual
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(titulo__icontains=q) |
                Q(autor__icontains=q) |
                Q(isbn__icontains=q)
            )

        # Filtro por gênero
        genero = self.request.GET.get('genero', '').strip()
        if genero:
            queryset = queryset.filter(genero=genero)

        return queryset.order_by('-data_cadastro')


class LivroDetailView(DetailView):
    """Detalhes de um livro."""
    model = Livro
    template_name = 'acervo/detalhes.html'
    context_object_name = 'livro'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Livro.objects.select_related('doador').prefetch_related(
            'avaliacoes__usuario'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        livro = self.get_object()

        # CORRIGIDO: usa status__in
        context['avaliacoes'] = livro.avaliacoes.all().order_by('-data_avaliacao')[:10]

        if self.request.user.is_authenticated:
            context['form_avaliacao'] = AvaliacaoForm(
                usuario=self.request.user, livro=livro
            )

        # Livros similares (mesmo gênero, disponíveis) — CORRIGIDO: status__in
        context['livros_similares'] = Livro.objects.filter(
            genero=livro.genero,
            status__in=['DD', 'DE'],
        ).exclude(id=livro.id)[:4]

        return context


class CadastrarLivroView(LoginRequiredMixin, CreateView):
    """Cadastro de novo livro."""
    model = Livro
    form_class = LivroForm
    template_name = 'acervo/cadastrar.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)

        # Concede pontos pela doação (com try/except para não quebrar se o app falhar)
        try:
            from apps.gamificacao.services import GamificacaoService
            GamificacaoService.conceder_pontos(
                usuario=self.request.user,
                tipo='DOACAO',
                objeto=self.object,
                descricao=f'Doação do livro: {self.object.titulo}',
            )
        except Exception as e:
            logger.error(f'Erro ao conceder pontos de doação: {e}')

        messages.success(self.request, 'Livro cadastrado com sucesso!')
        return response

    def get_success_url(self):
        # CORRIGIDO: self.object.slug (com ponto)
        return reverse('acervo:detalhes', kwargs={'slug': self.object.slug})


class BuscarISBNView(LoginRequiredMixin, View):
    """Busca livro por ISBN via Google Books API."""

    @method_decorator(ratelimit(key='user', rate='20/h', method='GET'))
    def get(self, request):
        isbn = request.GET.get('isbn', '').strip()
        if not isbn:
            return JsonResponse({'error': 'ISBN não informado.'}, status=400)

        try:
            from apps.core.validators import ISBNValidator
            ISBNValidator.validate_isbn(isbn)

            from apps.api.services.google_books import GoogleBooksService
            service = GoogleBooksService()
            dados = service.buscar_por_isbn(isbn)

            if dados:
                return JsonResponse({'success': True, 'data': dados})
            return JsonResponse({'error': 'Livro não encontrado.'}, status=404)

        except Exception as e:
            logger.error(f'Erro ao buscar ISBN {isbn}: {str(e)}')
            return JsonResponse({'error': str(e)}, status=400)