# apps/gamificacao/apps.py
from django.apps import AppConfig


class GamificacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.gamificacao'
    verbose_name = 'Gamificação'

    def ready(self):
        """Importa signals quando o app estiver pronto."""
        import apps.gamificacao.signals  # noqa