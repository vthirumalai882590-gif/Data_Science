"""
FIREGUARD X - Prediction API Router
Handles real-time prediction, local SHAP explanations, what-if counterfactual analyses,
and retrieval of historical prediction runs.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.database import get_db
from backend.database.repository import save_prediction, get_prediction_history
from backend.schemas.prediction import (
    PredictionInput,
    PredictionResponse,
    ExplainRequest,
    ExplainResponse,
    WhatIfRequest,
    WhatIfResponse,
)
from backend.services.prediction_service import run_prediction_pipeline, run_what_if_analysis

router = APIRouter(tags=["Prediction"])

@router.post("/predict", response_model=PredictionResponse)
def predict_fire_risk(payload: PredictionInput, db: Session = Depends(get_db)):
    try:
        input_data = payload.model_dump()
        result = run_prediction_pipeline(input_data)
        
        # Persist prediction run in database
        save_prediction(db, {
            "zone_id": payload.zone_id or "Custom Area",
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "model_probability": result["model_probability"],
            "data_quality": result["data_quality"]["score"],
            "inputs": result["inputs"],
            "drivers": result["drivers"],
        })

        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Prediction computation error: {str(exc)}")

@router.post("/explain", response_model=ExplainResponse)
def explain_fire_risk(payload: ExplainRequest):
    try:
        input_data = payload.inputs.model_dump()
        result = run_prediction_pipeline(input_data)
        return {
            "base_value": 0.5,
            "drivers": result["drivers"],
            "narrative": result["narrative"]
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Explanation computation error: {str(exc)}")

@router.post("/what-if", response_model=WhatIfResponse)
def what_if_counterfactual(payload: WhatIfRequest):
    try:
        baseline_dict = payload.baseline.model_dump()
        modified_dict = payload.modifications.model_dump()
        return run_what_if_analysis(baseline_dict, modified_dict)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"What-If scenario computation error: {str(exc)}")

@router.get("/predictions/history")
def get_recent_predictions(limit: int = 50, db: Session = Depends(get_db)):
    records = get_prediction_history(db, limit=limit)
    import json
    return [
        {
            "id": r.id,
            "timestamp": r.timestamp.isoformat(),
            "zone_id": r.zone_id,
            "risk_score": r.risk_score,
            "risk_level": r.risk_level,
            "probability": r.probability,
            "data_quality": r.data_quality,
            "input_data": json.loads(r.input_data) if r.input_data else {},
        }
        for r in records
    ]
