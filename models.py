from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    voltage = Column(Float, nullable=False)
    current = Column(Float, nullable=False)
    power_kw = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)