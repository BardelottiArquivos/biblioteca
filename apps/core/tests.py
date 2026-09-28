# apps/core/tests.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from .validators import ISBNValidator, SecurityValidator


class ISBNValidatorTestCase(TestCase):
    def test_isbn13_valid(self):
        resultado = ISBNValidator.validate_isbn('978-85-1234-567-8')
        self.assertEqual(resultado, '9788512345678')

    def test_isbn13_invalid(self):
        with self.assertRaises(ValidationError):
            ISBNValidator.validate_isbn('978-85-1234-567-9')

    def test_isbn10_valid(self):
        resultado = ISBNValidator.validate_isbn('85-359-0277-5')
        self.assertEqual(resultado, '8535902775')


class SecurityValidatorTestCase(TestCase):
    def test_xss_bloqueado(self):
        with self.assertRaises(ValidationError):
            SecurityValidator.validate_xss_safe('<script>alert(1)</script>')

    def test_sanitize_html(self):
        entrada = '<p>Bom</p><script>alert(1)</script>'
        saida = SecurityValidator.sanitize_html(entrada)
        self.assertIn('<p>Bom</p>', saida)
        self.assertNotIn('<script>', saida)
