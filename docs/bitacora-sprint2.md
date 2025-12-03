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