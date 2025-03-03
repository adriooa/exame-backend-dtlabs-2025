from abc import ABC, abstractmethod
from app.domain.entities.SensorData import SensorData

class SensorDataRepositoryInterface(ABC):
    @abstractmethod
    def save(self, data: SensorData) -> SensorData:
        pass
