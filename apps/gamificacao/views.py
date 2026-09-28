# apps/gamificacao/views.py
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import PontuacaoUsuario, HistoricoPontos
from .services import GamificacaoService


class RankingView(ListView):
    template_name = 'gamificacao/ranking.html'
    context_object_name = 'ranking'
    paginate_by = 50

    def get_queryset(self):
        return PontuacaoUsuario.objects.filter(
            pontos_totais__gt=0
        ).select_related('usuario').order_by('-pontos_totais')


class MeuProgressoView(LoginRequiredMixin, TemplateView):
    template_name = 'gamificacao/meu_progresso.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        pontuacao, _ = PontuacaoUsuario.objects.get_or_create(usuario=user)
        context['pontuacao'] = pontuacao
        context['posicao'] = GamificacaoService.get_posicao(user)
        context['proxima_conquista'] = GamificacaoService.get_proxima_conquista(user)
        context['historico'] = HistoricoPontos.objects.filter(
            usuario=user
        ).order_by('-data')[:20]
        return context


class ComoFuncionaView(TemplateView):
    template_name = 'gamificacao/como_funciona.html'