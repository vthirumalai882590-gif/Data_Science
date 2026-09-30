"""
FIREGUARD X - Educational Fire Spread Simulation Schemas
"""

from typing import Optional
from pydantic import BaseModel, Field

class SimulationRequest(BaseModel):
    start_zone: str = Field("zone-bej-01", description="Identifier of ignition origin zone")
    wind_speed: float = Field(20.0, description="Wind velocity in km/h", ge=0.0, le=100.0)
    wind_direction: str = Field("NE", description="Wind heading: N, NE, E, SE, S, SW, W, NW")
    dryness: float = Field(75.0, description="Relative dryness index (0-100)", ge=0.0, le=100.0)
    duration_hours: int = Field(24, description="Simulation duration (e.g. 24 hours)", ge=6, le=72)
    grid_size: int = Field(9, description="Dimension of simulation cellular grid (e.g. 9x9)", ge=5, le=15)

class CellState(BaseModel):
    row: int
    col: int
    state: str  # "SAFE", "AT_RISK", "SIMULATED_FIRE", "AFFECTED"
    intensity: float

class SimulationStep(BaseModel):
    time_label: str  # "T+0", "T+6", "T+12", "T+18", "T+24"
    hours: int
    cells: list[CellState]
    active_fire_count: int
    affected_count: int
    at_risk_count: int

class SimulationResponse(BaseModel):
    start_zone: str
    wind_speed: float
    wind_direction: str
    dryness: float
    duration_hours: int
    grid_dimension: int
    steps: list[SimulationStep]
    disclaimer: str
