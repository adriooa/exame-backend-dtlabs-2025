from fastapi import status
from app.core.database.models import ServerModel
from app.main import app
from app.core.dependencies import get_current_user

def test_register_server_success(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"

    payload = {"server_name": "Dolly #1"}
    response = client.post("/servers", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert "server_ulid" in data
    assert data["server_name"] == "Dolly #1"

    server = db.query(ServerModel).filter(ServerModel.ulid == data["server_ulid"]).first()
    assert server is not None

    app.dependency_overrides.clear()


def test_register_server_missing_payload(client):
    app.dependency_overrides[get_current_user] = lambda: "username"

    payload = {}
    response = client.post("/servers", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    app.dependency_overrides.clear()

def test_register_server_invalid_payload(client):
    app.dependency_overrides[get_current_user] = lambda: "username"

    payload = {"server_name": 12345}
    response = client.post("/servers", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    app.dependency_overrides.clear()

def test_register_server_unauthorized(client):
    payload = {"server_name": "Dolly #1"}
    response = client.post("/servers", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED