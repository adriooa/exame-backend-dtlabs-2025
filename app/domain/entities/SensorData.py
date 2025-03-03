from typing import Optional
from datetime import datetime


class SensorData:
    def __init__(
        self,
        server_ulid: str,
        timestamp: datetime,
        temperature: Optional[float] = None,
        humidity: Optional[float] = None,
        voltage: Optional[float] = None,
        current: Optional[float] = None,
        id: Optional[int] = None
    ):
        self.server_ulid = server_ulid
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidity = humidity
        self.voltage = voltage
        self.current = current
        self.id = id
