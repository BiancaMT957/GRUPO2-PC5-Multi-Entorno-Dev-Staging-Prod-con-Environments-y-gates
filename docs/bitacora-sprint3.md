# Issue 8 - Crear namespaces y manifiestos K8s para dev/staging/prod
## Descripcion
Crear infraestructura K8s separada por entorno.
## Que hacer
- Namespaces: catalog-dev, catalog-staging, catalog-prod.
- Deployment + Service por entorno.
- ConfigMap por entorno.

## Implementacion
En este issue prepararemos la aplicacion para que pueda ejecutarse en Kubernetes (K8s), el sistema mas usado en el mundo para ejecutar aplicaciones en la nube.
#### 1. Creamos namespaces
Cada uno representa un entorno distinto:
- `catalog-dev`: pruebas del desarrollador.
- `catalog-staging`: pruebas antes de produccion (prueba mas realista)
- `catalog-prod`: ambiente real del sistema (alta disponibilidad)
#### 2. Crear archivos (manifiestos) que definen como se ejecuta la app en Kubernetes
Los **manifiestos** enseñan a Kubernetes como correr la API. Para cada entorno se creo:
- `ConfigMap`: la configuracion del entorno.
- `Deployment`: como se ejecuta el contenedor (cuantas copias, que imagen usa)
- `Service`: hace la API accesible desde fuera del cluster.
#### 3. Para levantar la API en Kubernetes con un solo comando
El siguiente comando hace que Kubernetes levante automaticamente la API, configure el entorno, exponga el servicio y lo haga accesible.
```bash
# Primero creamos el namespace y luego lo demas
kubectl apply -f k8s/dev/namespace.yaml
kubectl apply -f k8s/dev
# Revisamos lo creado
kubectl get all -n catalog-dev
```

## Ejecucion
Construimos las imagenes de Docker
```bash
# 1) Construye la imagen base para dev
docker build -t catalog-api:dev .

# 2) Reusa la misma imagen para staging y prod
docker tag catalog-api:dev catalog-api:staging
docker tag catalog-api:dev catalog-api:prod

# 3) Comprobamos su existencia
docker images | grep catalog-api
```
Veremos la siguiente salida:
```bash
(venv) luis@LAPTOP-LC:/mnt/c/Users/Luis/Documents/GRUPO2-PC5-Multi-Entorno-Dev-Staging-Prod-con-Environments-y-gates$ docker images | grep catalog-api
catalog-api   dev       b61b57326a51   36 seconds ago   721MB
catalog-api   prod      b61b57326a51   36 seconds ago   721MB
catalog-api   staging   b61b57326a51   36 seconds ago   721MB
```

Creamos el cluster con **minikube**:
```bash
minikube start
# Verificamos, la existencia del nodo minikube
kubectl get nodes
```
Minikube tiene su propio Docker interno, asi que mandamos las imagenes:
```bash
minikube image load catalog-api:dev
minikube image load catalog-api:staging
minikube image load catalog-api:prod
```

Finalmente pasamos a la ejecucion para el entorno dev:
```bash
# Primero creamos el namespace
kubectl apply -f k8s/dev/namespace.yaml
# Luego el resto
kubectl apply -f k8s/dev/
# Verificamos
kubectl get all -n catalog-dev
```
Y probamos la API de dev, obteniendo la url del servicio con:
```bash
# 1) Obtenemos la URL del servicio
minikube service catalog-api -n catalog-dev --url
# 2) Probamos el endpoint
curl <url>/status
```
Finalmente repetimos los mismos pasos para `staging` y `prod`. Las salidas se adjuntan en `.evidence`.

# Issue 9 - Crear workflow deploy_env.yml con gates (dev → staging → prod)
## Descripcion
Pipeline completo con approvals y reglas de ambientes de GitHub.
## Que hacer
- Job: deploy_dev (auto).
- Job: deploy_staging (requiere approval).
- Job: deploy_prod (solo tags v*).
- Generar logs en .evidence/.
## Criterios de aceptacion
- Flujo completo: `push → dev → approval → staging → tag → prod`.
- Logs en `.evidence/deploy-log-*.txt`.
## Implementacion
### Gate 1: DEV > STAGING (enviroments + required reviewers en `staging`)
Primero haremos una breve configuracion en el repositorio:
1. Ir a **Settings** > **Enviroments** en el repositorio.
2. Crear un enviroment llamado `staging`.
3. Activar "**Required reviewers/Approvals**" para ese enviroment.
4. En el workflow, el job tiene:
    ```yaml
    needs: deploy_dev   # staging corre si dev fue exitoso
    environment:
        name: staging   # enviroment de GitHub
    ```
Con eso cuando el pipeline llega a `deploy staging`:
- GitHub detiene el job.
- Muestra un boton tipo "**Required reviewers/Approvals**".
- Hasta que alguien aprueba, **no se ejecuta** el deploy a staging.

### Gate 2: STAGING > PROD (solo se ejecuta `deploy_prod` si el push es un tag v*)`
```yaml
on:
  push:
    tags:
      - "v*"
...
if: startsWith(github.ref, 'refs/tags/v')
```
Flujo:
1. Se aprueba en `develop`.
2. Se despliega a dev y staging
3. El equipo valida staging
4. Cuando aprueban, crean un tag
```bash
git tag v1.0.0
git push origin v1.0.0
```
5. Ese push del tag v1.0.0 dispara solo el job deploy_prod.

### Logs en `.evidence/`
Cada job hace:
```bash
mkdir -p .evidence
echo "ENV=... TIME=... SHA=... REF=..." >> .evidence/deploy-log-<env>-<run>.txt
```
Se generan los archivos y se suben como artifacts en cada job.