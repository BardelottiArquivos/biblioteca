#!/usr/bin/env python
# manage.py
# ==========================================
# PONTO DE ENTRADA DO DJANGO
# ==========================================

import os
import sys


def main():
    """Executa tarefas administrativas do Django."""
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'biblioteca_do_saber.settings.development'
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. Verifique se ele está "
            "instalado e disponível no seu PYTHONPATH. Você se esqueceu "
            "de ativar o ambiente virtual?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
