# apps/chat/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Conversa, Mensagem


class ChatTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='SenhaForte_123!')
        self.user2 = User.objects.create_user(username='user2', password='SenhaForte_123!')

    def test_criar_conversa(self):
        conversa = Conversa.objects.create()
        conversa.participantes.add(self.user1, self.user2)
        self.assertEqual(conversa.participantes.count(), 2)

    def test_enviar_mensagem(self):
        conversa = Conversa.objects.create()
        conversa.participantes.add(self.user1, self.user2)
        msg = Mensagem.objects.create(
            conversa=conversa, remetente=self.user1, conteudo='Olá!',
        )
        self.assertEqual(msg.conteudo, 'Olá!')