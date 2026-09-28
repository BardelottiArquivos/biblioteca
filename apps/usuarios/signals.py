# apps/usuarios/signals.py
# ==============================================
# SIGNALS DO APP USUÁRIOS
# ==============================================
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Perfil


@receiver(post_save, sender=User)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    """Cria um Perfil automaticamente quando um usuário é criado."""
    if created:
        Perfil.objects.get_or_create(usuario=instance)

