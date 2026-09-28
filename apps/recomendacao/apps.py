# apps/recomendacao/apps.py
from django.apps import AppConfig


class RecomendacaoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.recomendacao'
    verbose_name = 'Recomendação'