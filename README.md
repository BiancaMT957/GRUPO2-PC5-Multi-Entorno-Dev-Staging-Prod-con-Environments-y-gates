# Proyecto 2 — Multi-Entorno Dev/Staging/Prod con GitHub Environments & Gates

# Proyecto — Multi-Entorno Dev · Staging · Prod con GitHub Actions, Docker y Kubernetes

##  Descripción

Este proyecto implementa un pipeline completo de CI/CD utilizando:

- GitHub Actions  
- Entornos protegidos (Dev, Staging, Prod)  
- Deploy automatizado a Kubernetes (Minikube/kind)  
- Docker y Docker Compose para entorno local  
- Generación de SBOM y análisis de seguridad  
- Gates de aprobación por entorno  

La aplicación base es una API Python (Flask/FastAPI) contenida en `app/main.py` y desplegada en múltiples entornos mediante configuraciones en `k8s/<entorno>/`.

---

## 1️ Requisitos previos

Asegúrate de tener instalados:

```
docker --version
docker compose version
git --version
```

## 2 Clonar el repositorio


```
git clone https://github.com/BiancaMT957/GRUPO2-PC5-Multi-Entorno-Dev-Staging-Prod-con-Environments-y-gates.git
cd GRUPO2-PC5-Multi-Entorno-Dev-Staging-Prod-con-Environments-y-gates
```

## 3) Estructura del proyecto

.
├── evidence/
├── github/
├── docs/
├── app/
│   ├── main.py
│   └── __init__.py
├── models/
│   └── service.py
├── routers/
│   └── services.py
├── tests/
│   └── test_endpoints.py
├── k8s/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── docker-compose.dev.yml
├── Dockerfile
├── requirements.txt
├── Readme.md
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy_env.yml
│       └── build-scan-sbom.yml
Cada entorno contiene:

namespace.yaml

deployment.yaml

service.yaml

configmap.yaml

## Variables de entorno
Variable	Descripción	Entorno
APP_ENV	Nombre del entorno	dev / staging / prod
APP_NAME	Nombre del servicio	service-api
SERVICE_MESSAGE	Mensaje mostrado en /health	según entorno

Ejemplo de ConfigMap:

yaml
data:
  APP_ENV: "dev"
  SERVICE_MESSAGE: "Servicio ejecutándose en DEV"


## 4)Cómo levantar cada entorno
### Desarrollo

docker compose -f docker-compose.dev.yml up --build

###  Staging

docker compose -f docker-compose.staging.yml up --build

### Producción

docker compose -f docker-compose.prod.yml up --build -d

## 5)Comandos útiles
Ver logs

```
docker compose logs -f
```

Detener contenedores

```
docker compose down
```

Reconstruir sin usar caché

```
docker compose build --no-cache
```

## 6) Despliegue (Deploy)
Crear un tag


```
git tag -a v1.0.0 -m "Primera release"
git push origin v1.0.0
Ejecutar workflow manual
gh workflow run deploy-prod.yml
```
## 7) Verificación del entorno
Healthcheck

```
curl http://localhost:8000/health
```

## 8) Variables de entorno (creación y export)
Crear archivo .env

```
cp .env.example .env.dev
```

Exportar variable temporal

```
export APP_ENV=dev
```

## 9) CI: Integración Continua
El pipeline de CI se ejecuta en .github/workflows/ci.yml e incluye:

Linter ruff

Formateador black

Pruebas unitarias con pytest

Build temporal de imagen

Runners utilizados
GitHub-hosted runners
Se usan para:

Lint

Formateo

Tests

Build sin push

Self-hosted runner
Se usa cuando se requiere:

Docker real

Docker Compose

Deploy a Minikube/kind

kubectl apply

Construcción + push de imágenes

Ejemplo:

runs-on: self-hosted

## 10) CD: Deploy por entorno
Workflow: .github/workflows/deploy_env.yml

Branch	Entorno	Protección
dev	Dev	Sin aprobación
staging	Staging	Requiere aprobación
main	Prod	Aprobación obligatoria

## 11) Docker / Docker Compose
Levantar ambiente local:


```
docker compose -f docker-compose.dev.yml up --build
```


## 12) Kubernetes
Aplicar manifiestos de un entorno:


kubectl apply -f k8s/dev/
Estructura por entorno:

deployment

service

configmap

namespace


## 13)Seguridad y SBOM
El workflow build-scan-sbom.yml:

Genera SBOM (CycloneDX)

Escanea vulnerabilidades

Guarda resultados en .evidence/logs/

## 14) Evidencias del proyecto
Incluye:

Screenshots

Logs

Reportes SBOM

Evidencias de test

Ubicación:

.evidence/img/
.evidence/logs/



## 15)Ejecutar la API sin Docker


```
python3 app/main.py
```