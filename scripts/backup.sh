#!/bin/bash
# scripts/backup.sh
# ==============================================
# BACKUP DO POSTGRESQL
# ==============================================

set -e

BACKUP_DIR="$(dirname "$0")/../backups"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="backup_${TIMESTAMP}.sql.gz"

echo "🔄 Iniciando backup do PostgreSQL..."

docker-compose exec -T db pg_dump \
    -U "${POSTGRES_USER:-biblioteca_user}" \
    -d "${POSTGRES_DB:-biblioteca_saber}" \
    --no-owner \
    --no-acl \
    | gzip > "${BACKUP_DIR}/${FILENAME}"

echo "✅ Backup criado: ${BACKUP_DIR}/${FILENAME}"
echo "📦 Tamanho: $(du -h "${BACKUP_DIR}/${FILENAME}" | cut -f1)"

# Remove backups com mais de 30 dias
find "$BACKUP_DIR" -name "backup_*.sql.gz" -mtime +30 -delete
echo "🧹 Backups antigos removidos"
