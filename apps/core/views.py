# apps/core/views.py
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'core/home.html'


class SobreView(TemplateView):
    template_name = 'core/sobre.html'


class ContatoView(TemplateView):
    template_name = 'core/contato.html'


class PrivacidadeView(TemplateView):
    template_name = 'core/privacidade.html'


class TermosView(TemplateView):
    template_name = 'core/termos.html'
