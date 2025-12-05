# Issue 4 - Crear Dockerfile endurecido para la API
## Objetivo
Crear un Dockerfile slim, seguro y funcional para la API.
## Criterios
- Base python:*-slim.
- Crear usuario no root.
- Añadir HEALTHCHECK.
- Ejecutar FastAPI con uvicorn.
## Implementacion
- Usamos una imagen slim fija de python, menos peso.
    ```Dockerfile
    FROM python:3.12-slim
    ```
- Creamos un usuario no root
    ```Dockerfile
    RUN groupadd -g 1001 appuser \
    && useradd -u 1001 -g appuser -s /usr/sbin/nologin -m appuser

    RUN chown -R appuser:appuser /app
    USER appuser
    ```
- Añadimos HEALTHCHECK para marcar el contenedor como `healthy`/`unhealthy` segun la API, instalamos curl para poder llamar a `\health` desde el contenedor:
    ```Dockerfile
    RUN apt-get update \
        && apt-get install -y --no-install-recommends curl \
        && rm -rf /var/lib/apt/lists/*

    HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
        CMD curl -f http://localhost:8000/health || exit 1
    ```  
- Ejecutamos la FastAPI con uvicorn, escucha todas las interfaces del contenedor en el puerto 8080.
    ```Dockerfile
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```

# Issue 5 - Crear docker-compose.dev.yml con APP_ENV=dev
## Objetivo
Crear un archivo Compose exclusivo para entorno de desarrollo.
## Criterios
- Servicio API con `APP_ENV=dev`.
- Exponer puerto local.
- Añadir variable que permita mostrar el entorno en la respuesta.
## Implementacion
Creamos el archivo `docker-compose.dev.yml` que define como debe levantarse la API en un entorno de desarrollo usando Docker Compose.
- `version: "3.9"`: version de Docker Compose
- `services`: contiene servicios/containers que se van a levantar
- `api`: nombre del servicio
- `build`: indica como construir la imagen
    ```yaml
    build:
        context: .  # Carpeta actual para build
        dockerfile: Dockerfile  # Dockerfile como receta
    ```
- `container_name: api-dev`: nombre personalizado del contenedor en ejecucion
- `enviroment`: define variables de entorno en el contenedor
- `ports`: expone el puerto del contenedor, luego para acceder:
    ```arduino
    http://localhost:8000
    ```
- `command`: sobreescribe el comando por defecto
    ```yaml
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ```
    - Levanta FastAPI con Uvicorn
    - Escucha en todas las interfaces del contenedor (0.0.0.0)
    - Usa el puerto 8080
    - `--reload` detecta cambios de codigo y reinicia automaticamente.

## Ejecucion
Ejecutamos usando el siguiente comando:
```bash
docker compose -f docker-compose.dev.yml up --build
```

# **Issue 6 — Implementar configuración por entorno (dev/staging/prod)**

##  Objetivo
Configurar la API para detectar automáticamente el entorno de ejecución (`APP_ENV`) y exponerlo mediante un endpoint y un header HTTP dinámico.  
Esto permitirá verificar desde cualquier cliente (navegador, Postman, curl) si la API está corriendo en **dev**, **staging** o **prod**.

---

##  Criterios de Aceptación

- La API debe leer la variable de entorno `APP_ENV`.
- Debe soportar los tres entornos:
  - `dev`
  - `staging`
  - `prod`
- La API debe devolver un valor distinto dependiendo del entorno.
- Debe existir un endpoint para verificar el entorno actual.
- **Todas las respuestas HTTP deben incluir el header:**

X-Environment: <env>


---

##  Implementación

### **1. Lectura del entorno**
Se usa:
```python
APP_ENV = os.getenv("APP_ENV", "dev")
```

Esto garantiza que si la variable no existe, se use automáticamente el entorno dev.


### **2. Middleware para Header Dinámico**
Un middleware agrega el header X-Environment en todas las respuestas HTTP.

### **3. Endpoints /status**

Expone la información del entorno en formato JSON.

## Verificación desde HTTP

### **1. Navegador o Postman**
Ir a:

http://localhost:8080/status


Respuesta esperada:

{
  "service": "fake-api",
  "environment": "dev"
}

### **2. Verificar Headers**

Debe aparecer:

X-Environment: dev

## Ejecución por entorno
### Modo dev
APP_ENV=dev uvicorn app.main:app --reload --port 8080

### Modo staging
APP_ENV=staging uvicorn app.main:app --reload --port 8080

### Modo prod
APP_ENV=prod uvicorn app.main:app --reload --port 8080

## Test rápido con curl
curl -i http://localhost:8080/status

## Debe mostrar:

X-Environment: dev

Seguido del JSON con el nombre del entorno.

# **Issue 7 — Crear pipeline build_scan_sbom.yml para build, scan y SBOM**

## Objetivo

Crear un pipeline automatizado en GitHub Actions que construya la imagen Docker, escanee vulnerabilidades críticas y genere un archivo SBOM.
Todo debe ser ejecutado en cada push y pull request hacia main y develop.

## Criterios de aceptación

Se ejecuta automáticamente en:

* push a main y develop

* pull request a main y develop

* Construye la imagen Docker del proyecto.

* Ejecuta escaneo de vulnerabilidades con Trivy.

* El pipeline falla si Trivy encuentra vulnerabilidades HIGH o CRITICAL.

* Genera un archivo SBOM usando Syft.

* El archivo SBOM debe guardarse en: .evidence/sbom.json

* Debe quedar visible en GitHub Actions para mostrarlo en el sprint.

## Implementación

Creamos el archivo:

.github/workflows/build_scan_sbom.yml


Este pipeline define todas las etapas necesarias para validar seguridad y generar un SBOM del proyecto.

## Ejecución

El pipeline NO se ejecuta manualmente.
Se activa automáticamente cuando:

* Haces push:
git push origin develop


o

git push origin main

* Creas un Pull Request hacia:

main

develop

GitHub Actions comenzará a correr el workflow.

### Qué debe aparecer en GitHub Actions

Si todo está bien:

✔ Checkout repository
✔ Crear carpeta .evidence
✔ Build Docker image
✔ Instalar Trivy
✔ Ejecutar Trivy Scan
✔ Instalar Syft
✔ Generar archivo SBOM
✔ Subir SBOM como artifact

SUCCESS


El archivo generado estará disponible como:

 Artifact: sbom
 Contenido: .evidence/sbom.json

## Cuando debe fallar

El pipeline se detendrá si Trivy detecta:

* HIGH

* CRITICAL

Y verás algo así:

CRITICAL vulnerability found
Error: Process completed with exit code 1.
