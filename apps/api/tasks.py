# apps/api/tasks.py
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def sincronizar_bibliotecas():
    logger.info('Sincronizando com bibliotecas parceiras...')
    # TODO: implementar