class FakeServersRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def exists_by_server_ulid(self, server_ulid: str) -> bool:
        return True
