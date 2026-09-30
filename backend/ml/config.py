"""
FIREGUARD X - Machine Learning Configuration
Defines file paths, random seeds, model hyper-parameters, and standardized risk thresholds.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "forest_fires.csv")
INTERIM_DATA_PATH = os.path.join(DATA_DIR, "interim", "cleaned_fires.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed", "featured_fires.csv")

MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "model.pkl")
ALL_MODELS_PATH = os.path.join(MODELS_DIR, "all_models.pkl")
PREPROCESSOR_PATH = os.path.join(MODELS_DIR, "preprocessor.pkl")
ANOMALY_MODEL_PATH = os.path.join(MODELS_DIR, "anomaly_model.pkl")
METRICS_PATH = os.path.join(MODELS_DIR, "metrics.json")
FEATURE_NAMES_PATH = os.path.join(MODELS_DIR, "feature_names.json")
METADATA_PATH = os.path.join(MODELS_DIR, "model_metadata.json")

REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FIGURES_DIR = os.path.join(REPORTS_DIR, "figures")
GENERATED_REPORTS_DIR = os.path.join(REPORTS_DIR, "generated")

RANDOM_STATE = 42
TEST_SIZE = 0.20

# Standardized 5-tier Fire Risk Level Criteria
RISK_LEVELS = [
    {"min": 0, "max": 20, "level": "LOW", "color": "#16a34a", "badge": "🟢 LOW"},
    {"min": 21, "max": 40, "level": "MODERATE", "color": "#ca8a04", "badge": "🟡 MODERATE"},
    {"min": 41, "max": 60, "level": "ELEVATED", "color": "#ea580c", "badge": "🟠 ELEVATED"},
    {"min": 61, "max": 80, "level": "HIGH", "color": "#dc2626", "badge": "🔴 HIGH"},
    {"min": 81, "max": 100, "level": "CRITICAL", "color": "#7c2d12", "badge": "🟣 CRITICAL"},
]

def get_risk_tier(score: float) -> dict:
    """Map numeric risk score (0-100) to qualitative risk category."""
    clipped = max(0.0, min(100.0, float(score)))
    for tier in RISK_LEVELS:
        if tier["min"] <= round(clipped) <= tier["max"]:
            return {
                "score": round(clipped, 1),
                "level": tier["level"],
                "color": tier["color"],
                "badge": tier["badge"],
            }
    return {
        "score": round(clipped, 1),
        "level": "CRITICAL",
        "color": "#7c2d12",
        "badge": "🟣 CRITICAL",
    }
