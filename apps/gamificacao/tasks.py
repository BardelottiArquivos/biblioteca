# apps/gamificacao/tasks.py
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def atualizar_ranking_semanal():
    logger.info('Atualizando ranking semanal...')
    # TODO: implementar lógica