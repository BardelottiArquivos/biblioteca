# apps/emprestimos/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect

from .models import SolicitacaoEmprestimo
from apps.acervo.models import Livro


class ListaEmprestimosView(LoginRequiredMixin, ListView):
    model = SolicitacaoEmprestimo
    template_name = 'emprestimos/lista.html'
    context_object_name = 'emprestimos'
    paginate_by = 20

    def get_queryset(self):
        return SolicitacaoEmprestimo.objects.filter(
            solicitante=self.request.user
        ).select_related('livro').order_by('-data_solicitacao')


class DetalhesEmprestimoView(LoginRequiredMixin, DetailView):
    model = SolicitacaoEmprestimo
    template_name = 'emprestimos/detalhes.html'
    context_object_name = 'emprestimo'

    def get_queryset(self):
        return SolicitacaoEmprestimo.objects.filter(solicitante=self.request.user)


class SolicitarEmprestimoView(LoginRequiredMixin, CreateView):
    model = SolicitacaoEmprestimo
    template_name = 'emprestimos/solicitar.html'
    fields = ['observacoes']

    def dispatch(self, request, *args, **kwargs):
        # Busca o livro pela slug
        self.livro = get_object_or_404(Livro, slug=kwargs['slug'])

        # Não deixa o usuário solicitar empréstimo do próprio livro
        if self.livro.doador_id == request.user.id:
            messages.warning(request, 'Você não pode solicitar empréstimo do seu próprio livro.')
            return redirect('acervo:detalhes', slug=self.livro.slug)

        # Verifica se já existe solicitação ativa — CORRIGIDO: status__in
        if SolicitacaoEmprestimo.objects.filter(
            solicitante=request.user,
            livro=self.livro,
            status__in=['P', 'A'],
        ).exists():
            messages.warning(request, 'Você já tem uma solicitação ativa para este livro.')
            return redirect('acervo:detalhes', slug=self.livro.slug)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.solicitante = self.request.user
        form.instance.livro = self.livro
        messages.success(self.request, 'Solicitação enviada! Aguarde aprovação.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('emprestimos:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['livro'] = self.livro
        return context