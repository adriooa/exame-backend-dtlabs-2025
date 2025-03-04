from typing import List
from fastapi import HTTPException, status
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
        return self.sensor_data_repository.save(data)

    def get_sensor_data(self, query: SensorDataQueryDTO) -> List[SensorDataDTO]:
        """
        Processa os filtros e, se necessário, a agregação.
        Delegando a lógica de consulta ao repositório.
        """
        # Pode adicionar lógica adicional aqui se necessário
        results = self.sensor_data_repository.get_sensor_data_filtered(query)
        return results
