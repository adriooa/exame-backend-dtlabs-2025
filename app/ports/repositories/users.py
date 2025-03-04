from abc import ABC, abstractmethod
from app.domain.entities.User import User

class UsersRepositoryInterface(ABC):
    @abstractmethod
    def create_user(user: User) -> User:
        pass

    @abstractmethod
    def get_by_username(username: str) -> User:
        pass