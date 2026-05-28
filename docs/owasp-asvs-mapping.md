# Mapeo OWASP ASVS — PMP DevSecOps
Versión ASVS: 4.0.3 | Nivel objetivo: L2

## V1 — Arquitectura, Diseño y Modelado de Amenazas

| Ref | Requisito | Estado | Notas |
|---|---|---|---|
| V1.1 | Documentación de arquitectura de seguridad | Parcial | Ver arquitectura-microservicios.md |
| V1.2 | Componentes de autenticación únicos y centralizados | Parcial | service-web gestiona auth; service-api usa JWT |
| V1.5 | Definición de límites de confianza | Pendiente | Definir mTLS o JWT entre servicios |

## V2 — Autenticación

| Ref | Requisito | Estado | Control |
|---|---|---|---|
| V2.1.1 | Contraseñas de mínimo 12 caracteres | Verificar | Django auth validators |
| V2.2.1 | Anti-automatización (rate limiting login) | Pendiente | Agregar django-axes |
| V2.3.1 | Tokens de sesión con suficiente entropía | Aplicado | Django SESSION_COOKIE_* seguro |
| V2.4.1 | Contraseñas hasheadas con algoritmo fuerte | Aplicado | Django usa PBKDF2 por defecto |

## V3 — Gestión de Sesiones

| Ref | Requisito | Estado | Control |
|---|---|---|---|
| V3.2.1 | Token generado en login | Aplicado | Django session framework |
| V3.2.3 | Cookie con Secure, HttpOnly, SameSite | Aplicado | settings.py hardened |
| V3.3.1 | Expiración de sesión por inactividad | Verificar | SESSION_COOKIE_AGE |
| V3.4.1 | Token CSRF en formularios POST | Aplicado | CsrfViewMiddleware activo |

## V4 — Control de Acceso

| Ref | Requisito | Estado | Control |
|---|---|---|---|
| V4.1.1 | Denegación por defecto | Aplicado | DashboardAuthMiddleware |
| V4.1.2 | Verificación de acceso en cada request | Aplicado | Middleware + @login_required |
| V4.2.1 | Protección contra IDOR | Pendiente | Revisar vistas API con objetos de usuario |
| V4.3.1 | Protección de funciones administrativas | Aplicado | /admin y /dashboard con middleware |

## V5 — Validación de Entradas

| Ref | Requisito | Estado | Control |
|---|---|---|---|
| V5.1.1 | Validación de todos los parámetros de entrada | Parcial | Django forms + DRF serializers |
| V5.3.1 | Codificación contextual de salida (XSS) | Aplicado | Django templates auto-escaping |
| V5.3.4 | Sin consultas SQL concatenadas | Verificar | Semgrep rule pmp-raw-sql-injection |

## V7 — Manejo de Errores y Logging

| Ref | Requisito | Estado | Control |
|---|---|---|---|
| V7.1.1 | Sin credenciales en logs | Pendiente | Auditar configuración de logging |
| V7.3.1 | Logs con timestamp y contexto | Pendiente | Configurar logging estructurado |
| V7.4.1 | Manejo de errores sin info sensible | Aplicado | DEBUG=0 en producción |

## V9 — Comunicaciones

| Ref | Requisito | Estado | Control |
|---|---|---|---|
| V9.1.1 | TLS para todas las comunicaciones | Parcial | Nginx con TLS (pendiente en producción) |
| V9.2.1 | Certificados válidos y actualizados | Pendiente | Configurar en despliegue |
| V9.3.1 | Rechazo de versiones TLS inseguras | Pendiente | Configurar en nginx.prod.conf |

## V10 — Código Malicioso

| Ref | Requisito | Estado | Control |
|---|---|---|---|
| V10.2.2 | Sin funcionalidades ocultas o backdoors | Verificar | CodeQL + Semgrep en CI |
| V10.3.1 | SBOM para componentes de terceros | Aplicado | Docker Buildx SBOM en release |
