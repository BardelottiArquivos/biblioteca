# Dockerfile
# ==============================================
# IMAGEM DE PRODUÇÃO - BIBLIOTECA DO SABER
# ==============================================
FROM python:3.11-slim

# Variáveis de ambiente do Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=biblioteca_do_saber.settings.production

# Diretório de trabalho
WORKDIR /app

# Instala dependências do sistema (PostgreSQL + libs de imagem/QR/Magic)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    libzbar0 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto
COPY . .

# Cria pastas necessárias
RUN mkdir -p /app/logs /app/media /app/staticfiles

# Coleta arquivos estáticos (pode falhar em build se não houver .env)
RUN python manage.py collectstatic --noinput || true

# Expõe a porta
EXPOSE 8000

# Comando padrão (pode ser sobrescrito pelo docker-compose)
CMD ["gunicorn", "biblioteca_do_saber.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
