# apps/acervo/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Livro, Avaliacao


class LivroTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='SenhaForte_123!')

    def test_criar_livro(self):
        livro = Livro.objects.create(
            titulo='Dom Casmurro', autor='Machado de Assis', doador=self.user,
        )
        self.assertEqual(livro.titulo, 'Dom Casmurro')
        self.assertTrue(livro.is_disponivel)

    def test_slug_gerado_automaticamente(self):
        livro = Livro.objects.create(
            titulo='O Cortiço', autor='Aluísio Azevedo', doador=self.user,
        )
        self.assertEqual(livro.slug, 'o-cortico')

    def test_slug_unico_para_mesmo_titulo(self):
        l1 = Livro.objects.create(titulo='Mesmo Título', autor='A', doador=self.user)
        l2 = Livro.objects.create(titulo='Mesmo Título', autor='B', doador=self.user)
        self.assertNotEqual(l1.slug, l2.slug)

    def test_recursos_acessibilidade(self):
        livro = Livro.objects.create(
            titulo='Livro Acessível', autor='Autor', doador=self.user,
            possui_braille=True, possui_audio=True,
        )
        self.assertIn('Braille', livro.recursos_acessibilidade)
        self.assertIn('Áudio', livro.recursos_acessibilidade)


class AvaliacaoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='SenhaForte_123!')
        self.livro = Livro.objects.create(
            titulo='Livro', autor='Autor', doador=self.user,
        )

    def test_avaliacao_criada(self):
        av = Avaliacao.objects.create(livro=self.livro, usuario=self.user, nota=5)
        self.assertEqual(av.nota, 5)