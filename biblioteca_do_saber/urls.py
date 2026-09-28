# biblioteca_do_saber/urls.py
# =======================
# ROTAS PRINCIPAIS DO PROJETO
# =======================

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('acervo/', include('apps.acervo.urls')),
    path('emprestimos/', include('apps.emprestimos.urls')),
    path('gamificacao/', include('apps.gamificacao.urls')),
    path('chat/', include('apps.chat.urls')),
    path('api/', include('apps.api.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('recomendacao/', include('apps.recomendacao.urls')),
    path('reservas/', include('apps.reservas.urls')),
    path('notificacoes/', include('apps.notificacoes.urls')),
    path('qrcode/', include('apps.qrcode.urls')),
]

# Arquivos de mídia e estáticos (apenas em desenvolvimento)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
