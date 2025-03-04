from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from app.core.config import configs
from app.domain.dtos.token_dto import TokenDTO
from app.domain.dtos.user_dto import CreateUserDTO, LoginUserDTO
from app.domain.entities.User import User
from app.ports.repositories.users import UsersRepositoryInterface
import jwt
from jwt import PyJWTError as JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = configs.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

class AuthService:
    def __init__(self, user_repository: UsersRepositoryInterface):
        self.user_repository = user_repository

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    def register_user(self, dto: CreateUserDTO) -> TokenDTO:
        existing_user = self.user_repository.get_by_username(dto.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = self.hash_password(dto.password)
        data = User(username=dto.username, password=hashed_password)
        user = self.user_repository.create_user(data)

        access_token = self.create_access_token({"sub": user.username})
        return TokenDTO(access_token=access_token)

    def login_user(self, dto: LoginUserDTO) -> TokenDTO:
        user = self.user_repository.get_by_username(dto.username)
        if not user or not self.verify_password(dto.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = self.create_access_token({"sub": user.username})
        return TokenDTO(access_token=access_token)

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
