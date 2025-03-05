from datetime import datetime, timezone, timedelta
from app.domain.dtos.sensor_health_dto import CreateServerDTO, ServerHealthDTO, ServerHealthListDTO
from app.ports.repositories.servers import ServersRepositoryInterface


class ServerService:
    def __init__(self, servers_repository: ServersRepositoryInterface):
        self.servers_repository = servers_repository
    
    def _calculate_status(self, server) -> str:
        now = datetime.now(timezone.utc)
        if server.last_update is None:
            return "offline"
        last_update = server.last_update
        if last_update.tzinfo is None:
            last_update = last_update.replace(tzinfo=timezone.utc)
        if last_update and (now - last_update) <= timedelta(seconds=10):
            return "online"
        return "offline"


    def get_server_health(self, server_ulid: str):
        server = self.servers_repository.get_server_by_ulid(server_ulid)
        if not server:
            return None
        
        status = self._calculate_status(server)

        return ServerHealthDTO(
            server_ulid=server.ulid,
            status=status,
            server_name=server.name,
        )

    def get_all_servers_health(self):
        servers = self.servers_repository.get_all_servers()
        server_list = [
            ServerHealthDTO(
                server_ulid=server.ulid,
                status=self._calculate_status(server),
                server_name=server.name,
            )
            for server in servers
        ]
        return ServerHealthListDTO(servers=server_list)
    
    def register_server(self, dto: CreateServerDTO) -> ServerHealthDTO:
        server = self.servers_repository.create_server(dto.server_name)
        result = ServerHealthDTO(
            server_ulid=server.ulid,
            status="offline",
            server_name=server.name
        )
        return result