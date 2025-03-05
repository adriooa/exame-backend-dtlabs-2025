
from typing import List
from pydantic import BaseModel


class ServerHealthDTO(BaseModel):
    server_ulid: str
    status: str
    server_name: str

    class Config:
        orm_mode = True
        from_attributes = True

class ServerHealthListDTO(BaseModel):
    servers: List[ServerHealthDTO]

class CreateServerDTO(BaseModel):
    server_name: str