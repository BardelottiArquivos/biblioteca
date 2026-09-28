# biblioteca_do_saber/celery.py
# ========================
# CONFIGURACAO DO CELERY
# ========================

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'biblioteca_do_saber.settings.development'
)

app = Celery('biblioteca_do_saber')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# ========================
# TAREFAS AGENDADAS (CRON JOBS)
# ========================
app.conf.beat_schedule = {
    'expirar-reservas': {
        'task': 'apps.reservas.tasks.expirar_reservas_vencidas',
        'schedule': crontab(hour=0, minute=0),
    },
    'atualizar-ranking': {
        'task': 'apps.gamificacao.tasks.atualizar_ranking_semanal',
        'schedule': crontab(day_of_week='sun', hour=23, minute=59),
    },
    'sincronizar-bibliotecas': {
        'task': 'apps.api.tasks.sincronizar_bibliotecas',
        'schedule': crontab(hour=3, minute=0),
    },
    'enviar-notificacoes': {
        'task': 'apps.notificacoes.tasks.enviar_notificacoes_pendentes',
        'schedule': crontab(minute='*/15'),
    },
}
