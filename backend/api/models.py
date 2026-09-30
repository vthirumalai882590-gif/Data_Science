"""
FIREGUARD X - Model Laboratory API
Exposes authentic model benchmarks, cross-model comparison metrics,
feature sets, and training provenance.
"""

from fastapi import APIRouter
from ml.model_registry import get_registry

router = APIRouter(tags=["Models"])

@router.get("/model/metrics")
def get_model_metrics():
    registry = get_registry()
    return registry.metrics

@router.get("/model/features")
def get_model_features():
    registry = get_registry()
    from ml.feature_engineering import FEATURE_DESCRIPTIONS
    features_info = []
    for f in registry.feature_names:
        features_info.append({
            "name": f,
            "label": f.replace("_", " ").title(),
            "description": FEATURE_DESCRIPTIONS.get(f, "Environmental parameter")
        })
    return {
        "total_features": len(registry.feature_names),
        "features": features_info
    }

@router.get("/model/metadata")
def get_model_metadata():
    registry = get_registry()
    return registry.metadata
