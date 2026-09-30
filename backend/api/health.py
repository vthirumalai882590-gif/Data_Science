"""
FIREGUARD X - Health API
"""

import datetime
from fastapi import APIRouter
from ml.model_registry import get_registry

router = APIRouter(tags=["Health"])

@router.get("/health")
def get_health():
    registry = get_registry()
    return {
        "status": "HEALTHY",
        "service": "FIREGUARD X Intelligence Platform",
        "version": "1.0.0",
        "model_loaded": registry.is_loaded,
        "selected_model": registry.metadata.get("model_name", "N/A"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
