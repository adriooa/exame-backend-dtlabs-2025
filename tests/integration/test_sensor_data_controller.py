from fastapi import status
from app.main import app  
from app.core.dependencies import get_current_user  # Import the get_current_user function
from app.domain.dtos.sensor_data_dto import SensorDataDTO
from app.core.database.models import SensorDataModel, ServerModel
from datetime import datetime, timezone


def test_register_sensor_data_success(client, db, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}

    server_ulid = "01JMG0J6BH9JV08PKJD5GSRM84"
    server = ServerModel(ulid=server_ulid, name="Test Server", status="online")
    db.add(server)
    db.commit()

    mock_entity = SensorDataModel(
        id=1,
        server_ulid=server_ulid,
        timestamp=datetime(2024, 2, 19, 12, 34, 56, tzinfo=timezone.utc),
        temperature=25.5,
        humidity=60.2,
    )
    payload = {
        "server_ulid": server_ulid,
        "timestamp": "2024-02-19T12:34:56Z",
        "temperature": 25.5,
        "humidity": 60.2,
    }

    response = client.post("/data", json=payload, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED

    expected_response = SensorDataDTO.from_orm(mock_entity).dict()
    expected_response["timestamp"] = expected_response["timestamp"].isoformat(
    ).replace("+00:00", "")
    assert response.json() == expected_response


def test_register_sensor_data_fail_server_not_found(client):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "01JMG0J6BH9JV08PKJD5GSRM84"

    payload = {
        "server_ulid": server_ulid,
        "timestamp": "2024-02-19T12:34:56Z",
        "temperature": 25.5,
        "humidity": 60.2,
    }

    response = client.post("/data", json=payload)

    assert response.status_code in [
        status.HTTP_404_NOT_FOUND, status.HTTP_400_BAD_REQUEST]
    
    app.dependency_overrides.clear()
    


def test_register_sensor_data_fail_missing_fields(client):
    app.dependency_overrides[get_current_user] = lambda: "username"
    payload = {
        "server_ulid": "01JMG0J6BH9JV08PKJD5GSRM84",
        # "timestamp" ausente
        "temperature": 25.5,
        # "humidity" ausente
    }

    response = client.post("/data", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    app.dependency_overrides.clear()


def test_register_sensor_data_fail_invalid_timestamp(client):
    app.dependency_overrides[get_current_user] = lambda: "username"
    payload = {
        "server_ulid": "01JMG0J6BH9JV08PKJD5GSRM84",
        "timestamp": "data-inválida",
        "temperature": 25.5,
        "humidity": 60.2,
    }

    response = client.post("/data", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    app.dependency_overrides.clear()


def test_register_sensor_data_fail_invalid_temperature(client):
    app.dependency_overrides[get_current_user] = lambda: "username"
    payload = {
        "server_ulid": "01JMG0J6BH9JV08PKJD5GSRM84",
        "timestamp": "2024-02-19T12:34:56Z",
        "temperature": -200,
        "humidity": 99999,
    }

    response = client.post("/data", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    app.dependency_overrides.clear()


def test_register_sensor_data_idempotence(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "01JMG0J6BH9JV08PKJD5GSRM84"
    server = ServerModel(ulid=server_ulid, name="Test Server", status="online")
    db.add(server)
    db.commit()

    payload = {
        "server_ulid": server_ulid,
        "timestamp": "2024-02-19T12:34:56Z",
        "temperature": 25.5,
        "humidity": 60.2,
    }

    response1 = client.post("/data", json=payload)
    response2 = client.post("/data", json=payload)

    assert response1.status_code == status.HTTP_201_CREATED
    assert response2.status_code in [
        status.HTTP_201_CREATED, status.HTTP_409_CONFLICT]
    
    app.dependency_overrides.clear()
