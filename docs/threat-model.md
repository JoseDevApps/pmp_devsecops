# Threat Model — PMP Microservices
Fecha: 2026-05-28 | Metodología: STRIDE

## Alcance

Sistema PMP en proceso de migración de monolito Django a microservicios.
Actores: usuarios autenticados, usuarios anónimos, administradores, procesos internos.

## Componentes en alcance

- Nginx (API Gateway público)
- service-web (Django, sesiones, dashboard)
- service-api (REST API, JWT)
- service-ws (WebSocket, notificaciones)
- service-worker (Celery, tareas async)
- PostgreSQL, Redis, MinIO

## Análisis STRIDE

### Spoofing (Suplantación de identidad)

| Amenaza | Componente | Mitigación |
|---|---|---|
| Token JWT falsificado | service-api | Validar firma con SECRET_KEY; expiración corta |
| Session cookie robada | service-web | Secure + HttpOnly + SameSite=Strict |
| Conexión WS sin autenticar | service-ws | Validar user en connect() |

### Tampering (Manipulación de datos)

| Amenaza | Componente | Mitigación |
|---|---|---|
| CSRF sobre endpoints POST | service-web | CsrfViewMiddleware activo; sin @csrf_exempt |
| Modificación de objeto ajeno (IDOR) | service-api | Filtrar queryset por request.user |
| Inyección SQL en parámetros | service-web/api | ORM Django; Semgrep rule activa |

### Repudiation (Repudio)

| Amenaza | Componente | Mitigación |
|---|---|---|
| Acciones sin trazabilidad | Todos | Logging estructurado con user + timestamp |
| Pipeline sin evidencia | CI/CD | SARIF + artefactos en GitHub Actions |

### Information Disclosure (Divulgación de información)

| Amenaza | Componente | Mitigación |
|---|---|---|
| DEBUG=True en producción | service-web | DEBUG controlado por ENV; Semgrep rule |
| Secretos en historial git | Repo | Gitleaks en CI; rotar credenciales H-01 |
| Backups SQL expuestos | Filesystem | .gitignore; mover a almacenamiento cifrado H-06 |
| URLs prefirmadas MinIO largas | MinIO | Usar expiración corta (3600s max) |

### Denial of Service (Denegación de servicio)

| Amenaza | Componente | Mitigación |
|---|---|---|
| Flood de conexiones WebSocket | service-ws | Rate limiting pendiente (H-04) |
| Tareas Celery sin límite | service-worker | Configurar rate_limit en tasks |
| Archivos grandes en upload | MinIO | client_max_body_size en nginx |

### Elevation of Privilege (Escalada de privilegios)

| Amenaza | Componente | Mitigación |
|---|---|---|
| Acceso a /dashboard sin grupo | service-web | DashboardAuthMiddleware + ENFORCE_MODULE_GROUPS |
| Contenedor como root | Todos | USER non-root en Dockerfiles |
| Acción GitHub con write-all | CI/CD | Permisos mínimos por job en workflows |

## Revisión recomendada

- Revisar este documento cada trimestre o tras cambio arquitectural significativo.
- Actualizar estados de mitigación conforme avance el roadmap.
