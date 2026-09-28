# apps/recomendacao/tests.py
from django.test import TestCase
from django.contrib.auth.models import User

from .services import RecomendadorLivros
from apps.acervo.models import Livro


class RecomendadorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='leitor', password='SenhaForte_123!')
        self.outro = User.objects.create_user(username='outro', password='SenhaForte_123!')

        Livro.objects.create(
            titulo='Fantasia 1', autor='A', genero='FAN', doador=self.outro,
        )
        Livro.objects.create(
            titulo='Fantasia 2', autor='A', genero='FAN', doador=self.outro,
        )

    def test_recomendador_inicializa(self):
        rec = RecomendadorLivros(self.user)
        self.assertEqual(rec.usuario, self.user)

    def test_recomendar_sem_historico(self):
        rec = RecomendadorLivros(self.user)
        recomendacoes = rec.recomendar_por_genero(limite=5)
        self.assertGreater(len(recomendacoes), 0)