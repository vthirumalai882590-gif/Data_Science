"""
FIREGUARD X - Zone Schemas
"""

from typing import Optional
from pydantic import BaseModel

class ZoneResponse(BaseModel):
    id: str
    zone_name: str
    latitude: float
    longitude: float
    region_id: int
    risk_score: float
    risk_level: str
    temperature: float
    humidity: float
    wind: float
    rainfall: float
    ffmc: float
    dmc: float
    dc: float
    isi: float
    bui: float
    fwi: float
    historical_fire_count: int
    country: Optional[str] = "India"

    model_config = {"from_attributes": True}
