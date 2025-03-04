from pydantic import BaseModel, Field
from datetime import datetime
from ulid import parse


class UserFields(BaseModel):
    username: str = Field(..., description="Nome de usuário")
    password: str = Field(..., description="Senha de usuário")


class CreateUserDTO(UserFields):
    pass

class LoginUserDTO(UserFields):
    pass


class UserDTO(UserFields):
    id: int = Field(..., description="Identificador único")

    class Config:
        orm_mode = True
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "username": "user",
                "password": "password"
            }
        }
