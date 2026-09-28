# apps/gamificacao/tests.py
from django.test import TestCase
from django.contrib.auth.models import User

from .models import Acao, PontuacaoUsuario
from .services import GamificacaoService


class GamificacaoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teste', password='SenhaForte_123!'
        )
        Acao.objects.create(tipo='CADASTRO', pontos=20, descricao='Cadastro')
        Acao.objects.create(tipo='DOACAO', pontos=50, descricao='Doação')

    def test_conceder_pontos(self):
        sucesso = GamificacaoService.conceder_pontos(self.user, 'DOACAO')
        self.assertTrue(sucesso)

        pontuacao = PontuacaoUsuario.objects.get(usuario=self.user)
        # 20 (cadastro automático) + 50 (doação)
        self.assertEqual(pontuacao.pontos_totais, 70)

    def test_ranking(self):
        GamificacaoService.conceder_pontos(self.user, 'DOACAO')
        ranking = GamificacaoService.get_ranking(limit=10)
        self.assertEqual(len(ranking), 1)