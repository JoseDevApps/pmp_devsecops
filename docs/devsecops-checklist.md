# Checklist DevSecOps — PMP
Referencia: OWASP DevSecOps Guideline + OWASP ASVS + diagnóstico 2026-05-28

## Controles activos en este repositorio

| Control | Herramienta | Trigger | Bloquea merge | Estado |
|---|---|---|---|---|
| Workflow lint | actionlint + zizmor | PR / push | Sí | Activo |
| Secret scanning | Gitleaks | PR / push | Sí | Activo |
| SAST Python | CodeQL | PR / push | Sí | Activo |
| SAST OWASP rules | Semgrep (p/django, p/owasp-top-ten) | PR / push | Sí | Activo |
| SCA dependencias | OSV Scanner | PR / push | Por severidad | Activo |
| SCA automático | Dependabot | Semanal | Alerts | Activo |
| Docker image scan | Trivy (CRITICAL+HIGH) | PR / push | Sí | Activo |
| SBOM | Docker Buildx | Release | Evidencia | Activo |
| Attestation/Provenance | GitHub Attest | Release | Evidencia | Activo |
| DAST ZAP | OWASP ZAP Baseline | Manual/staging | Por hallazgo | Manual |
| Branch protection | GitHub settings | Merge | Sí | Configurar |
| Environment approval | GitHub Environments | Deploy producción | Sí | Configurar |

## Controles pendientes de activación

| Control | Acción requerida | Prioridad |
|---|---|---|
| Branch protection en `main` | Configurar en Settings → Branches | Alta |
| Environment `production` con reviewers | Settings → Environments | Alta |
| Pin de acciones por SHA | Reemplazar tags por SHA en workflows | Media |
| OIDC hacia cloud | Configurar si se despliega en AWS/GCP/Azure | Media |
| DAST autenticado | Extender ZAP con login | Baja |

## Roadmap 30 / 60 / 90 días

### 0–30 días (controles mínimos)
- [x] Dockerfiles non-root para todos los servicios
- [x] Pipeline CI con Gitleaks, CodeQL, Semgrep, OSV, Trivy
- [x] Dependabot configurado
- [x] CODEOWNERS para rutas críticas
- [ ] Branch protection activado en `main`
- [ ] Rotar todos los secretos del monolito (H-01)
- [ ] Eliminar o aislar views2.py (H-02)
- [ ] Environment `production` con aprobación manual

### 31–60 días (controles robustos)
- [ ] SBOM en cada release
- [ ] Attestation de imagen en release
- [ ] DAST ZAP en staging (manual)
- [ ] Política formal de excepciones documentada
- [ ] Activar ENFORCE_MODULE_GROUPS=1 en producción (H-03)
- [ ] Rate limiting en WebSocket (H-04)
- [ ] Separar schemas DB por servicio

### 61–90 días (madurez avanzada)
- [ ] Pin de acciones por SHA en producción
- [ ] OIDC hacia cloud provider
- [ ] Métricas DevSecOps en dashboard
- [ ] Threat modeling revisado post-migración
- [ ] Auditoría OWASP SAMM trimestral
- [ ] TLS end-to-end MinIO (H-05 producción)
- [ ] Migrar backups SQL a almacenamiento cifrado (H-06)

## Métricas objetivo

| Métrica | Objetivo |
|---|---|
| Tiempo medio remediación críticas | < 7 días |
| PRs con todos los checks pasando | 100 % |
| Workflows con permisos mínimos | 100 % |
| Imágenes con non-root | 100 % |
| Releases con SBOM | 100 % |
| Secretos detectados en PR | 0 |
| CVEs críticos sin excepción | 0 |
