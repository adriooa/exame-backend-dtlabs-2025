from sqlalchemy.orm import Session
from app.core.database.models import UserModel
from app.domain.entities.User import User
from app.ports.repositories.users import UsersRepositoryInterface

class PostgresUsersRepository(UsersRepositoryInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def get_by_username(self, username: str) -> User:
        data = self.db_session.query(UserModel).filter(UserModel.username == username).first()
        if data:
            user = User(username=data.username, password=data.hashed_password)
            return user
        return None
    
    def create_user(self, user: User):
        db_item = UserModel(username=user.username, hashed_password=user.password)
        self.db_session.add(db_item)
        self.db_session.commit()
        self.db_session.refresh(db_item)
        return user
