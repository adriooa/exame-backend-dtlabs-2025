from datetime import datetime, timezone
from sqlalchemy.orm import Session
import ulid
from app.core.database.models import ServerModel
from app.ports.repositories.servers import ServersRepositoryInterface


class PostgresServersRepository(ServersRepositoryInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def exists_by_server_ulid(self, server_ulid: str) -> bool:
        return self.db_session.query(ServerModel).filter(ServerModel.ulid == server_ulid).first() is not None
        
    def get_server_by_ulid(self, server_ulid: str):
        return self.db_session.query(ServerModel).filter(ServerModel.ulid == server_ulid).first()

    def get_all_servers(self):
        return self.db_session.query(ServerModel).all()
    
    def get_server_status(self, server: ServerModel):
        if server.last_update and (datetime.now(timezone.utc) - server.last_update).total_seconds() <= 10:
            return "online"
        return "offline"
    
    def update_last_update(self, ulid: str, timestamp: datetime):
        server = self.get_server_by_ulid(ulid)
        if server:
            server.last_update = timestamp
            self.db_session.commit()
            
    def create_server(self, server_name: str) -> ServerModel:
        new_ulid = str(ulid.new())
        server = ServerModel(
            ulid=new_ulid,
            name=server_name,
            last_update=None
        )
        self.db_session.add(server)
        self.db_session.commit()
        self.db_session.refresh(server)
        return server