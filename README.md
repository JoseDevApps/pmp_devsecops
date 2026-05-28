# PMP DevSecOps

Entorno de desarrollo y migración de Django monolítico a microservicios con pipeline
DevSecOps alineado a OWASP.

Stack: Python 3.12 · Django 4.2 · PostgreSQL 15 · Redis 7 · MinIO · Celery · Docker Compose · GitHub Actions

---

## Arquitectura

```
Internet → Nginx :80
               ├── /          → service-web  (dashboard, public, registration)
               ├── /api/      → service-api  (REST API — JWT)
               └── /ws/       → service-ws   (WebSocket — Channels)

Interno:
  service-worker  (Celery)
  PostgreSQL 15
  Redis 7
  MinIO (S3-compatible)
```

Documentación completa: [docs/arquitectura-microservicios.md](docs/arquitectura-microservicios.md)

---

## Inicio rápido

```bash
# 1. Copiar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales locales

# 2. Levantar todos los servicios
make up

# o directamente:
docker compose up --build
```

Servicios disponibles:
- Web:    http://localhost/
- API:    http://localhost/api/
- WS:     ws://localhost/ws/
- MinIO:  http://localhost:9011 (consola)

---

## Comandos útiles

```bash
make lint          # ruff en todos los servicios
make test          # pytest en web y api
make security      # gitleaks + trivy fs + bandit
make docker-build  # construir imágenes locales
make docker-scan   # trivy image scan local
make migrate       # python manage.py migrate en web
make shell         # shell Django en web
```

---

## Pipeline DevSecOps

| Stage | Herramienta | Bloquea merge |
|---|---|---|
| Workflow lint | actionlint + zizmor | Sí |
| Secret scan | Gitleaks | Sí |
| SAST Python | CodeQL + Semgrep | Sí |
| SCA | OSV Scanner + Dependabot | Por severidad |
| Docker scan | Trivy CRITICAL+HIGH | Sí |
| SBOM + Attestation | Docker Buildx + GitHub Attest | En release |
| DAST | OWASP ZAP (manual) | Por hallazgo |

---

## Documentación

| Documento | Descripción |
|---|---|
| [docs/arquitectura-microservicios.md](docs/arquitectura-microservicios.md) | Arquitectura y fases de migración |
| [docs/inventario-riesgos.md](docs/inventario-riesgos.md) | Matriz de riesgos (del diagnóstico PMP_2026) |
| [docs/devsecops-checklist.md](docs/devsecops-checklist.md) | Checklist y roadmap 30/60/90 días |
| [docs/owasp-asvs-mapping.md](docs/owasp-asvs-mapping.md) | Mapeo de controles vs ASVS L2 |
| [docs/threat-model.md](docs/threat-model.md) | Modelo de amenazas STRIDE |

---

## Seguridad

- Ver [docs/inventario-riesgos.md](docs/inventario-riesgos.md) para riesgos activos.
- Nunca versionar el archivo `.env`.
- Rotar credenciales antes del primer despliegue a producción (H-01).
- Eliminar o aislar `views2.py` del monolito antes de migrar (H-02).
