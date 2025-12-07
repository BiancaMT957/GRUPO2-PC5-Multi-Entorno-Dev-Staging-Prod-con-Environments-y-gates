## app/main.py
import os
from fastapi import FastAPI, Request

app = FastAPI()

# Leer APP_ENV, si no existe, usar "dev" por defecto
APP_ENV = os.getenv("APP_ENV", "dev")


@app.middleware("http")
async def add_env_header(request: Request, call_next):
    # Añadir un header X-Environment a todas las respuestas
    response = await call_next(request)
    response.headers["X-Environment"] = APP_ENV
    return response


@app.get("/status")
def status():
    # Respuesta visible por HTTP
    return {"service": "fake-api", "environment": APP_ENV}
