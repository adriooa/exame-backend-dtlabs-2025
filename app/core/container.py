from app.adapters.repositories.servers import PostgresServersRepository
from dependency_injector import containers, providers
from app.core.database.db import engine
from sqlalchemy.orm import sessionmaker
from app.adapters.repositories.sensor_data import PostgresSensorDataRepository
from app.useCases.sensor_data_service import SensorDataService


class Container(containers.DeclarativeContainer):

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_session = providers.Singleton(SessionLocal)

    sensor_data_repository = providers.Factory(
        PostgresSensorDataRepository,
        db_session=db_session
    )
    servers_repository = providers.Factory(
        PostgresServersRepository,
        db_session=db_session
    )

    sensor_data_service = providers.Factory(
        SensorDataService,
        sensor_data_repository=sensor_data_repository,
        servers_repository=servers_repository
    )

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.routes.sensor_data_controller",
        ]
    )
