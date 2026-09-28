# Makefile
# ==============================================
# ATALHOS PARA COMANDOS COMUNS
# ==============================================

.PHONY: help install migrate makemigrations test run shell superuser populate \
        docker-up docker-down docker-build docker-logs docker-shell \
        docker-migrate docker-populate docker-test \
        collectstatic check clean backup restore

help:
	@echo "Comandos disponíveis:"
	@echo "  make install          - Instala dependências (local)"
	@echo "  make migrate          - Aplica migrações"
	@echo "  make makemigrations   - Cria novas migrações"
	@echo "  make test             - Roda testes"
	@echo "  make run              - Roda servidor de dev"
	@echo "  make shell            - Abre shell do Django"
	@echo "  make superuser        - Cria superusuário"
	@echo "  make populate         - Popula dados iniciais"
	@echo "  make check            - Verifica o projeto"
	@echo "  make collectstatic    - Coleta estáticos"
	@echo "  make docker-up        - Sobe containers"
	@echo "  make docker-down      - Derruba containers"
	@echo "  make docker-build     - Reconstrói imagens"
	@echo "  make docker-logs      - Logs em tempo real"
	@echo "  make docker-shell     - Shell dentro do container"
	@echo "  make docker-migrate   - Migra dentro do container"
	@echo "  make docker-populate  - Popula dentro do container"
	@echo "  make docker-test      - Testes dentro do container"
	@echo "  make backup           - Backup do PostgreSQL"
	@echo "  make restore          - Restaura backup do PostgreSQL"
	@echo "  make clean            - Limpa arquivos temporários"

# ========== Local ==========
install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

test:
	pytest -v --cov=apps

run:
	python manage.py runserver

shell:
	python manage.py shell

superuser:
	python manage.py createsuperuser

populate:
	python scripts/run_populate.py

check:
	python manage.py check

collectstatic:
	python manage.py collectstatic --noinput

# ========== Docker ==========
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose build --no-cache

docker-logs:
	docker-compose logs -f --tail=100

docker-shell:
	docker-compose exec web python manage.py shell

docker-migrate:
	docker-compose exec web python manage.py migrate

docker-populate:
	docker-compose exec web python scripts/run_populate.py

docker-test:
	docker-compose exec web pytest -v

# ========== Backup/Restore ==========
backup:
	@mkdir -p backups
	docker-compose exec -T db pg_dump -U biblioteca_user biblioteca_saber \
		| gzip > backups/backup_$$(date +%Y%m%d_%H%M%S).sql.gz
	@echo "✅ Backup criado em backups/"

restore:
	@read -p "Nome do backup (sem .sql.gz): " file; \
	docker-compose exec -T db psql -U biblioteca_user -d biblioteca_saber \
		< backups/$$file.sql.gz

# ========== Limpeza ==========
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache htmlcov .coverage
	@echo "✅ Limpeza concluída"
