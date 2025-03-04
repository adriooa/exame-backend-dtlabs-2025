from abc import ABC, abstractmethod
from typing import List
from app.domain.dtos.sensor_data_dto import SensorDataDTO, SensorDataQueryDTO
from app.domain.entities.SensorData import SensorData

class SensorDataRepositoryInterface(ABC):
    @abstractmethod
    def save(self, data: SensorData) -> SensorData:
        pass

    def get_sensor_data_filtered(self, query: SensorDataQueryDTO) -> List[SensorDataDTO]:
        pass
