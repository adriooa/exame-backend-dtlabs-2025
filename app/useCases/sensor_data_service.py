from fastapi import HTTPException, status
from app.domain.entities.SensorData import SensorData
from app.domain.dtos.sensor_data_dto import RegisterSensorDataDTO
from app.ports.repositories.sensor_data_repository import SensorDataRepositoryInterface
from app.ports.repositories.servers import ServersRepositoryInterface


class SensorDataService:
    def __init__(self, sensor_data_repository: SensorDataRepositoryInterface, servers_repository: ServersRepositoryInterface):
        self.sensor_data_repository = sensor_data_repository
        self.servers_repository = servers_repository

    def save_sensor_data(self, dto: RegisterSensorDataDTO) -> SensorData:
        data = SensorData(
            server_ulid=dto.server_ulid,
            timestamp=dto.timestamp,
            temperature=dto.temperature,
            humidity=dto.humidity,
            voltage=dto.voltage,
            current=dto.current)
        if not self.servers_repository.exists_by_server_ulid(dto.server_ulid):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Server not found",
            )
        return self.sensor_data_repository.save(data)
