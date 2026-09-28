# apps/usuarios/validators.py
# ==============================================
# VALIDADOR DE SENHA FORTE
# ==============================================
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomPasswordValidator:
    """Valida que a senha contém letras, números e caracteres especiais."""

    def validate(self, password, user=None):
        if not re.search(r'[A-Za-z]', password):
            raise ValidationError(
                _('A senha deve conter pelo menos uma letra.'),
                code='password_no_letter',
            )
        if not re.search(r'\d', password):
            raise ValidationError(
                _('A senha deve conter pelo menos um número.'),
                code='password_no_number',
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError(
                _('A senha deve conter pelo menos um caractere especial.'),
                code='password_no_special',
            )

    def get_help_text(self):
        return _('Sua senha deve conter letras, números e caracteres especiais.')