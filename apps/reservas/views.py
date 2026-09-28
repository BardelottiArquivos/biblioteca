# apps/reservas/views.py
from django.views.generic import ListView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Reserva
from apps.acervo.models import Livro


class ListaReservasView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'reservas/lista.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        return Reserva.objects.filter(
            usuario=self.request.user
        ).select_related('livro')


class CriarReservaView(LoginRequiredMixin, CreateView):
    model = Reserva
    template_name = 'reservas/criar.html'
    fields = []

    def dispatch(self, request, *args, **kwargs):
        self.livro = get_object_or_404(Livro, slug=kwargs['slug'])

        # CORRIGIDO: status__in
        if Reserva.objects.filter(
            livro=self.livro, usuario=request.user, status__in=['A', 'C'],
        ).exists():
            messages.warning(request, 'Você já reservou este livro.')
            return redirect('acervo:detalhes', slug=self.livro.slug)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.livro = self.livro
        # Calcula posição na fila
        form.instance.posicao_fila = Reserva.objects.filter(
            livro=self.livro, status='A'
        ).count() + 1

        messages.success(
            self.request,
            f'Reserva feita! Posição: {form.instance.posicao_fila}'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('reservas:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['livro'] = self.livro
        return context


class CancelarReservaView(LoginRequiredMixin, View):
    def post(self, request, pk):
        reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
        reserva.status = 'X'
        reserva.save(update_fields=['status'])
        messages.info(request, 'Reserva cancelada.')
        return redirect('reservas:lista')