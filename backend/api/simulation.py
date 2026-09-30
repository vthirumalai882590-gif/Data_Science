"""
FIREGUARD X - Educational Fire Spread Simulator API
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.database.repository import save_simulation
from backend.schemas.simulation import SimulationRequest, SimulationResponse
from backend.services.simulation_service import run_fire_spread_simulation

router = APIRouter(tags=["Simulation"])

@router.post("/simulation", response_model=SimulationResponse)
def simulate_fire_spread(payload: SimulationRequest, db: Session = Depends(get_db)):
    try:
        sim_result = run_fire_spread_simulation(
            start_zone=payload.start_zone,
            wind_speed=payload.wind_speed,
            wind_direction=payload.wind_direction,
            dryness=payload.dryness,
            duration_hours=payload.duration_hours,
            grid_size=payload.grid_size
        )
        
        # Save simulation record
        save_simulation(db, {
            "start_zone": payload.start_zone,
            "wind_speed": payload.wind_speed,
            "wind_direction": payload.wind_direction,
            "dryness": payload.dryness,
            "duration_hours": payload.duration_hours,
            "result": sim_result["steps"]
        })

        return sim_result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Simulation error: {str(exc)}")
