# apps/chat/views.py
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Conversa


class ListaConversasView(LoginRequiredMixin, ListView):
    model = Conversa
    template_name = 'chat/lista_conversas.html'
    context_object_name = 'conversas'

    def get_queryset(self):
        return Conversa.objects.filter(
            participantes=self.request.user
        ).prefetch_related('participantes', 'mensagens')


class ConversaView(LoginRequiredMixin, DetailView):
    model = Conversa
    template_name = 'chat/conversa.html'
    context_object_name = 'conversa'
    pk_url_kwarg = 'conversa_id'

    def get_queryset(self):
        # CORRIGIDO: só mostra conversas em que o usuário participa
        return Conversa.objects.filter(participantes=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mensagens'] = self.object.mensagens.select_related('remetente')
        return context