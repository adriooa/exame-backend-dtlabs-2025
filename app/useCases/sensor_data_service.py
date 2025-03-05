from typing import List
from fastapi import HTTPException, status
from app.domain.dtos.sensor_health_dto import ServerHealthDTO, ServerHealthListDTO
from app.domain.entities.SensorData import SensorData
from app.domain.dtos.sensor_data_dto import RegisterSensorDataDTO, SensorDataDTO, SensorDataQueryDTO
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
        result = self.sensor_data_repository.save(data)

        self.servers_repository.update_last_update(dto.server_ulid, dto.timestamp)
        
        return result

    def get_sensor_data(self, query: SensorDataQueryDTO) -> List[SensorDataDTO]:
        results = self.sensor_data_repository.get_sensor_data_filtered(query)
        return results
