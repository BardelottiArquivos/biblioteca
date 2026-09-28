# apps/usuarios/apps.py
from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.usuarios'
    verbose_name = 'Usuários'

    def ready(self):
        """Importa signals quando o app estiver pronto."""
        import apps.usuarios.signals  # noqa
