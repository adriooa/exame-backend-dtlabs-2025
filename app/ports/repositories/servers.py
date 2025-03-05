from abc import ABC, abstractmethod
import datetime
from typing import List

from app.core.database.models import ServerModel


class ServersRepositoryInterface(ABC):
    @abstractmethod
    def exists_by_server_ulid(self, server_ulid: str) -> bool:
        pass

    @abstractmethod
    def get_server_by_ulid(self, server_ulid: str) -> ServerModel:
        pass

    @abstractmethod
    def get_all_servers(self) -> List[ServerModel]:
        pass

    @abstractmethod
    def get_server_status(self, server: ServerModel) -> str:
        pass
    
    @abstractmethod
    def update_last_update(self, ulid: str, timestamp: datetime):
        pass

    @abstractmethod
    def create_server(self, server_name: str) -> ServerModel:
        pass