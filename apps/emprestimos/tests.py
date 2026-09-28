# apps/emprestimos/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import SolicitacaoEmprestimo
from apps.acervo.models import Livro


class EmprestimoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='SenhaForte_123!')
        self.outro = User.objects.create_user(username='outro', password='SenhaForte_123!')
        self.livro = Livro.objects.create(
            titulo='Livro', autor='Autor', doador=self.outro,
        )

    def test_criar_solicitacao(self):
        emp = SolicitacaoEmprestimo.objects.create(
            solicitante=self.user, livro=self.livro,
        )
        self.assertEqual(emp.status, 'P')
        self.assertIsNotNone(emp.data_solicitacao)
