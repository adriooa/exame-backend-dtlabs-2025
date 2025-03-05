from app.adapters.repositories.servers import PostgresServersRepository
from dependency_injector import containers, providers
from app.adapters.repositories.users import PostgresUsersRepository
from app.core.database.db import engine
from sqlalchemy.orm import sessionmaker
from app.adapters.repositories.sensor_data import PostgresSensorDataRepository
from app.useCases.auth_service import AuthService
from app.useCases.sensor_data_service import SensorDataService
from app.useCases.server_service import ServerService


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

    user_repository = providers.Factory(
        PostgresUsersRepository,
        db_session=db_session
    )

    sensor_data_service = providers.Factory(
        SensorDataService,
        sensor_data_repository=sensor_data_repository,
        servers_repository=servers_repository
    )

    servers_service = providers.Factory(
        ServerService,
        servers_repository=servers_repository
    )

    auth_service = providers.Factory(
        AuthService,
        user_repository=user_repository
    )

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.routes.sensor_data_controller",
            "app.api.routes.auth_controller",
            "app.api.routes.servers_controller"
        ]
    )
