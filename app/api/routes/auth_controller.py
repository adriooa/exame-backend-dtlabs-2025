from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.container import Container
from app.domain.dtos.token_dto import TokenDTO
from app.domain.dtos.user_dto import CreateUserDTO, LoginUserDTO
from app.useCases.auth_service import AuthService

router = APIRouter()

@router.post("/auth/register", response_model=TokenDTO, status_code=status.HTTP_201_CREATED)
@inject
def register_user(
    dto: CreateUserDTO,
    service: AuthService = Depends(
        Provide[Container.auth_service]),
) -> TokenDTO:
    try:
        return service.register_user(dto)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e
    
@router.post("/auth/login", response_model=TokenDTO)
@inject
def login_user(
    dto: LoginUserDTO,
    service: AuthService = Depends(Provide[Container.auth_service]),
) -> TokenDTO:
    try:
        return service.login_user(dto)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e
