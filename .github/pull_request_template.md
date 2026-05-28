## Descripción

<!-- Qué cambia y por qué -->

## Tipo de cambio

- [ ] Bugfix
- [ ] Nueva funcionalidad
- [ ] Refactoring
- [ ] Infraestructura / CI-CD
- [ ] Seguridad

---

## Checklist DevSecOps

### Código
- [ ] Cambios revisados por al menos una persona.
- [ ] No se introducen secretos ni credenciales en el código.
- [ ] Tests unitarios / integración pasan en CI.
- [ ] Documentación actualizada si aplica.

### Seguridad OWASP
- [ ] No se rompe control de acceso (A01 — Broken Access Control).
- [ ] No se agregan consultas sin parámetros seguros (A03 — Injection).
- [ ] No se exponen errores con información sensible (A05 — Security Misconfiguration).
- [ ] Dependencias nuevas tienen justificación (A06 — Vulnerable Components).
- [ ] No se registran datos sensibles en logs (A09 — Logging Failures).
- [ ] Se mantiene protección CSRF en todas las vistas activas.
- [ ] No se usa `@csrf_exempt` sin justificación documentada.

### Docker
- [ ] Imagen corre como usuario non-root (`USER appuser`).
- [ ] No se copiaron `.env`, llaves ni secretos en la imagen.
- [ ] Build multi-stage aplicado.
- [ ] `.dockerignore` correcto en el servicio.
- [ ] Imagen escaneada sin CVEs críticos bloqueantes (Trivy).

### GitHub Actions
- [ ] No se agregaron permisos innecesarios al workflow.
- [ ] No se usó `pull_request_target` sin revisión explícita.
- [ ] Acciones de terceros verificadas.
- [ ] No se imprime ningún secreto en logs.

### Microservicios — migración PMP
- [ ] El cambio está acotado al servicio correspondiente (web / api / ws / worker).
- [ ] La comunicación entre servicios usa la interfaz definida (REST / WebSocket).
- [ ] Variables de entorno nuevas están documentadas en `.env.example`.
