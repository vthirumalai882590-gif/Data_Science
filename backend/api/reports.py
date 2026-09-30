"""
FIREGUARD X - Reports API Router
"""

import json
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.database.repository import save_report, get_reports
from backend.database.models import ReportRecord
from backend.schemas.report import ReportGenerateRequest, ReportResponse
from backend.services.report_service import generate_html_report

router = APIRouter(tags=["Reports"])

@router.post("/reports/generate", response_model=ReportResponse)
def generate_risk_report(payload: ReportGenerateRequest, db: Session = Depends(get_db)):
    try:
        report_dict = payload.model_dump()
        html_content = generate_html_report(report_dict)
        
        record = save_report(db, {
            "zone_name": payload.zone_name,
            "risk_score": payload.risk_score,
            "risk_level": payload.risk_level,
            "html": html_content,
            "payload": report_dict
        })

        return {
            "id": record.id,
            "timestamp": record.timestamp.isoformat(),
            "zone_name": record.zone_name,
            "risk_score": record.risk_score,
            "risk_level": record.risk_level,
            "report_html": html_content,
            "download_url": f"/api/reports/{record.id}/view",
            "disclaimer": "Academic and educational intelligence report. Not for operational life-safety deployment."
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Report compilation failed: {str(exc)}")

@router.get("/reports")
def list_reports(limit: int = 20, db: Session = Depends(get_db)):
    records = get_reports(db, limit=limit)
    return [
        {
            "id": r.id,
            "timestamp": r.timestamp.isoformat(),
            "zone_name": r.zone_name,
            "risk_score": r.risk_score,
            "risk_level": r.risk_level,
            "view_url": f"/api/reports/{r.id}/view"
        }
        for r in records
    ]

@router.get("/reports/{report_id}/view", response_class=HTMLResponse)
def view_html_report(report_id: int, db: Session = Depends(get_db)):
    record = db.query(ReportRecord).filter(ReportRecord.id == report_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Report not found")
    
    try:
        data = json.loads(record.report_data)
        html = data.get("html") or generate_html_report(data)
        return HTMLResponse(content=html)
    except Exception:
        raise HTTPException(status_code=500, detail="Error formatting report.")
