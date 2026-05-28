.PHONY: help lint test security docker-build docker-scan up down logs migrate shell superuser

REGISTRY  ?= ghcr.io/josedevapps
TAG       ?= local
SERVICES  := web api ws worker

help:
	@echo ""
	@echo "  PMP DevSecOps — Comandos disponibles"
	@echo "  ─────────────────────────────────────"
	@echo "  make up            Levanta todos los servicios (dev)"
	@echo "  make down          Detiene y elimina contenedores"
	@echo "  make logs          Muestra logs de todos los servicios"
	@echo "  make lint          Lint ruff en todos los servicios"
	@echo "  make test          Ejecuta pytest en todos los servicios"
	@echo "  make security      Escaneo de secretos y dependencias local"
	@echo "  make docker-build  Construye imágenes de todos los servicios"
	@echo "  make docker-scan   Trivy scan en imágenes locales"
	@echo "  make migrate       Ejecuta migraciones en servicio web"
	@echo "  make superuser     Crea superusuario admin (primera vez)"
	@echo "  make shell         Shell en contenedor web"
	@echo ""

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

lint:
	@for svc in $(SERVICES); do \
	  echo ">> Lint: services/$$svc"; \
	  ruff check services/$$svc/ || true; \
	done

test:
	@for svc in web api; do \
	  echo ">> Tests: services/$$svc"; \
	  pytest services/$$svc/ -q --tb=short || true; \
	done

security:
	@echo ">> Gitleaks — búsqueda de secretos"
	gitleaks detect --source . --redact || true
	@echo ""
	@echo ">> Trivy — escaneo de filesystem"
	trivy fs --scanners vuln,secret,misconfig . || true
	@echo ""
	@echo ">> Bandit — análisis estático Python"
	@for svc in $(SERVICES); do \
	  bandit -r services/$$svc/ -ll || true; \
	done

docker-build:
	@for svc in $(SERVICES); do \
	  echo ">> Build: $$svc"; \
	  docker build -t $(REGISTRY)/pmp-$$svc:$(TAG) services/$$svc/ || exit 1; \
	done

docker-scan:
	@for svc in $(SERVICES); do \
	  echo ">> Trivy scan: pmp-$$svc:$(TAG)"; \
	  trivy image --severity HIGH,CRITICAL --exit-code 1 \
	    $(REGISTRY)/pmp-$$svc:$(TAG) || true; \
	done

migrate:
	docker compose exec web python manage.py migrate

superuser:
	docker compose exec web python manage.py shell -c "\
from django.contrib.auth import get_user_model; \
User = get_user_model(); \
u, created = User.objects.get_or_create(username='admin', defaults={'email':'admin@pmp.local','is_staff':True,'is_superuser':True}); \
u.set_password('PMP@admin2026!'); u.save(); \
print('Creado:' if created else 'Actualizado:','admin / PMP@admin2026!')"

shell:
	docker compose exec web python manage.py shell
