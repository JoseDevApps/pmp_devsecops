# Inventario de Riesgos DevSecOps — PMP
Fecha: 2026-05-28 | Basado en: diagnostico-seguridad-django-2026-05-28.md

## Matriz de riesgos iniciales

| ID | Área | Riesgo | Evidencia | Severidad | Estado | Acción |
|---|---|---|---|---|---|---|
| H-01 | Secrets | Historial git con credenciales / .env | Repo PMP_2026 | Crítico | Pendiente | Rotar DB, SMTP, SECRET_KEY, MinIO keys |
| H-02 | CSRF | `@csrf_exempt` en views2.py | dashboard/views2.py | Crítico | Parcial | Eliminar o aislar views2.py completo |
| H-03 | AuthZ | Control de acceso por grupos no activo | middleware.py | Alto | Parcial | Activar ENFORCE_MODULE_GROUPS=1 |
| H-04 | WebSocket | Canales sin rate limit ni auditoría | consumers.py | Alto | Parcial | Implementar límites y logging |
| H-05 | HTTP/SSL | Hardening condicional por DEBUG | settings.py | Medio | Aplicado | Verificar en producción |
| H-06 | Backups | Archivos .sql en workspace | / raíz repo | Medio | Parcial | Mover a almacenamiento cifrado |
| H-07 | Runtime | Python 3.8 EOL en contenedores | Dockerfile | Medio | Pendiente | Migrar a Python 3.12 (este repo) |
| H-08 | DB | Migraciones no aplicadas al arrancar | docker-compose | Bajo | Pendiente | Automatizar en release pipeline |
| H-09 | Docker | Imagen corre como root | Dockerfile monolito | Alto | Aplicado | Todos los Dockerfiles de este repo usan non-root |
| H-10 | Secrets build | Credenciales en ARG/ENV Docker | Dockerfile monolito | Alto | Aplicado | BuildKit secrets o variables de runtime |

## Riesgos nuevos — arquitectura microservicios

| ID | Área | Riesgo | Severidad | Acción |
|---|---|---|---|---|
| M-01 | API Gateway | Nginx sin autenticación entre servicios | Alto | Autenticación interna (JWT o mTLS) |
| M-02 | Datos | Compartición de base de datos entre servicios | Medio | Definir esquemas separados por servicio |
| M-03 | Red | Puertos de servicios expuestos externamente | Alto | Solo nginx expuesto; servicios en red interna |
| M-04 | Secrets | Variables de entorno duplicadas por servicio | Medio | Gestión centralizada (Vault o GitHub Envs) |

## Acciones priorizadas — 30 días

1. Rotar todos los secretos (H-01): SECRET_KEY, DB password, MinIO keys, SMTP.
2. Eliminar `views2.py` del monolito o confirmarlo como no enrutado (H-02).
3. Activar `ENFORCE_MODULE_GROUPS=1` en staging (H-03).
4. Confirmar que solo el puerto 80 (nginx) sea público en docker-compose (M-03).
5. Ejecutar `make security` antes de cada PR.
