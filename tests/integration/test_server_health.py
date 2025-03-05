from fastapi import status
from datetime import datetime, timedelta
import pytz

# Importe os modelos do banco de dados
from app.core.database.models import ServerModel, SensorDataModel
from app.main import app
from app.core.dependencies import get_current_user

def test_get_all_servers_health_success(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"

    server1 = ServerModel(
        ulid="ulid1",
        name="Server 1",
        last_update=datetime.now(pytz.UTC) 
    )
    server2 = ServerModel(
        ulid="ulid2",
        name="Server 2",
        last_update=datetime.now(pytz.UTC) - timedelta(seconds=20) 
    )
    db.add_all([server1, server2])
    db.commit()

    response = client.get("/health/all")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert "servers" in data
    assert isinstance(data["servers"], list)
    assert len(data["servers"]) == 2

    server1_data = next((s for s in data["servers"] if s["server_ulid"] == "ulid1"), None)
    server2_data = next((s for s in data["servers"] if s["server_ulid"] == "ulid2"), None)

    assert server1_data is not None
    assert server2_data is not None
    assert server1_data["server_name"] == "Server 1"
    assert server1_data["status"] == "online"
    assert server2_data["server_name"] == "Server 2"
    assert server2_data["status"] == "offline"

    app.dependency_overrides.clear()


def test_get_all_servers_health_no_servers(client):
    app.dependency_overrides[get_current_user] = lambda: "username"

    response = client.get("/health/all")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "servers" in data
    assert isinstance(data["servers"], list)
    assert len(data["servers"]) == 0

    app.dependency_overrides.clear()


def test_get_all_servers_health_unauthorized(client):
    response = client.get("/health/all")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_server_health_success(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"

    server = ServerModel(
        ulid="ulid1",
        name="Server 1",
        last_update=datetime.now(pytz.UTC)
    )
    db.add(server)
    db.commit()

    response = client.get("/health/ulid1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["server_ulid"] == "ulid1"
    assert data["server_name"] == "Server 1"
    assert data["status"] == "online"

    app.dependency_overrides.clear()


def test_get_server_health_offline(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"

    server = ServerModel(
        ulid="ulid2",
        name="Server 2",
        last_update=datetime.now(pytz.UTC) - timedelta(seconds=20)
    )
    db.add(server)
    db.commit()

    response = client.get("/health/ulid2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["server_ulid"] == "ulid2"
    assert data["server_name"] == "Server 2"
    assert data["status"] == "offline"

    app.dependency_overrides.clear()


def test_get_server_health_not_found(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"

    response = client.get("/health/invalid_ulid")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Server not found"}

    app.dependency_overrides.clear()


def test_get_server_health_no_sensor_data(client, db):
    """Se o servidor não possui last_update (nenhum dado enviado), ele deve ser considerado offline."""
    app.dependency_overrides[get_current_user] = lambda: "username"

    server = ServerModel(
        ulid="ulid3",
        name="Server 3",
        last_update=None 
    )
    db.add(server)
    db.commit()

    response = client.get("/health/ulid3")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["server_ulid"] == "ulid3"
    assert data["server_name"] == "Server 3"
    assert data["status"] == "offline"  

    app.dependency_overrides.clear()


def test_get_server_health_unauthorized(client):
    response = client.get("/health/ulid1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
