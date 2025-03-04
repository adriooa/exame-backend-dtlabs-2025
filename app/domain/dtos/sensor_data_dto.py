from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, model_validator, validator, field_validator
from datetime import datetime
from ulid import parse


class SensorDataFields(BaseModel):
    server_ulid: str = Field(..., description="ULID do servidor")
    timestamp: datetime = Field(..., description="Timestamp da leitura")
    temperature: Optional[float] = Field(
        None, description="Temperatura em Celsius")
    humidity: Optional[float] = Field(
        None, description="Umidade relativa em %")
    voltage: Optional[float] = Field(
        None, description="Tensão elétrica em Volts")
    current: Optional[float] = Field(
        None, description="Corrente elétrica em Ampères")

class RegisterSensorDataDTO(SensorDataFields):
    @field_validator("server_ulid")  
    @classmethod
    def server_ulid_must_be_valid(cls, v):
        try:
            parse(v)
        except ValueError:
            raise ValueError("Input should be a valid ULID")
        return v

    @field_validator("timestamp")
    @classmethod
    def timestamp_must_be_iso_format(cls, v):
        if not isinstance(v, datetime):
            raise ValueError("Invalid date format")
        return v


    @model_validator(mode='after')
    def check_humidity_0_100(self) -> 'RegisterSensorDataDTO':
        if not (self.humidity is None or (0 <= self.humidity <= 100)):
            raise ValueError("Humidity must be between 0 and 100")
        return self    

    @model_validator(mode='after')
    def check_at_least_one_sensor(self) -> 'RegisterSensorDataDTO':
        if not (self.temperature is not None or
                self.humidity is not None or
                self.voltage is not None or
                self.current is not None):
            raise ValueError("At least one sensor value must be provided")
        return self


class SensorDataDTO(SensorDataFields):
    id: int = Field(..., description="Identificador único")

    class Config:
        orm_mode = True
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "server_ulid": "01F0G5YG5Z09W9854Z09W9854Z",
                "timestamp": "2024-07-26T14:30:00Z",
                "temperature": 25.5,
                "humidity": 62.3,
                "voltage": 220.1,
                "current": 1.2,
            }
        }


class SensorTypeEnum(str, Enum):
    temperature = "temperature"
    humidity = "humidity"
    voltage = "voltage"
    current = "current"

class AggregationEnum(str, Enum):
    minute = "minute"
    hour = "hour"
    day = "day"

class SensorDataQueryDTO(BaseModel):
    server_ulid: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    sensor_type: Optional[SensorTypeEnum] = None
    aggregation: Optional[AggregationEnum] = None 
        