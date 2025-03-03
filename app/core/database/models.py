from app.core.database.db import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class ServerModel(Base):
    __tablename__ = "servers"

    ulid = Column(String, primary_key=True, unique=True,
                  index=True, nullable=False)
    name = Column(String, nullable=True)
    status = Column(String, nullable=True)

    sensor_data = relationship("SensorDataModel", back_populates="server")


class SensorDataModel(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    server_ulid = Column(String, ForeignKey(
        "servers.ulid"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    voltage = Column(Float, nullable=True)
    current = Column(Float, nullable=True)

    server = relationship("ServerModel", back_populates="sensor_data")
