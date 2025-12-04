# tests/test_endpoints.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_status_code():
    """/status debe existir y devolver 200."""
    response = client.get("/status")
    assert response.status_code == 200


def test_status_body():
    """El body debe contener 'service' y 'environment' con tipos esperados."""
    response = client.get("/status")
    assert response.status_code == 200

    data = response.json()
    assert "service" in data
    assert data["service"] == "fake-api"

    assert "environment" in data
    assert isinstance(data["environment"], str)


def test_status_header_environment():
    """El middleware debe añadir el header 'X-Environment' y coincidir con el campo environment del body."""
    response = client.get("/status")
    assert response.status_code == 200

    data = response.json()
    # Header presente
    assert "X-Environment" in response.headers

    # Valor del header debe coincidir con el campo environment del body
    assert response.headers["X-Environment"] == data["environment"]
