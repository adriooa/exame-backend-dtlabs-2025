from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.container import Container
from app.core.dependencies import get_current_user
from app.domain.dtos.sensor_health_dto import CreateServerDTO, ServerHealthDTO, ServerHealthListDTO
from app.useCases.server_service import ServerService


router = APIRouter()


@router.get(
    "/health/all",
    response_model=ServerHealthListDTO,
    dependencies=[Depends(get_current_user)]
)
@inject
def get_all_servers_health(
    server_service: ServerService = Depends(
        Provide[Container.servers_service])
):
    try:
        return server_service.get_all_servers_health()
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e


@router.get(
        "/health/{server_id}",
        response_model=ServerHealthDTO,
        dependencies=[Depends(get_current_user)]
)
@inject
def get_server_health(
    server_id: str,
    server_service: ServerService = Depends(
        Provide[Container.servers_service])
):
    try:
        server_health = server_service.get_server_health(server_id)

        if not server_health:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Server not found")

        return server_health
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e
    

@router.post(
        "/servers",
        response_model=ServerHealthDTO,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(get_current_user)]
        )
@inject
def register_server(
    dto: CreateServerDTO,
    service: ServerService = Depends(Provide[Container.servers_service]),
) -> ServerHealthDTO:
    try:
        return service.register_server(dto)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e
