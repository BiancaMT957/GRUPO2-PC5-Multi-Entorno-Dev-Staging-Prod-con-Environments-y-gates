import os
from fastapi import APIRouter, HTTPException
from models.service import Service

router = APIRouter(prefix="/services", tags=["Services"])

# Datos mock en memoria
mock_services = [
    Service(id=1, name="Compute Engine", description="Virtual machines"),
    Service(id=2, name="Cloud Storage", description="Object storage service"),
    Service(id=3, name="Kubernetes Engine", description="Managed Kubernetes clusters"),
]
APP_ENV = os.getenv("APP_ENV", "unknown")


@router.get("/")
def get_services():
    return {"env": APP_ENV, "services": mock_services}


@router.get("/{id}")
def get_service(id: int):
    for svc in mock_services:
        if svc.id == id:
            return {"env": APP_ENV, "service": svc}
    raise HTTPException(status_code=404, detail="Service not found")
