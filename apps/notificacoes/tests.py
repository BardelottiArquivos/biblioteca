# apps/notificacoes/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail

from .services import NotificacaoService


class NotificacaoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teste', email='teste@teste.com',
            password='SenhaForte_123!'
        )

    def test_enviar_notificacao_email(self):
        NotificacaoService.enviar_notificacao(
            usuario=self.user, tipo='TESTE',
            titulo='Teste', mensagem='Mensagem',
        )
        self.assertEqual(len(mail.outbox), 1)