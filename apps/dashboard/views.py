# apps/dashboard/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum

from apps.acervo.models import Livro
from apps.emprestimos.models import SolicitacaoEmprestimo
from apps.reservas.models import Reserva
from apps.gamificacao.models import PontuacaoUsuario, HistoricoPontos


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['total_emprestimos'] = SolicitacaoEmprestimo.objects.filter(
            solicitante=user
        ).count()

        context['emprestimos_ativos'] = SolicitacaoEmprestimo.objects.filter(
            solicitante=user, status='A'
        ).count()

        context['total_reservas'] = Reserva.objects.filter(usuario=user).count()
        context['livros_doados'] = Livro.objects.filter(doador=user).count()

        pontuacao, _ = PontuacaoUsuario.objects.get_or_create(usuario=user)
        context['pontuacao'] = pontuacao

        context['ultimas_atividades'] = HistoricoPontos.objects.filter(
            usuario=user
        ).order_by('-data')[:5]

        return context


class EstatisticasView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/estatisticas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['emprestimos_por_status'] = SolicitacaoEmprestimo.objects.filter(
            solicitante=user
        ).values('status').annotate(total=Count('id'))

        context['pontos_por_acao'] = HistoricoPontos.objects.filter(
            usuario=user
        ).values('acao__tipo').annotate(total=Sum('pontos'))

        return context