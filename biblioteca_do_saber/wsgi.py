# biblioteca_do_saber/wsgi.py
# ===============================================
# SERVIDOR WSGI - REQUISIÇÕES HTTP SÍNCRONAS
# ===============================================

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'biblioteca_do_saber.settings.development'
)

application = get_wsgi_application()
