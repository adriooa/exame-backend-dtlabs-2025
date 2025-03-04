from typing import List, Optional
from fastapi import Query
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from app.domain.dtos.sensor_data_dto import SensorDataDTO, SensorDataQueryDTO
from app.ports.repositories.sensor_data_repository import SensorDataRepositoryInterface
from app.domain.entities.SensorData import SensorData
from app.core.database.models import SensorDataModel


class PostgresSensorDataRepository(SensorDataRepositoryInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, data: SensorData) -> SensorData:
        db_item = SensorDataModel(
            server_ulid=data.server_ulid,
            timestamp=data.timestamp,
            temperature=data.temperature,
            humidity=data.humidity,
            voltage=data.voltage,
            current=data.current
        )
        self.db_session.add(db_item)
        self.db_session.commit()
        self.db_session.refresh(db_item)

        return SensorData(
            server_ulid=db_item.server_ulid,
            timestamp=db_item.timestamp,
            temperature=db_item.temperature,
            humidity=db_item.humidity,
            voltage=db_item.voltage,
            current=db_item.current,
            id=db_item.id
        )
    
    def _apply_filters(self, query, server_ulid: Optional[str], start_time: Optional[str], end_time: Optional[str]):
        """Aplica filtros comuns à query."""
        if server_ulid:
            query = query.filter(SensorDataModel.server_ulid == server_ulid)
        if start_time:
            query = query.filter(SensorDataModel.timestamp >= start_time)
        if end_time:
            query = query.filter(SensorDataModel.timestamp <= end_time)
        return query

    def get_sensor_data_filtered(self, query_params: SensorDataQueryDTO) -> List:
        db = self.db_session

        base_query = db.query(SensorDataModel.server_ulid, SensorDataModel.timestamp)

        if query_params.aggregation:
            interval_map = {"minute": "1 minute", "hour": "1 hour", "day": "1 day"}
            interval = interval_map.get(query_params.aggregation)
            if not interval:
                raise ValueError("Invalid aggregation value")

            bucket = func.time_bucket(interval, SensorDataModel.timestamp).label("timestamp")
            base_query = db.query(SensorDataModel.server_ulid, bucket)

            if query_params.sensor_type:
                sensor_col = getattr(SensorDataModel, query_params.sensor_type, None)
                if not sensor_col:
                    raise ValueError("Invalid sensor type provided")
                avg_value = func.avg(sensor_col).label(query_params.sensor_type)
                base_query = base_query.add_columns(avg_value)
            else:
                base_query = base_query.add_columns(
                    func.avg(SensorDataModel.temperature).label("temperature"),
                    func.avg(SensorDataModel.humidity).label("humidity"),
                    func.avg(SensorDataModel.voltage).label("voltage"),
                    func.avg(SensorDataModel.current).label("current"),
                )

            base_query = self._apply_filters(base_query, query_params.server_ulid, query_params.start_time, query_params.end_time)
            base_query = base_query.group_by(SensorDataModel.server_ulid, bucket).order_by(bucket)

        else:
            if query_params.sensor_type:
                sensor_col = getattr(SensorDataModel, query_params.sensor_type, None)
                if not sensor_col:
                    raise ValueError("Invalid sensor type provided")
                base_query = base_query.add_columns(sensor_col.label(query_params.sensor_type))
            else:
                base_query = base_query.add_columns(
                    SensorDataModel.temperature,
                    SensorDataModel.humidity,
                    SensorDataModel.voltage,
                    SensorDataModel.current,
                )

            base_query = self._apply_filters(base_query, query_params.server_ulid, query_params.start_time, query_params.end_time)
            base_query = base_query.order_by(SensorDataModel.timestamp)

        results = base_query.all()

        return [dict(row._asdict()) for row in results]
