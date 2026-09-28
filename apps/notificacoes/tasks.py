# apps/notificacoes/tasks.py
import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def enviar_notificacoes_pendentes():
    logger.info('Enviando notificações pendentes...')
    # TODO: implementar lógica