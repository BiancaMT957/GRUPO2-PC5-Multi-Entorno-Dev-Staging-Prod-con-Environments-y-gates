import os
from fastapi import FastAPI
from routers import services

# lee entornos desde var entornos
APP_ENV = os.getenv("APP_ENV", "unknown")
app = FastAPI(title="Service Catalog API")


@app.get("/health")
def health():
    return {"status": "ok",
            "env": APP_ENV # indicador del entorno
    }


app.include_router(services.router)
