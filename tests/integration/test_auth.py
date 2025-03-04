

from fastapi import status

from app.core.database.models import UserModel


def test_register_user_success(client, db, container_override):  
    payload = {
        "username": "testuser",
        "password": "testpassword",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "access_token" in data

    retrieved_user = db.query(UserModel).filter(UserModel.username == "testuser").first()
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"

    auth_service = container_override.auth_service() 
    assert auth_service.verify_password("testpassword", retrieved_user.hashed_password)

def test_register_user_already_exists(client, db):
    existing_user = UserModel(username="existinguser", hashed_password="hashedpassword")
    db.add(existing_user)
    db.commit()

    payload = {
        "username": "existinguser",
        "password": "testpassword",
    }
    response = client.post("/auth/register", json=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Username already registered"}

def test_register_user_invalid_payload(client):
    payload = {"username": "testuser"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 422


def test_login_user_success(client, db, container_override):
    auth_service = container_override.auth_service() 
    hashed_password = auth_service.hash_password("testpassword")
    user = UserModel(username="testuser", hashed_password=hashed_password)
    db.add(user)
    db.commit()

    payload = {
        "username": "testuser",
        "password": "testpassword",
    }

    response = client.post("/auth/login", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data

def test_login_user_invalid_credentials(client, db, container_override):
    auth_service = container_override.auth_service() 
    hashed_password = auth_service.hash_password("correctpassword")
    user = UserModel(username="testuser", hashed_password=hashed_password)
    db.add(user)
    db.commit()

    payload = {
        "username": "testuser",
        "password": "wrongpassword",
    }
    response = client.post("/auth/login", json=payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid credentials"}

def test_login_user_invalid_payload(client):
    payload = {"username": "testuser"}
    response = client.post("/auth/login", json=payload)
    assert response.status_code == 422