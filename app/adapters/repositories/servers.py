from sqlalchemy.orm import Session
from app.core.database.models import ServerModel
from app.ports.repositories.servers import ServersRepositoryInterface


class PostgresServersRepository(ServersRepositoryInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def exists_by_server_ulid(self, server_ulid: str) -> bool:
        return self.db_session.query(ServerModel).filter(ServerModel.ulid == server_ulid).first() is not None