from datetime import datetime, timedelta, timezone
from fastapi import status
from app.core.database.models import SensorDataModel, ServerModel
from app.main import app
from app.core.dependencies import get_current_user


def test_get_sensor_data_without_aggregation(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server123"
    server = ServerModel(ulid=server_ulid, name="Test Server")
    db.add(server)
    db.commit()

    sensor1 = SensorDataModel(
        server_ulid=server_ulid,
        timestamp=datetime(2024, 2, 19, 12, 34, 0, tzinfo=timezone.utc),
        temperature=25.3,
        humidity=None,
        voltage=None,
        current=None
    )
    sensor2 = SensorDataModel(
        server_ulid=server_ulid,
        timestamp=datetime(2024, 2, 19, 12, 35, 0, tzinfo=timezone.utc),
        temperature=24.9,
        humidity=None,
        voltage=None,
        current=None
    )
    db.add(sensor1)
    db.add(sensor2)
    db.commit()

    params = {
        "server_ulid": server_ulid,
        "start_time": "2024-02-19T12:33:00Z",
        "end_time": "2024-02-19T12:36:00Z"
    }
    response = client.get("/data", params=params)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["temperature"] == 25.3
    assert data[1]["temperature"] == 24.9
    app.dependency_overrides.clear()

def test_get_sensor_data_with_aggregation_minute(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server_agg_minute"
    server = ServerModel(ulid=server_ulid, name="Server Minute")
    db.add(server)
    db.commit()

    ts_base = datetime(2024, 2, 19, 12, 34, 0, tzinfo=timezone.utc)
    sensor1 = SensorDataModel(
        server_ulid=server_ulid,
        timestamp=ts_base,
        temperature=25.0,
        humidity=None,
        voltage=None,
        current=None
    )
    sensor2 = SensorDataModel(
        server_ulid=server_ulid,
        timestamp=ts_base + timedelta(seconds=30),
        temperature=27.0,
        humidity=None,
        voltage=None,
        current=None
    )
    db.add(sensor1)
    db.add(sensor2)
    db.commit()

    params = {
        "server_ulid": server_ulid,
        "start_time": "2024-02-19T12:33:00Z",
        "end_time": "2024-02-19T12:36:00Z",
        "sensor_type": "temperature",
        "aggregation": "minute"
    }
    response = client.get("/data", params=params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["temperature"] == 26.0
    app.dependency_overrides.clear()

def test_get_sensor_data_with_aggregation_hour(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server_agg_hour"
    server = ServerModel(ulid=server_ulid, name="Server Hour")
    db.add(server)
    db.commit()

    ts1 = datetime(2024, 2, 19, 14, 10, 0, tzinfo=timezone.utc)
    ts2 = datetime(2024, 2, 19, 14, 45, 0, tzinfo=timezone.utc)
    sensor1 = SensorDataModel(
        server_ulid=server_ulid,
        timestamp=ts1,
        humidity=60.0,
        temperature=None,
        voltage=None,
        current=None
    )
    sensor2 = SensorDataModel(
        server_ulid=server_ulid,
        timestamp=ts2,
        humidity=62.0,
        temperature=None,
        voltage=None,
        current=None
    )
    db.add(sensor1)
    db.add(sensor2)
    db.commit()

    params = {
        "server_ulid": server_ulid,
        "start_time": "2024-02-19T14:00:00Z",
        "end_time": "2024-02-19T15:00:00Z",
        "sensor_type": "humidity",
        "aggregation": "hour"
    }
    response = client.get("/data", params=params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["humidity"] == 61.0
    app.dependency_overrides.clear()

def test_get_sensor_data_no_results(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server_no_data"

    params = {
        "server_ulid": server_ulid,
        "start_time": "2024-02-19T00:00:00Z",
        "end_time": "2024-02-19T23:59:59Z"
    }
    response = client.get("/data", params=params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
    app.dependency_overrides.clear()

def test_get_sensor_data_multiple_servers_without_aggregation(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server1_ulid = "server1"
    server2_ulid = "server2"
    
    server1 = ServerModel(ulid=server1_ulid, name="Server 1")
    server2 = ServerModel(ulid=server2_ulid, name="Server 2")
    db.add(server1)
    db.add(server2)
    db.commit()

    sensor1 = SensorDataModel(
        server_ulid=server1_ulid,
        timestamp=datetime(2024, 2, 19, 10, 0, 0, tzinfo=timezone.utc),
        temperature=23.0
    )
    sensor2 = SensorDataModel(
        server_ulid=server1_ulid,
        timestamp=datetime(2024, 2, 19, 10, 5, 0, tzinfo=timezone.utc),
        temperature=24.0
    )
    sensor3 = SensorDataModel(
        server_ulid=server2_ulid,
        timestamp=datetime(2024, 2, 19, 11, 0, 0, tzinfo=timezone.utc),
        temperature=22.0
    )
    db.add_all([sensor1, sensor2, sensor3])
    db.commit()

    params = {
        "server_ulid": server1_ulid,
        "start_time": "2024-02-19T09:00:00Z",
        "end_time": "2024-02-19T11:00:00Z"
    }
    response = client.get("/data", params=params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["temperature"] == 23.0
    assert data[1]["temperature"] == 24.0
    app.dependency_overrides.clear()

def test_get_sensor_data_multiple_servers_with_aggregation(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server1_ulid = "serverA"
    server2_ulid = "serverB"
    
    server1 = ServerModel(ulid=server1_ulid, name="Server A")
    server2 = ServerModel(ulid=server2_ulid, name="Server B")
    db.add(server1)
    db.add(server2)
    db.commit()

    ts_base = datetime(2024, 2, 19, 12, 0, 0, tzinfo=timezone.utc)
    sensor1 = SensorDataModel(
        server_ulid=server1_ulid,
        timestamp=ts_base,
        temperature=20.0
    )
    sensor2 = SensorDataModel(
        server_ulid=server1_ulid,
        timestamp=ts_base + timedelta(seconds=30),
        temperature=22.0
    )

    sensor3 = SensorDataModel(
        server_ulid=server2_ulid,
        timestamp=datetime(2024, 2, 19, 12, 5, 0, tzinfo=timezone.utc),
        temperature=25.0
    )
    db.add_all([sensor1, sensor2, sensor3])
    db.commit()

    params = {
        "server_ulid": server1_ulid,
        "start_time": "2024-02-19T11:55:00Z",
        "end_time": "2024-02-19T12:05:00Z",
        "sensor_type": "temperature",
        "aggregation": "minute"
    }
    response = client.get("/data", params=params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["temperature"] == 21.0
    app.dependency_overrides.clear()


def test_get_sensor_data_without_aggregation_sensor_type(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server123"
    server = ServerModel(ulid=server_ulid, name="Test Server")
    db.add(server)
    db.commit()

    sensor1 = SensorDataModel(
        server_ulid=server_ulid,
        timestamp=datetime(2024, 2, 19, 12, 34, 0, tzinfo=timezone.utc),
        temperature=25.3,
        humidity=55.0,
        voltage=None,
        current=None
    )
    sensor2 = SensorDataModel(
        server_ulid=server_ulid,
        timestamp=datetime(2024, 2, 19, 12, 35, 0, tzinfo=timezone.utc),
        temperature=24.9,
        humidity=54.5,
        voltage=None,
        current=None
    )
    db.add(sensor1)
    db.add(sensor2)
    db.commit()

    params = {
        "server_ulid": server_ulid,
        "start_time": "2024-02-19T12:33:00Z",
        "end_time": "2024-02-19T12:36:00Z",
        "sensor_type": "temperature"
    }
    response = client.get("/data", params=params)
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    for record in data:
        assert "timestamp" in record
        assert "temperature" in record
        assert "humidity" not in record
        assert "voltage" not in record
        assert "current" not in record
        assert "id" not in record
    app.dependency_overrides.clear()


def test_get_sensor_data_with_aggregation_sensor_type(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server_agg"
    server = ServerModel(ulid=server_ulid, name="Server Aggregation")
    db.add(server)
    db.commit()

    ts_base = datetime(2024, 2, 19, 12, 0, 0, tzinfo=timezone.utc)
    sensor1 = SensorDataModel(
        server_ulid=server_ulid,
        timestamp=ts_base,
        temperature=20.0,
        humidity=None,
        voltage=None,
        current=None
    )
    sensor2 = SensorDataModel(
        server_ulid=server_ulid,
        timestamp=ts_base + timedelta(seconds=30),
        temperature=22.0,
        humidity=None,
        voltage=None,
        current=None
    )
    db.add(sensor1)
    db.add(sensor2)
    db.commit()

    params = {
        "server_ulid": server_ulid,
        "start_time": "2024-02-19T11:55:00Z",
        "end_time": "2024-02-19T12:05:00Z",
        "sensor_type": "temperature",
        "aggregation": "minute"
    }
    response = client.get("/data", params=params)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1

    record = data[0]
    assert "timestamp" in record
    assert "temperature" in record

    assert record["temperature"] == 21.0

    assert "humidity" not in record
    assert "voltage" not in record
    assert "current" not in record
    assert "id" not in record
    app.dependency_overrides.clear()

def test_get_sensor_data_invalid_aggregation(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server_invalid_agg"
    server = ServerModel(ulid=server_ulid, name="Invalid Agg Server")
    db.add(server)
    db.commit()

    params = {
        "server_ulid": server_ulid,
        "start_time": "2024-02-19T12:00:00Z",
        "end_time": "2024-02-19T13:00:00Z",
        "aggregation": "invalid_value"
    }
    response = client.get("/data", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    app.dependency_overrides.clear()

def test_get_sensor_data_invalid_sensor_type(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server_invalid_sensor"
    server = ServerModel(ulid=server_ulid, name="Invalid Sensor Server")
    db.add(server)
    db.commit()

    params = {
        "server_ulid": server_ulid,
        "start_time": "2024-02-19T12:00:00Z",
        "end_time": "2024-02-19T13:00:00Z",
        "sensor_type": "invalid_sensor"
    }
    response = client.get("/data", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    app.dependency_overrides.clear()

def test_get_sensor_data_invalid_time_range(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server_invalid_time"
    server = ServerModel(ulid=server_ulid, name="Invalid Time Server")
    db.add(server)
    db.commit()

    params = {
        "server_ulid": server_ulid,
        "start_time": "2024-02-19T13:00:00Z",
        "end_time": "2024-02-19T12:00:00Z"
    }
    response = client.get("/data", params=params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "start_time cannot be greater than end_time"
    app.dependency_overrides.clear()

def test_get_sensor_data_no_results(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server_no_data"
    server = ServerModel(ulid=server_ulid, name="No Data Server")
    db.add(server)
    db.commit()

    params = {
        "server_ulid": server_ulid,
        "start_time": "2024-02-19T12:00:00Z",
        "end_time": "2024-02-19T13:00:00Z"
    }
    response = client.get("/data", params=params)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
    app.dependency_overrides.clear()

def test_get_sensor_data_invalid_datetime_format(client, db):
    app.dependency_overrides[get_current_user] = lambda: "username"
    server_ulid = "server_invalid_datetime"
    server = ServerModel(ulid=server_ulid, name="Invalid Datetime Server")
    db.add(server)
    db.commit()

    params = {
        "server_ulid": server_ulid,
        "start_time": "invalid_date",
        "end_time": "invalid_date"
    }
    response = client.get("/data", params=params)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    app.dependency_overrides.clear()
