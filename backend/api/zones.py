"""
FIREGUARD X - Forest Digital Twin & Spatial Zones API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.database.repository import get_all_zones, get_zone_by_id, seed_zones_if_empty
from backend.schemas.zone import ZoneResponse
from backend.services.forecast_service import get_zone_risk_forecast

router = APIRouter(tags=["Zones"])

@router.get("/zones", response_model=list[ZoneResponse])
def list_forest_zones(db: Session = Depends(get_db)):
    seed_zones_if_empty(db)
    return get_all_zones(db)

@router.get("/zones/{zone_id}", response_model=ZoneResponse)
def get_zone_details(zone_id: str, db: Session = Depends(get_db)):
    seed_zones_if_empty(db)
    zone = get_zone_by_id(db, zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail=f"Zone '{zone_id}' not found.")
    return zone

@router.get("/forecast/{zone_id}")
def get_zone_forecast(zone_id: str, db: Session = Depends(get_db)):
    seed_zones_if_empty(db)
    try:
        return get_zone_risk_forecast(zone_id, db)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Forecasting error: {str(exc)}")
