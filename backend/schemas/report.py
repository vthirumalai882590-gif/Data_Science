"""
FIREGUARD X - Report Schemas
"""

from typing import Optional, Any
from pydantic import BaseModel, Field

class ReportGenerateRequest(BaseModel):
    zone_name: str = Field("Akfadou Forest Reserve", description="Selected Forest Zone")
    region: str = Field("Bejaia Region", description="Administrative or eco-region")
    inputs: dict = Field(..., description="Observed weather & environmental conditions")
    risk_score: float
    risk_level: str
    probability: float
    drivers: list[dict]
    anomaly_status: str
    notes: Optional[str] = "Standard routine monitoring report"

class ReportResponse(BaseModel):
    id: int
    timestamp: str
    zone_name: str
    risk_score: float
    risk_level: str
    report_html: str
    download_url: Optional[str]
    disclaimer: str
