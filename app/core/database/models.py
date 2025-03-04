from app.core.database.db import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
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

    # TODO: verificar primary key
    id = Column(Integer, primary_key=True, autoincrement= True)
    server_ulid = Column(String, ForeignKey(
        "servers.ulid"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, primary_key=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    voltage = Column(Float, nullable=True)
    current = Column(Float, nullable=True)

    server = relationship("ServerModel", back_populates="sensor_data")


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)