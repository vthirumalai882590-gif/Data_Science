"""
FIREGUARD X - Database Schema Models
SQLAlchemy Declarative Models for historical records, spatial zones, simulations, and telemetry.
"""

import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from backend.database.database import Base

class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    zone_id = Column(String(50), nullable=True, default="Custom Area")
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    probability = Column(Float, nullable=False)
    data_quality = Column(Float, nullable=False, default=1.0)
    input_data = Column(Text, nullable=False)   # Serialized JSON of raw inputs
    drivers = Column(Text, nullable=True)       # Serialized JSON of top feature contributions

class ZoneRecord(Base):
    __tablename__ = "zones"

    id = Column(String(50), primary_key=True, index=True)
    zone_name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    region_id = Column(Integer, default=0)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind = Column(Float, nullable=False)
    rainfall = Column(Float, nullable=False)
    ffmc = Column(Float, default=85.0)
    dmc = Column(Float, default=16.0)
    dc = Column(Float, default=45.0)
    isi = Column(Float, default=6.5)
    bui = Column(Float, default=18.0)
    fwi = Column(Float, default=8.0)
    historical_fire_count = Column(Integer, default=0)
    country = Column(String(50), default="India")

class SimulationRecord(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    start_zone = Column(String(50), nullable=False)
    wind_speed = Column(Float, nullable=False)
    wind_direction = Column(String(10), nullable=False)
    dryness = Column(Float, nullable=False)
    duration_hours = Column(Integer, nullable=False)
    result = Column(Text, nullable=False)       # Serialized simulation time-step frames

class ModelRunRecord(Base):
    __tablename__ = "model_runs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    model_name = Column(String(100), nullable=False)
    training_date = Column(String(50), nullable=False)
    metrics = Column(Text, nullable=False)       # JSON string of metrics
    dataset = Column(String(200), nullable=False)

class ReportRecord(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    zone_name = Column(String(100), nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    report_data = Column(Text, nullable=False)   # Full JSON snapshot
