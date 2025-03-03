from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dependency_injector import providers
from sqlalchemy.exc import ProgrammingError
from app.adapters.repositories.sensor_data import PostgresSensorDataRepository
from app.adapters.repositories.servers import PostgresServersRepository
from app.core.container import Container
from app.core.database.db import Base, get_db
from app.core.config import configs 
from app.main import app 


TEST_SQLALCHEMY_DATABASE_URL: str = configs.TEST_DATABASE_URL

print(TEST_SQLALCHEMY_DATABASE_URL)

admin_engine = create_engine(
    f"postgresql://{configs.POSTGRES_USER}:{configs.POSTGRES_PASSWORD}@{configs.POSTGRES_SERVER}/postgres", isolation_level="AUTOCOMMIT")


engine = create_engine(TEST_SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def create_test_database():
    with admin_engine.connect() as connection:
        try:
            connection.execute(
                text(
                    f"CREATE DATABASE {TEST_SQLALCHEMY_DATABASE_URL.split('/')[-1]}")
            )
        except ProgrammingError:
            print("Database already exists, continuing...")


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    create_test_database()  
    Base.metadata.create_all(bind=engine)  
    yield
    Base.metadata.drop_all(bind=engine) 


@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function", autouse=True)
def container_override(db):
    container = Container()

    container.db_session.override(providers.Object(db))
    
    container.servers_repository.override(
        providers.Factory(PostgresServersRepository, db_session=db)
    )
    
    container.sensor_data_repository.override(
        providers.Factory(PostgresSensorDataRepository, db_session=db)
    )

    yield container
    container.shutdown_resources()

@pytest.fixture()
def client(db):
    def override_get_db(): 
        yield db

    app.dependency_overrides[get_db] = override_get_db  

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear() 
