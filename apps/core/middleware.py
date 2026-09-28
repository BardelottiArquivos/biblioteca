# apps/core/middleware.py
# ========================
# MIDDLEWARES CUSTOMIZADOS
# ========================
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """Adiciona headers de segurança em todas as respostas."""

    def process_response(self, request, response):
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://vlibras.gov.br; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' https://viacep.com.br https://www.googleapis.com https://vlibras.gov.br; "
            "frame-src https://vlibras.gov.br; "
            "base-uri 'self'; "
            "form-action 'self'; "
            "object-src 'none';"
        )
        response['Content-Security-Policy'] = csp

        if not settings.DEBUG and settings.SECURE_HSTS_SECONDS > 0:
            response['Strict-Transport-Security'] = (
                f'max-age={settings.SECURE_HSTS_SECONDS}; includeSubDomains; preload'
            )
        return response


class AccessControlMiddleware(MiddlewareMixin):
    """Controla acesso por IP e rate limiting básico."""

    def process_request(self, request):
        ip = self._get_client_ip(request)
        if not ip:
            return None

        if self._is_rate_limited(ip):
            logger.warning(f'Rate limit excedido: {ip}')
            return HttpResponseForbidden('Muitas requisições. Tente novamente mais tarde.')
        return None

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    def _is_rate_limited(self, ip):
        key = f'rate_limit_{ip}'
        count = cache.get(key, 0)
        if count > 100:
            return True
        cache.set(key, count + 1, 60)
        return False


class AccessibilityMiddleware(MiddlewareMixin):
    """Carrega preferências de acessibilidade dos cookies."""

    def process_request(self, request):
        request.acessibilidade = {
            'alto_contraste': request.COOKIES.get('alto_contraste', 'false') == 'true',
            'fonte_dislexia': request.COOKIES.get('fonte_dislexia', 'false') == 'true',
            'tamanho_fonte': request.COOKIES.get('tamanho_fonte', 'media'),
        }
