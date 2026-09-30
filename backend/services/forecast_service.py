"""
FIREGUARD X - Forecast Service
Provides zone-specific risk projection based on diurnal meteorological trends.
"""

from ml.model_registry import get_registry
from ml.forecasting import generate_zone_forecast
from backend.database.repository import get_zone_by_id
from sqlalchemy.orm import Session

def get_zone_risk_forecast(zone_id: str, db: Session) -> dict:
    registry = get_registry()
    zone = get_zone_by_id(db, zone_id)
    
    if not zone:
        # Fallback default conditions
        conditions = {
            "Temperature": 34.0,
            "RH": 42.0,
            "Ws": 18.0,
            "Rain": 0.0,
            "Region": 0,
            "FFMC": 88.0,
            "DMC": 20.0,
            "DC": 60.0,
            "ISI": 8.0,
            "BUI": 22.0,
            "FWI": 12.0
        }
        zone_name = "Selected Micro-Zone"
    else:
        conditions = {
            "Temperature": zone.temperature,
            "RH": zone.humidity,
            "Ws": zone.wind,
            "Rain": zone.rainfall,
            "Region": zone.region_id,
            "FFMC": zone.ffmc,
            "DMC": zone.dmc,
            "DC": zone.dc,
            "ISI": zone.isi,
            "BUI": zone.bui,
            "FWI": zone.fwi
        }
        zone_name = zone.zone_name

    res = generate_zone_forecast(conditions, registry.model, registry.preprocessor)
    res["zone_id"] = zone_id
    res["zone_name"] = zone_name
    return res
