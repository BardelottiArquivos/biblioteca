# apps/core/validators.py
# ==============================================
# VALIDADORES DE SEGURANÇA E DADOS
# ==============================================
import re
import bleach
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class SecurityValidator:
    """Protege contra XSS e código malicioso."""

    # Tags HTML permitidas (whitelist)
    ALLOWED_TAGS = [
        'p', 'br', 'strong', 'em', 'u', 'a',
        'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4',
        'blockquote', 'code', 'pre',
    ]

    ALLOWED_ATTRS = {
        'a': ['href', 'title'],
    }

    @staticmethod
    def validate_xss_safe(value):
        """Verifica se o valor contém código malicioso."""
        if not value:
            return value

        patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=\s*["\'].*?["\']',
            r'<iframe.*?</iframe>',
            r'<object.*?</object>',
            r'<embed.*?>',
        ]
        for pattern in patterns:
            if re.search(pattern, value, re.IGNORECASE | re.DOTALL):
                raise ValidationError(_('Conteúdo com código malicioso detectado.'))
        return value

    @staticmethod
    def sanitize_html(value):
        """Limpa HTML, removendo tags e atributos não permitidos."""
        if not value:
            return value
        return bleach.clean(
            value,
            tags=SecurityValidator.ALLOWED_TAGS,
            attributes=SecurityValidator.ALLOWED_ATTRS,
            strip=True,
            strip_comments=True,
        )


class ISBNValidator:
    """Valida ISBN-10 e ISBN-13 com cálculo de dígito verificador."""

    @staticmethod
    def validate_isbn(value):
        """Valida ISBN (10 ou 13 dígitos)."""
        isbn = re.sub(r'[-\s]', '', value or '')
        if len(isbn) == 10:
            return ISBNValidator._validate_isbn10(isbn)
        elif len(isbn) == 13:
            return ISBNValidator._validate_isbn13(isbn)
        else:
            raise ValidationError(_('ISBN deve ter 10 ou 13 dígitos.'))

    @staticmethod
    def _validate_isbn10(isbn):
        """Valida ISBN-10 com cálculo do dígito verificador."""
        if not isbn[:-1].isdigit():
            raise ValidationError(_('ISBN-10 inválido.'))

        total = 0
        for i, char in enumerate(isbn[:-1]):
            total += (10 - i) * (10 if char.upper() == 'X' else int(char))

        check = (11 - (total % 11)) % 11
        if check == 10:
            check = 'X'

        if str(check).upper() != isbn[-1].upper():
            raise ValidationError(_('Dígito verificador do ISBN-10 inválido.'))
        return isbn

    @staticmethod
    def _validate_isbn13(isbn):
        """Valida ISBN-13 com cálculo do dígito verificador."""
        if not isbn.isdigit():
            raise ValidationError(_('ISBN-13 deve conter apenas números.'))

        total = 0
        for i, char in enumerate(isbn[:-1]):
            total += int(char) * (1 if i % 2 == 0 else 3)

        check = (10 - (total % 10)) % 10
        if check != int(isbn[-1]):
            raise ValidationError(_('Dígito verificador do ISBN-13 inválido.'))
        return isbn

