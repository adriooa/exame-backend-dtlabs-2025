from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.core.container import Container
from app.domain.dtos.sensor_data_dto import RegisterSensorDataDTO, SensorDataDTO
from app.useCases.sensor_data_service import SensorDataService

router = APIRouter()


@router.post("/data", response_model=SensorDataDTO, status_code=status.HTTP_201_CREATED)
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
