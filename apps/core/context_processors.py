# apps/core/context_processors.py
# ==============================================
# CONTEXT PROCESSORS - Variáveis globais em templates
# ==============================================
from django.conf import settings


def site_settings(request):
    """Disponibiliza configurações do site em todos os templates."""
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'Biblioteca do Saber'),
        'PWA_APP_NAME': getattr(settings, 'PWA_APP_NAME', 'Biblioteca do Saber'),
    }


def accessibility_settings(request):
    """Disponibiliza preferências de acessibilidade em todos os templates."""
    return {
        'acessibilidade': getattr(request, 'acessibilidade', {
            'alto_contraste': False,
            'fonte_dislexia': False,
            'tamanho_fonte': 'media',
        })
    }
