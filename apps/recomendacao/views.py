# apps/recomendacao/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .services import RecomendadorLivros


class RecomendacoesView(LoginRequiredMixin, TemplateView):
    template_name = 'recomendacao/recomendacoes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recomendador = RecomendadorLivros(self.request.user)
        context['recomendacoes'] = recomendador.recomendar_mistos(15)
        return context