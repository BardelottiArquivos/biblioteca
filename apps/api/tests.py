# apps/api/tests.py
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from apps.acervo.models import Livro


class LivroAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='api_user', password='SenhaForte_123!'
        )
        self.livro = Livro.objects.create(
            titulo='Dom Casmurro', autor='Machado',
            genero='ROM', doador=self.user,
        )

    def test_listar_livros(self):
        response = self.client.get('/api/livros/')
        self.assertEqual(response.status_code, 200)

    def test_detalhe_por_slug(self):
        response = self.client.get(f'/api/livros/{self.livro.slug}/')
        self.assertEqual(response.status_code, 200)