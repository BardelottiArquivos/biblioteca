# biblioteca_do_saber/asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'biblioteca_do_saber.settings.development'
)

django_asgi_app = get_asgi_application()

# Importar DEPOIS do setup do Django
from apps.chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
