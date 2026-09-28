# apps/api/services/google_books.py
# ===============================
# INTEGRAÇÃO COM GOOGLE BOOKS API
# ===============================
import logging
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class GoogleBooksService:
    """Serviço para buscar metadados de livros na Google Books API."""

    BASE_URL = 'https://www.googleapis.com/books/v1/volumes'

    def __init__(self):
        self.api_key = getattr(settings, 'GOOGLE_BOOKS_API_KEY', None)

    def _request(self, params):
        """Faz requisição à API, com tratamento de erros."""
        if self.api_key:
            params['key'] = self.api_key

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f'Erro na Google Books API: {str(e)}')
            return None

    def buscar_por_isbn(self, isbn):
        data = self._request({'q': f'isbn:{isbn}'})
        # CORRIGIDO: checa se 'items' existe antes de acessar
        if not data or not data.get('items'):
            return None
        return self._parse_volume(data['items'][0])

    def buscar_por_titulo(self, titulo, autor=None, limite=5):
        query = f'intitle:{titulo}'
        if autor:
            query += f'+inauthor:{autor}'

        data = self._request({'q': query, 'maxResults': limite})
        if not data or not data.get('items'):
            return []
        return [self._parse_volume(item) for item in data['items']]

    def _parse_volume(self, item):
        info = item.get('volumeInfo', {})
        imagens = info.get('imageLinks', {})

        return {
            'titulo': info.get('title', ''),
            'autores': info.get('authors', []),
            'editora': info.get('publisher', ''),
            'ano_publicacao': self._extract_ano(info.get('publishedDate', '')),
            'paginas': info.get('pageCount'),
            'idioma': info.get('language', 'pt-BR'),
            'resumo': info.get('description', ''),
            'capa_url': imagens.get('thumbnail') or imagens.get('smallThumbnail', ''),
            'isbn': self._extract_isbn(info.get('industryIdentifiers', [])),
        }

    # CORRIGIDO: nome do método era '_extrait_ano' (typo)
    def _extract_ano(self, data_str):
        if not data_str:
            return None
        try:
            return int(data_str[:4])
        except (ValueError, TypeError):
            return None

    # CORRIGIDO: nome do método era '_extrait_isbn' (typo)
    def _extract_isbn(self, identifiers):
        isbn_10 = None
        isbn_13 = None
        for ident in identifiers:
            if ident.get('type') == 'ISBN_13':
                isbn_13 = ident.get('identifier')
            elif ident.get('type') == 'ISBN_10':
                isbn_10 = ident.get('identifier')
        return isbn_13 or isbn_10 or ''