from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from app.core.container import Container
from app.useCases.auth_service import AuthService
from dependency_injector.wiring import inject, Provide

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@inject
def get_current_user(token: str = Depends(oauth2_scheme), service: AuthService = Depends(Provide[Container.auth_service])):
    username = service.decode_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username
