"""
FIREGUARD X - Database Repository Layer
Provides transactional data access and seeds realistic spatial zones
spanning prominent Indian Forest Reserves & Western Ghats hotspots as well as Mediterranean reserves.
"""

import json
import datetime
import pandas as pd
from sqlalchemy.orm import Session
from backend.database.models import (
    PredictionRecord,
    ZoneRecord,
    SimulationRecord,
    ModelRunRecord,
    ReportRecord,
)
from ml.config import RAW_DATA_PATH, PROCESSED_DATA_PATH, get_risk_tier

DEFAULT_ZONES = [
    # --- INDIA FOREST RESERVES (Karnataka, Western Ghats, Central & Northern India) ---
    {
        "id": "zone-ind-01",
        "zone_name": "Bandipur Tiger Reserve (Karnataka)",
        "country": "India",
        "latitude": 11.6664,
        "longitude": 76.6291,
        "region_id": 2,
        "temperature": 36.5,
        "humidity": 34.0,
        "wind": 18.0,
        "rainfall": 0.0,
        "ffmc": 91.2,
        "dmc": 32.5,
        "dc": 115.0,
        "isi": 12.4,
        "bui": 35.0,
        "fwi": 24.2,
        "historical_fire_count": 48,
    },
    {
        "id": "zone-ind-02",
        "zone_name": "Nagarhole National Park (Karnataka)",
        "country": "India",
        "latitude": 12.0314,
        "longitude": 76.1558,
        "region_id": 2,
        "temperature": 33.5,
        "humidity": 46.0,
        "wind": 14.0,
        "rainfall": 0.0,
        "ffmc": 83.5,
        "dmc": 18.0,
        "dc": 58.0,
        "isi": 6.2,
        "bui": 20.5,
        "fwi": 10.4,
        "historical_fire_count": 26,
    },
    {
        "id": "zone-ind-03",
        "zone_name": "Simlipal Biosphere Reserve (Odisha)",
        "country": "India",
        "latitude": 21.6833,
        "longitude": 86.3333,
        "region_id": 2,
        "temperature": 39.8,
        "humidity": 23.0,
        "wind": 21.0,
        "rainfall": 0.0,
        "ffmc": 94.6,
        "dmc": 42.0,
        "dc": 168.0,
        "isi": 16.8,
        "bui": 46.0,
        "fwi": 32.5,
        "historical_fire_count": 74,
    },
    {
        "id": "zone-ind-04",
        "zone_name": "Jim Corbett Reserve (Uttarakhand)",
        "country": "India",
        "latitude": 29.5300,
        "longitude": 78.7747,
        "region_id": 2,
        "temperature": 37.0,
        "humidity": 31.0,
        "wind": 19.0,
        "rainfall": 0.0,
        "ffmc": 90.8,
        "dmc": 31.0,
        "dc": 118.0,
        "isi": 11.5,
        "bui": 34.0,
        "fwi": 22.8,
        "historical_fire_count": 52,
    },
    {
        "id": "zone-ind-05",
        "zone_name": "Mudumalai Tiger Reserve (Tamil Nadu)",
        "country": "India",
        "latitude": 11.5623,
        "longitude": 76.5345,
        "region_id": 2,
        "temperature": 35.0,
        "humidity": 40.0,
        "wind": 16.0,
        "rainfall": 0.0,
        "ffmc": 87.5,
        "dmc": 22.0,
        "dc": 72.0,
        "isi": 8.0,
        "bui": 24.5,
        "fwi": 14.2,
        "historical_fire_count": 35,
    },
    {
        "id": "zone-ind-06",
        "zone_name": "Kanha Tiger Reserve (Madhya Pradesh)",
        "country": "India",
        "latitude": 22.3345,
        "longitude": 80.6115,
        "region_id": 2,
        "temperature": 41.0,
        "humidity": 19.0,
        "wind": 23.0,
        "rainfall": 0.0,
        "ffmc": 95.5,
        "dmc": 46.0,
        "dc": 182.0,
        "isi": 18.2,
        "bui": 51.0,
        "fwi": 35.8,
        "historical_fire_count": 68,
    },
    {
        "id": "zone-ind-07",
        "zone_name": "Sariska Tiger Reserve (Rajasthan)",
        "country": "India",
        "latitude": 27.3197,
        "longitude": 76.4385,
        "region_id": 2,
        "temperature": 42.5,
        "humidity": 16.0,
        "wind": 24.0,
        "rainfall": 0.0,
        "ffmc": 96.2,
        "dmc": 50.0,
        "dc": 195.0,
        "isi": 19.5,
        "bui": 55.0,
        "fwi": 38.0,
        "historical_fire_count": 59,
    },
    {
        "id": "zone-ind-08",
        "zone_name": "Wayanad Wildlife Sanctuary (Kerala)",
        "country": "India",
        "latitude": 11.6854,
        "longitude": 76.3670,
        "region_id": 2,
        "temperature": 31.0,
        "humidity": 60.0,
        "wind": 12.0,
        "rainfall": 0.8,
        "ffmc": 76.0,
        "dmc": 9.5,
        "dc": 30.0,
        "isi": 3.0,
        "bui": 10.8,
        "fwi": 3.6,
        "historical_fire_count": 14,
    },
    {
        "id": "zone-ind-09",
        "zone_name": "Gir National Park (Gujarat)",
        "country": "India",
        "latitude": 21.1243,
        "longitude": 70.8242,
        "region_id": 2,
        "temperature": 39.0,
        "humidity": 28.0,
        "wind": 19.0,
        "rainfall": 0.0,
        "ffmc": 92.5,
        "dmc": 35.0,
        "dc": 135.0,
        "isi": 14.0,
        "bui": 38.0,
        "fwi": 26.5,
        "historical_fire_count": 41,
    },
    # --- ALGERIA FOREST RESERVES (Mediterranean & Steppe) ---
    {
        "id": "zone-bej-01",
        "zone_name": "Akfadou Forest Reserve",
        "country": "Algeria",
        "latitude": 36.7215,
        "longitude": 4.5821,
        "region_id": 0,
        "temperature": 34.0,
        "humidity": 45.0,
        "wind": 16.0,
        "rainfall": 0.0,
        "ffmc": 86.2,
        "dmc": 18.5,
        "dc": 52.0,
        "isi": 7.4,
        "bui": 20.1,
        "fwi": 11.2,
        "historical_fire_count": 18,
    },
    {
        "id": "zone-bej-02",
        "zone_name": "Gouraya Coastal Ridge",
        "country": "Algeria",
        "latitude": 36.7682,
        "longitude": 5.0934,
        "region_id": 0,
        "temperature": 30.5,
        "humidity": 62.0,
        "wind": 14.0,
        "rainfall": 0.2,
        "ffmc": 74.0,
        "dmc": 8.2,
        "dc": 28.4,
        "isi": 2.5,
        "bui": 9.5,
        "fwi": 2.1,
        "historical_fire_count": 6,
    },
    {
        "id": "zone-bej-03",
        "zone_name": "Soummam Valley Perimeter",
        "country": "Algeria",
        "latitude": 36.6110,
        "longitude": 4.9125,
        "region_id": 0,
        "temperature": 36.0,
        "humidity": 38.0,
        "wind": 18.0,
        "rainfall": 0.0,
        "ffmc": 89.4,
        "dmc": 24.1,
        "dc": 74.8,
        "isi": 9.6,
        "bui": 26.2,
        "fwi": 16.8,
        "historical_fire_count": 24,
    },
    {
        "id": "zone-sba-01",
        "zone_name": "Tessala Mountain Forest",
        "country": "Algeria",
        "latitude": 35.3120,
        "longitude": -0.7410,
        "region_id": 1,
        "temperature": 37.5,
        "humidity": 31.0,
        "wind": 21.0,
        "rainfall": 0.0,
        "ffmc": 91.8,
        "dmc": 31.2,
        "dc": 112.4,
        "isi": 12.4,
        "bui": 34.0,
        "fwi": 23.5,
        "historical_fire_count": 32,
    },
    {
        "id": "zone-sba-02",
        "zone_name": "Mekerra Basin Zone",
        "country": "Algeria",
        "latitude": 35.1950,
        "longitude": -0.6350,
        "region_id": 1,
        "temperature": 33.0,
        "humidity": 52.0,
        "wind": 13.0,
        "rainfall": 0.0,
        "ffmc": 82.5,
        "dmc": 14.2,
        "dc": 42.1,
        "isi": 4.8,
        "bui": 15.0,
        "fwi": 6.4,
        "historical_fire_count": 12,
    },
    {
        "id": "zone-sba-03",
        "zone_name": "Telagh Southern Scrubland",
        "country": "Algeria",
        "latitude": 34.7820,
        "longitude": -0.5710,
        "region_id": 1,
        "temperature": 39.0,
        "humidity": 24.0,
        "wind": 22.0,
        "rainfall": 0.0,
        "ffmc": 93.6,
        "dmc": 39.4,
        "dc": 148.0,
        "isi": 15.2,
        "bui": 41.5,
        "fwi": 28.7,
        "historical_fire_count": 39,
    },
    {
        "id": "zone-buf-01",
        "zone_name": "Djurdjura Foothill Corridor",
        "country": "Algeria",
        "latitude": 36.4520,
        "longitude": 4.2180,
        "region_id": 0,
        "temperature": 27.0,
        "humidity": 70.0,
        "wind": 11.0,
        "rainfall": 1.4,
        "ffmc": 58.2,
        "dmc": 4.5,
        "dc": 14.0,
        "isi": 1.1,
        "bui": 5.1,
        "fwi": 0.8,
        "historical_fire_count": 2,
    },
    {
        "id": "zone-buf-02",
        "zone_name": "Chott Ech Chergui Boundary",
        "country": "Algeria",
        "latitude": 34.4200,
        "longitude": 0.3100,
        "region_id": 1,
        "temperature": 38.5,
        "humidity": 26.0,
        "wind": 19.0,
        "rainfall": 0.0,
        "ffmc": 92.1,
        "dmc": 36.0,
        "dc": 130.5,
        "isi": 13.8,
        "bui": 38.2,
        "fwi": 25.1,
        "historical_fire_count": 29,
    },
]

def seed_zones_if_empty(db: Session):
    """Seed or update base zones to ensure Indian and Algerian reserves are present."""
    for z in DEFAULT_ZONES:
        existing = db.query(ZoneRecord).filter(ZoneRecord.id == z["id"]).first()
        raw_score = min(
            98.0,
            (z["temperature"] * 1.5)
            + (100 - z["humidity"]) * 0.4
            + (z["wind"] * 0.5)
            - (z["rainfall"] * 20),
        )
        tier = get_risk_tier(raw_score)

        if not existing:
            zone_obj = ZoneRecord(
                id=z["id"],
                zone_name=z["zone_name"],
                country=z.get("country", "India"),
                latitude=z["latitude"],
                longitude=z["longitude"],
                region_id=z["region_id"],
                risk_score=tier["score"],
                risk_level=tier["level"],
                temperature=z["temperature"],
                humidity=z["humidity"],
                wind=z["wind"],
                rainfall=z["rainfall"],
                ffmc=z["ffmc"],
                dmc=z["dmc"],
                dc=z["dc"],
                isi=z["isi"],
                bui=z["bui"],
                fwi=z["fwi"],
                historical_fire_count=z["historical_fire_count"],
            )
            db.add(zone_obj)
        else:
            # Update attributes if needed
            existing.country = z.get("country", "India")
            existing.zone_name = z["zone_name"]
            existing.risk_score = tier["score"]
            existing.risk_level = tier["level"]
    db.commit()

def save_prediction(db: Session, prediction_data: dict) -> PredictionRecord:
    record = PredictionRecord(
        zone_id=prediction_data.get("zone_id", "Custom Area"),
        risk_score=prediction_data["risk_score"],
        risk_level=prediction_data["risk_level"],
        probability=prediction_data["model_probability"],
        data_quality=prediction_data.get("data_quality", 1.0),
        input_data=json.dumps(prediction_data.get("inputs", {})),
        drivers=json.dumps(prediction_data.get("drivers", []))
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_prediction_history(db: Session, limit: int = 50) -> list[PredictionRecord]:
    return db.query(PredictionRecord).order_by(PredictionRecord.timestamp.desc()).limit(limit).all()

def get_all_zones(db: Session) -> list[ZoneRecord]:
    return db.query(ZoneRecord).all()

def get_zone_by_id(db: Session, zone_id: str) -> ZoneRecord:
    return db.query(ZoneRecord).filter(ZoneRecord.id == zone_id).first()

def save_simulation(db: Session, sim_data: dict) -> SimulationRecord:
    record = SimulationRecord(
        start_zone=sim_data["start_zone"],
        wind_speed=sim_data["wind_speed"],
        wind_direction=sim_data["wind_direction"],
        dryness=sim_data["dryness"],
        duration_hours=sim_data["duration_hours"],
        result=json.dumps(sim_data["result"])
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def save_report(db: Session, report_data: dict) -> ReportRecord:
    record = ReportRecord(
        zone_name=report_data["zone_name"],
        risk_score=report_data["risk_score"],
        risk_level=report_data["risk_level"],
        report_data=json.dumps(report_data)
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_reports(db: Session, limit: int = 20) -> list[ReportRecord]:
    return db.query(ReportRecord).order_by(ReportRecord.timestamp.desc()).limit(limit).all()
