from abc import ABC, abstractmethod
from app.domain.entities.Server import Server


class ServersRepositoryInterface(ABC):
    @abstractmethod
    def exists_by_server_ulid(self, server_ulid: str) -> bool:
        pass
