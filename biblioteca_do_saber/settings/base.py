# biblioteca_do_saber/settings/base.py
# ===============================================
# CONFIGURAÇÕES BASE DO PROJETO (PostgreSQL)
# ===============================================
import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url

# ===============================================
# CAMINHOS
# ===============================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ===============================================
# SEGURANÇA
# ===============================================
SECRET_KEY = config('SECRET_KEY', default='django-insecure-dev-key')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ===============================================
# APPS INSTALADOS
# ===============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'crispy_forms',
    'crispy_bootstrap5',
    'channels',
    'axes',
    #'django_ratelimit',
    'import_export',
    'ckeditor',

    'apps.core.apps.CoreConfig',
    'apps.usuarios.apps.UsuariosConfig',
    'apps.acervo.apps.AcervoConfig',
    'apps.emprestimos.apps.EmprestimosConfig',
    'apps.gamificacao.apps.GamificacaoConfig',
    'apps.chat.apps.ChatConfig',
    'apps.api.apps.ApiConfig',
    'apps.dashboard.apps.DashboardConfig',
    'apps.recomendacao.apps.RecomendacaoConfig',
    'apps.reservas.apps.ReservasConfig',
    'apps.notificacoes.apps.NotificacoesConfig',
    'apps.qrcode.apps.QrcodeConfig',
]

# ===============================================
# MIDDLEWARES
# ===============================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'apps.core.middleware.SecurityHeadersMiddleware',
    'apps.core.middleware.AccessibilityMiddleware',
]

# ===============================================
# URLS E WSGI/ASGI
# ===============================================
ROOT_URLCONF = 'biblioteca_do_saber.urls'
WSGI_APPLICATION = 'biblioteca_do_saber.wsgi.application'
ASGI_APPLICATION = 'biblioteca_do_saber.asgi.application'

# ===============================================
# TEMPLATES
# ===============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_settings',
                'apps.core.context_processors.accessibility_settings',
            ],
        },
    },
]

# ===============================================
# BANCO DE DADOS (PostgreSQL)
# ===============================================
DATABASES = {
    'default': dj_database_url.config(
        default=config(
            'DATABASE_URL',
            default='postgresql://biblioteca_user:biblioteca_pass@localhost:5432/biblioteca_saber'
        ),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = 600

# ===============================================
# VALIDAÇÃO DE SENHAS
# ===============================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    {'NAME': 'apps.usuarios.validators.CustomPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# ===============================================
# INTERNACIONALIZAÇÃO
# ===============================================
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ===============================================
# ARQUIVOS ESTÁTICOS E MÍDIA
# ===============================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ===============================================
# CACHE (Redis)
# ===============================================
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_CACHE_URL', default='redis://localhost:6379/1'),
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
        'KEY_PREFIX': 'biblioteca_saber',
    }
}

# ===============================================
# CHANNELS (WebSocket)
# ===============================================
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [config('REDIS_CHANNEL_URL', default='redis://localhost:6379/2')],
        },
    },
}

# ===============================================
# CELERY
# ===============================================
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 20 * 60

# ===============================================
# EMAIL
# ===============================================
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='nao-responda@biblioteca.com')

# ===============================================
# SEGURANÇA AVANÇADA
# ===============================================
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=0, cast=int)

# ===============================================
# CORS
# ===============================================
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:8000', cast=Csv())
CORS_ALLOW_CREDENTIALS = True

# ===============================================
# CSRF
# ===============================================
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:8000', cast=Csv())

# ===============================================
# SESSÃO
# ===============================================
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_NAME = 'biblioteca_session'
SESSION_COOKIE_AGE = 86400

# ===============================================
# AXES
# ===============================================
AXES_ENABLED = True
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
AXES_LOCK_OUT_AT_FAILURE = True

# ===============================================
# RATE LIMITING
# ===============================================
RATELIMIT_ENABLE = config('RATELIMIT_ENABLE', default=True, cast=bool)
RATELIMIT_RATE = config('RATELIMIT_RATE', default='100/h')

# ===============================================
# CRISPY FORMS
# ===============================================
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# ===============================================
# LOGGING
# ===============================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {'format': '{levelname} {asctime} {module} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'verbose'},
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'biblioteca.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': False},
        'apps': {'handlers': ['console', 'file'], 'level': 'INFO', 'propagate': False},
    },
}

# ===============================================
# REST FRAMEWORK
# ===============================================
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# ===============================================
# LOGIN/LOGOUT
# ===============================================
LOGIN_URL = 'usuarios:login'
LOGIN_REDIRECT_URL = 'dashboard:index'
LOGOUT_REDIRECT_URL = 'core:home'

# ===============================================
# URLs EXTERNAS
# ===============================================
BASE_URL = config('BASE_URL', default='http://localhost:8000')
GOOGLE_BOOKS_API_KEY = config('GOOGLE_BOOKS_API_KEY', default='')