# apps/qrcode/tests.py
from django.test import TestCase
from django.contrib.auth.models import User

from .services import QRCodeGenerator
from apps.acervo.models import Livro


class QRCodeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='SenhaForte_123!')
        self.livro = Livro.objects.create(
            titulo='Livro QR', autor='Autor', doador=self.user,
        )

    def test_gerar_qr_code(self):
        resultado = QRCodeGenerator.gerar_qr_code(self.livro)
        self.assertIsNotNone(resultado)

    def test_qr_code_salvo(self):
        QRCodeGenerator.gerar_qr_code(self.livro)
        self.livro.refresh_from_db()
        self.assertTrue(self.livro.qr_code)