# Proyecto 2 — Multi-Entorno Dev/Staging/Prod con GitHub Environments & Gates

API interna desarrollada con Python + FastAPI, diseñada para funcionar en tres entornos (dev, staging, prod) con despliegues controlados mediante pipelines DevSecOps, escaneo de seguridad y un flujo CI/CD con aprobaciones.

# Características principales
## Endpoints Sprint 1

GET /health → estado del servicio

GET /services → lista de servicios mock en memoria

GET /services/{id} → detalle de un servicio o 404

## Arquitectura del proyecto

FastAPI modular (routers / models / main)

Tests unitarios con pytest

Integración continua: ci.yml (lint + tests en PR)

## Sprint 2

Dockerfile seguro (slim, non-root, healthcheck)

docker-compose.dev.yml

Configuraciones por entorno vía variables de entorno

API responde incluyendo el entorno actual (dev/staging/prod)

build_scan_sbom.yml → genera SBOM y ejecuta Trivy/Grype

Evidencia en .evidence/

## Sprint 3

Despliegue multi-entorno en Kubernetes

Namespaces:

catalog-dev

catalog-staging

catalog-prod

Manifests por entorno con ConfigMaps + réplicas diferentes

Pipeline deploy_env.yml con gates:

Dev → despliegue automático

Staging → requiere aprobación

Prod → solo en tags v* + aprobación

## Estructura del proyecto (simplificada)
app/
 ├── main.py
 ├── routers/
 │    └── services.py
 ├── models/
 │    └── service.py
tests/
 .evidence/
Dockerfile
docker-compose.dev.yml
.github/workflows/
 ├── ci.yml
 ├── build_scan_sbom.yml
 └── deploy_env.yml

# Cómo ejecutar el proyecto localmente
### Instalar dependencias
pip install -r requirements.txt

### Ejecutar FastAPI con Uvicorn
uvicorn app.main:app --reload

### Abrir documentación interactiva

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

## Ejecutar con Docker (modo dev)
docker compose -f docker-compose.dev.yml up --build


El endpoint debe devolverte algo como:

{
  "environment": "dev",
  "services": [...]
}
## Seguridad y Evidencias

Este proyecto implementa prácticas DevSecOps:

Análisis de vulnerabilidades con Trivy y Grype

Generación de SBOM (Syft)

Archivos almacenados en .evidence/

## CI/CD (Resumen de pipelines)
ci.yml

Ejecutado en cada Pull Request

Corre lint + tests

build_scan_sbom.yml

Construye imagen

Escanea vulnerabilidades

Genera SBOM → .evidence/sbom.json

deploy_env.yml

dev → automático

staging → requiere aprobación manual

prod → solo tags v* + aprobación