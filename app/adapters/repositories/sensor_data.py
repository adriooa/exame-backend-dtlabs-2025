from sqlalchemy.orm import Session
from app.ports.repositories.sensor_data_repository import SensorDataRepositoryInterface
from app.domain.entities.SensorData import SensorData
from app.core.database.models import SensorDataModel


class PostgresSensorDataRepository(SensorDataRepositoryInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, data: SensorData) -> SensorData:
        db_item = SensorDataModel(
            server_ulid=data.server_ulid,
            timestamp=data.timestamp,
            temperature=data.temperature,
            humidity=data.humidity,
            voltage=data.voltage,
            current=data.current
        )
        self.db_session.add(db_item)
        self.db_session.commit()
        self.db_session.refresh(db_item)

        return SensorData(
            server_ulid=db_item.server_ulid,
            timestamp=db_item.timestamp,
            temperature=db_item.temperature,
            humidity=db_item.humidity,
            voltage=db_item.voltage,
            current=db_item.current,
            id=db_item.id
        )
