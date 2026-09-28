# apps/usuarios/views.py
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Perfil
from .forms import PerfilForm


class CadastroView(CreateView):
    """Cadastro de novo usuário."""
    form_class = UserCreationForm
    template_name = 'usuarios/cadastro.html'
    success_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Cadastro realizado! Faça login para continuar.'
        )
        return response


class PerfilView(LoginRequiredMixin, DetailView):
    """Exibe o perfil do usuário logado."""
    model = User
    template_name = 'usuarios/perfil.html'
    context_object_name = 'usuario_perfil'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil, _ = Perfil.objects.get_or_create(usuario=self.request.user)
        context['perfil'] = perfil
        return context


class EditarPerfilView(LoginRequiredMixin, UpdateView):
    """Edita o perfil do usuário logado."""
    model = Perfil
    form_class = PerfilForm
    template_name = 'usuarios/editar_perfil.html'
    success_url = reverse_lazy('usuarios:perfil')

    def get_object(self, queryset=None):
        perfil, _ = Perfil.objects.get_or_create(usuario=self.request.user)
        return perfil

    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)