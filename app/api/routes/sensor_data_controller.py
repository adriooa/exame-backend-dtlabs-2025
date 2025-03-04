from typing import List
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.container import Container
from app.core.dependencies import get_current_user
from app.domain.dtos.sensor_data_dto import RegisterSensorDataDTO, SensorDataDTO, SensorDataQueryDTO
from app.useCases.sensor_data_service import SensorDataService

router = APIRouter()


@router.post("/data",
             response_model=SensorDataDTO,
             status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(get_current_user)]
             )
@inject
def register_sensor_data(
    dto: RegisterSensorDataDTO,
    service: SensorDataService = Depends(
        Provide[Container.sensor_data_service]),
) -> SensorDataDTO:
    try:
        saved_data = service.save_sensor_data(dto)

        return SensorDataDTO.from_orm(saved_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e


@router.get("/data", response_model=None, status_code=status.HTTP_200_OK)
@inject
def get_sensor_data(
    query: SensorDataQueryDTO = Depends(),
    service: SensorDataService = Depends(Provide[Container.sensor_data_service]),
) -> List[SensorDataDTO]:
    """
    Consulta os dados dos sensores com suporte a filtros e agregação.
    - Se aggregation for informado, retorna dados agregados (média) por período.
    - Se não for informado, retorna os dados conforme armazenados.
    """
    return service.get_sensor_data(query)
