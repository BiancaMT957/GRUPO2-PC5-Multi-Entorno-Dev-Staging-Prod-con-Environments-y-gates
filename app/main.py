from fastapi import FastAPI
from routers import services

app = FastAPI(title="Service Catalog API")


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(services.router)
