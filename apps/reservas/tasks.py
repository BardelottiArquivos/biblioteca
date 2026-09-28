# apps/reservas/tasks.py
import logging
from celery import shared_task
from .services import GerenciadorFila

logger = logging.getLogger(__name__)


@shared_task
def expirar_reservas_vencidas():
    logger.info('Executando expiração de reservas...')
    GerenciadorFila.expirar_reservas()