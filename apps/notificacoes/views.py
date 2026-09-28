# apps/notificacoes/views.py
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


class ListaNotificacoesView(LoginRequiredMixin, ListView):
    template_name = 'notificacoes/lista.html'
    context_object_name = 'notificacoes'

    def get_queryset(self):
        return []