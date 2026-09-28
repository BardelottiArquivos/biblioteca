# apps/reservas/tests.py
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Reserva
from .services import GerenciadorFila
from apps.acervo.models import Livro


class ReservaTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='SenhaForte_123!')
        self.user2 = User.objects.create_user(username='user2', password='SenhaForte_123!')
        self.livro = Livro.objects.create(
            titulo='Raro', autor='Autor', doador=self.user1,
        )

    def test_criar_reserva(self):
        r = Reserva.objects.create(livro=self.livro, usuario=self.user2)
        self.assertEqual(r.status, 'A')

    def test_calcular_posicao(self):
        r1 = Reserva.objects.create(livro=self.livro, usuario=self.user2)
        posicao = r1.calcular_posicao()
        self.assertEqual(posicao, 1)

    def test_processar_liberacao(self):
        r1 = Reserva.objects.create(livro=self.livro, usuario=self.user2)
        GerenciadorFila.processar_liberacao_livro(self.livro)
        r1.refresh_from_db()
        self.assertEqual(r1.status, 'C')