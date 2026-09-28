# apps/usuarios/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Perfil


class PerfilTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='teste', password='senha_forte_123!',
            email='teste@teste.com'
        )

    def test_perfil_criado_automaticamente(self):
        self.assertTrue(Perfil.objects.filter(usuario=self.user).exists())

    def test_tipo_padrao_leitor(self):
        self.assertEqual(self.user.perfil.tipo, 'LEITOR')

    def test_str_perfil(self):
        self.assertEqual(str(self.user.perfil), 'Perfil de teste')


class CadastroTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pagina_cadastro_abre(self):
        response = self.client.get(reverse('usuarios:cadastro'))
        self.assertEqual(response.status_code, 200)

    def test_cadastro_cria_usuario(self):
        response = self.client.post(reverse('usuarios:cadastro'), {
            'username': 'novo_user',
            'password1': 'senha_forte_xyz_123!',
            'password2': 'senha_forte_xyz_123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='novo_user').exists())