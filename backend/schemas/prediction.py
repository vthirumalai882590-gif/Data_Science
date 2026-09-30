"""
FIREGUARD X - Prediction & What-If Pydantic Schemas
"""

from typing import Optional, Any
from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    Temperature: float = Field(..., description="Ambient temperature in °C", ge=-10.0, le=65.0)
    RH: float = Field(..., description="Relative humidity %", ge=1.0, le=100.0)
    Ws: float = Field(..., description="Wind speed in km/h", ge=0.0, le=120.0)
    Rain: float = Field(0.0, description="Rainfall in mm", ge=0.0, le=300.0)
    FFMC: Optional[float] = Field(None, description="Fine Fuel Moisture Code", ge=0.0, le=105.0)
    DMC: Optional[float] = Field(None, description="Duff Moisture Code", ge=0.0)
    DC: Optional[float] = Field(None, description="Drought Code", ge=0.0)
    ISI: Optional[float] = Field(None, description="Initial Spread Index", ge=0.0)
    BUI: Optional[float] = Field(None, description="Buildup Index", ge=0.0)
    FWI: Optional[float] = Field(None, description="Fire Weather Index", ge=0.0)
    Region: Optional[int] = Field(0, description="Region ID (0: Bejaia, 1: Sidi Bel-abbes)")
    zone_id: Optional[str] = Field("Custom Area", description="Zone ID or custom tag")

class FeatureDriver(BaseModel):
    feature: str
    label: str
    raw_value: Any
    display_value: str
    contribution: float
    abs_contribution: float
    direction: str
    is_positive: bool
    description: str

class AnomalyInfo(BaseModel):
    status: str
    badge: str
    anomaly_score: float
    is_anomaly: bool
    deviations: list[dict]
    narrative: str

class DataQualityInfo(BaseModel):
    score: float
    percentage: float
    missing_fields: list[str]
    invalid_fields: list[dict]
    is_acceptable: bool
    notes: str

class PredictionResponse(BaseModel):
    risk_score: float
    risk_level: str
    risk_badge: str
    risk_color: str
    model_probability: float
    probability_percent: float
    environmental_vulnerability: float
    data_quality: DataQualityInfo
    anomaly: AnomalyInfo
    drivers: list[FeatureDriver]
    narrative: str
    model_name: str
    timestamp: str

class ExplainRequest(BaseModel):
    inputs: PredictionInput

class ExplainResponse(BaseModel):
    base_value: float
    drivers: list[FeatureDriver]
    narrative: str

class WhatIfRequest(BaseModel):
    baseline: PredictionInput
    modifications: PredictionInput

class WhatIfImpact(BaseModel):
    feature: str
    baseline_value: float
    modified_value: float
    direction: str
    reason: str

class WhatIfResponse(BaseModel):
    baseline_risk: float
    baseline_level: str
    modified_risk: float
    modified_level: str
    risk_delta: float
    delta_direction: str
    baseline_probability: float
    modified_probability: float
    primary_drivers_of_change: list[WhatIfImpact]
    disclaimer: str
