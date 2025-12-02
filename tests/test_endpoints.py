from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# Retorna 200 y msj de status
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# Retorna 200 y lista de endpoints
def test_services():
    response = client.get("/services")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# check items basicos: id, name, description
def test_services_items():
    response = client.get("/services")
    assert response.status_code == 200

    data = response.json()
    # Si no hay servicios, este test fallara
    assert len(data) > 0

    first = data[0]
    assert "id" in first
    assert "name" in first
    assert "description" in first

# verifica id valido
def test_get_service_id():
    valid_id = 1  # ajustar al valor del mock
    response = client.get(f"/services/{valid_id}")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == valid_id

# id invalido
def test_get_service_invalid_id():
    invalid_id = 9999
    response = client.get(f"/services/{invalid_id}")
    assert response.status_code == 404

    data = response.json()
    assert "detail" in data or "message" in data