from abc import ABC, abstractmethod


class ServersRepositoryInterface(ABC):
    @abstractmethod
    def exists_by_server_ulid(self, server_ulid: str) -> bool:
        pass
