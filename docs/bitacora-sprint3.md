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