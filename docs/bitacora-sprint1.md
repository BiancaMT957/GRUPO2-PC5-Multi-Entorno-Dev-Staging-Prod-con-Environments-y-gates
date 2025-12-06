#  Bitácora — Issue 1: Implementación de endpoints básicos del Service Catalog API

##  Objetivo  
Crear la base del backend utilizando FastAPI e implementar los endpoints iniciales del Service Catalog: `/health`, `/services` y `/services/{id}`, utilizando datos mock en memoria.


##  Metodología

### **1. Creación de la estructura base del proyecto**
Se definió la estructura mínima recomendada para mantener orden y permitir escalabilidad:

```bash
project-root/
├── app/
│   ├── main.py
├── models/
│   ├── service.py
├── routers/
│   ├── services.py
```


---

### **2. Implementación del endpoint `/health`**
- Agregado en `main.py`.
- Permite validar la disponibilidad del servicio.
- Retorna:


```json
{ "status": "ok" }
```

3. Definición del modelo Service
En models/service.py se creó el modelo Pydantic:

```
class Service(BaseModel):
    id: int
    name: str
    description: str
Este modelo estandariza las respuestas del API.
```

4. Creación del router /services
En routers/services.py se desarrollaron:

Una lista mock de servicios en memoria.

Endpoints:

GET /services/ → retorna la lista mock.

GET /services/{id} → busca un servicio por ID.

Si existe → retorna el servicio.

Si no → responde 404 con mensaje "Service not found".

Se utilizó APIRouter para mantener modularidad y limpieza en el proyecto.

5. Registro del router en la aplicación principal
main.py integra el router con:

```
app.include_router(services.router)
```

Esto habilita todos los endpoints del módulo de servicios.

6. Pruebas manuales
Se ejecutó la aplicación con:

```
uvicorn app.main:app --reload
```


Validaciones realizadas:

/health → responde 200 correctamente.

/services → retorna lista mock esperada.

/services/{id}:

ID válido → retorna servicio.

ID inválido → retorna 404.

/docs → carga correctamente la documentación generada por FastAPI.


```
(venv) bianca007@MSI:/mnt/c/Users/Bianca/Documents/GRUPO2-PC5-Multi-Entorno-Dev-Staging-Prod-con-Environments-y-gates$ uvicorn app.main:app --reload
INFO:     Will watch for changes in these directories: ['/mnt/c/Users/Bianca/Documents/GRUPO2-PC5-Multi-Entorno-Dev-Staging-Prod-con-Environments-y-gates']   
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [9199] using StatReload
INFO:     Started server process [9201]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:42388 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:42404 - "GET /services HTTP/1.1" 307 Temporary Redirect
INFO:     127.0.0.1:42404 - "GET /services/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:42412 - "GET /services/1 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52842 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:52842 - "GET /openapi.json HTTP/1.1" 200 OK
```

# Issue 2 - Crear tests unitarios para los endpoints
## Objetivo
Crear pruebas unitarias usando pytest para validar los endpoints creados.
## Criterios
- Crear carpeta `tests/`.
- Tests para `/health`, `/services`, `/services/{id}`.
- Cubrir casos de exito y error.
## Implementacion
`TestClient` es una herramienta que simula un cliente HTTP, dentro de python. Luego se pasa la aplicacion FastAPI (`app`) para realizar `client.get()`, `client.post()` y otros. Sin la necesidad de levantar el servidor con `uvicorn`.
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
```
Luego implementamos tests para los siguientes casos:

| **Nombre del Test** | **Función Principal** |
|----------------------|------------------------|
| `test_health` | Verifica que el endpoint `/health` responde con codigo 200 y retorna exactamente `{"status": "ok"}`. |
| `test_services` | Comprueba que el endpoint `/services` devuelve una lista y responde correctamente (código 200). |
| `test_services_items` | Asegura que al menos un servicio existe y que cada item contiene los campos esenciales: `id`, `name`, `description`. |
| `test_get_service__id` | Valida que `/services/{id}` devuelve un servicio cuando se usa un ID válido, con la estructura correcta. |
| `test_get_service_invalid_id` | Revisa que el endpoint devuelva un código 404 y un mensaje de error cuando se solicita un ID inexistente. |

## Ejecucion
Para la ejecucion añadimos archivos `__init__.py` dentro de las carpetas `app`, `model` y `routers`, que convierten las carpetas en paquetes Python. Esto es muy util, ya que Python y Pytest pueden importar modulos correctamente.

Ejecutamos con el siguiente comando:
```bash 
# 80% de cobertura
pytest --cov=app --cov-fail-under=80 --cov-report=term-missing
```

# Issue 3 — Configurar pipeline CI (ci.yml)
## Objetivo

Implementar un pipeline de Integración Continua (CI) en GitHub Actions que ejecute automáticamente:

Linter (Ruff)

Formateador (Black)

Pruebas unitarias (pytest)

Esto garantiza que el código cumpla estándares de estilo y que los tests pasen antes de permitir un merge en la rama principal.

## Criterios de aceptación

Crear el archivo:
.github/workflows/ci.yml

El pipeline debe ejecutarse automáticamente en:

push a cualquier rama

pull_request hacia cualquier rama

Debe fallar si:

El código no está formateado correctamente (Black)

Hay errores de lint (Ruff)

Algún test falla (pytest)

En los videos del sprint debe verse:

Ejecución de Ruff, Black y pytest

El pipeline corriendo correctamente

## Implementación
1. Crear el archivo del workflow

Se agrega .github/workflows/ci.yml con el siguiente contenido:

name: CI

on:
  push:
    branches: ["*"]
  pull_request:
    branches: ["*"]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install black ruff pytest pytest-cov

      # Fix necesario para que Python encuentre la carpeta "app" en GitHub Actions
      - name: Fix Python path
        run: echo "PYTHONPATH=$PYTHONPATH:$(pwd)" >> $GITHUB_ENV

      - name: Run Ruff (linter)
        run: ruff check .

      - name: Run Black (code formatter check)
        run: black --check .

      - name: Run pytest
        run: pytest -q

## Qué valida cada herramienta
Herramienta	Función
Ruff	Revisa errores de estilo, calidad y buenas prácticas (alternativa moderna a flake8).
Black	Verifica que todo el código esté formateado correctamente.
pytest	Ejecuta los tests unitarios y falla si algún endpoint no funciona.
## Ejecución en GitHub Actions

Cada vez que se haga push o pull request, GitHub:

Instalará dependencias.

Correrá Ruff.

Correrá Black en modo --check.

Ejecutará pytest.

Aceptará o rechazará el PR según el resultado.

Esto asegura que solo se mergea código limpio y funcional.
