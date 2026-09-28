# apps/core/utils.py
# ========================
# FUNÇÕES UTILITÁRIAS
# ========================
import re
from django.utils.text import slugify


def generate_slug(text):
    """Gera um slug amigável a partir de um texto."""
    if not text:
        return ''
    slug = slugify(text, allow_unicode=False)
    # Remove hífens duplicados e das extremidades
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug
