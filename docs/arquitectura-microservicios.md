# Arquitectura de Microservicios — PMP
Fecha: 2026-05-28

## Contexto: migración desde monolito Django

El monolito original (`PMP_2026`) contiene 13 aplicaciones Django en un único proceso:
actividad, api, blog, dashboard, ecologico, economico, equilibrio, mail, notification,
personal, public, registration, social.

La migración se hace por fases, extrayendo primero los límites funcionales más claros.

## Arquitectura objetivo

```
Internet
   │
   ▼
[Nginx — API Gateway :80]
   │
   ├── /           → service-web  :8000  (dashboard, public, registration)
   ├── /api/       → service-api  :8001  (REST API — DRF)
   ├── /ws/        → service-ws   :8002  (WebSocket — Channels + Daphne)
   └── /static/    → archivos estáticos

[Servicios internos — red Docker privada]
   ├── service-worker  (Celery — tareas async: mail, notificaciones, reportes)
   ├── PostgreSQL 15   (base de datos compartida — migrar a schemas separados)
   ├── Redis 7         (caché + broker Celery + channel layer WebSocket)
   └── MinIO           (object storage S3-compatible — media e imágenes)
```

## Responsabilidades por servicio

### service-web
- Módulos migrados: dashboard, public, registration, social, personal, blog
- Auth: Django sessions + middleware de autorización por grupos
- Tecnología: Django 4.2 + Gunicorn + Python 3.12

### service-api
- Módulos: api (REST pública y/o interna)
- Auth: JWT (djangorestframework-simplejwt)
- Documentación: OpenAPI automática (drf-spectacular)
- Tecnología: Django 4.2 + DRF + Gunicorn + Python 3.12

### service-ws
- Módulos: notification, consumers (WebSocket tiempo real)
- Auth: session/token validado al conectar
- Tecnología: Django 4.2 + Channels 4 + Daphne + Python 3.12

### service-worker
- Módulos: tareas async (mail, generación de reportes, ecologico, economico, equilibrio)
- Broker: Redis
- Tecnología: Celery 5.3 + Python 3.12

## Fases de migración

### Fase 1 — Infraestructura DevSecOps (este repo)
- Crear estructura de microservicios con Dockerfiles seguros.
- Pipeline CI Security completo (SAST, SCA, Trivy, secretos).
- Makefile local reproducible.
- Documentación base.

### Fase 2 — Extracción service-api (semanas 2-4)
- Mover app `api` de Django al servicio independiente.
- Configurar JWT authentication.
- Generar documentación OpenAPI.
- Tests de integración con service-web.

### Fase 3 — Extracción service-ws (semanas 4-6)
- Mover `notification` y `consumers` al servicio WebSocket.
- Configurar channel layer compartido con Redis.
- Tests de conexión anónima/autenticada.

### Fase 4 — Extracción service-worker (semanas 6-8)
- Mover tareas email y reportes a Celery.
- Configurar beat scheduler para tareas periódicas.
- Tests de tareas en CI con Redis mock.

### Fase 5 — Endurecimiento producción (semanas 8-12)
- TLS end-to-end (nginx + MinIO).
- Secrets management (GitHub Environments / Vault).
- DAST con OWASP ZAP sobre staging.
- Separar schemas de base de datos por servicio.

## Principios de la migración

- **Strangler Fig**: el monolito sigue funcionando mientras se extraen servicios.
- **Un PR por servicio**: cambios acotados a un servicio por pull request.
- **Contrato primero**: definir la API (OpenAPI) antes de implementar.
- **Sin estado en los servicios**: estado en DB, Redis o MinIO; no en memoria del proceso.
