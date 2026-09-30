"""
FIREGUARD X - Prediction & Risk Intelligence Engine
Integrates ML probability estimation, physical environmental risk scoring,
data quality auditing, and anomaly evaluation into a unified prediction pipeline.
"""

import numpy as np
import pandas as pd
from ml.config import get_risk_tier
from ml.feature_engineering import compute_engineered_features

PHYSICAL_BOUNDS = {
    "Temperature": {"min": -10.0, "max": 60.0, "default": 32.0},
    "RH": {"min": 1.0, "max": 100.0, "default": 50.0},
    "Ws": {"min": 0.0, "max": 120.0, "default": 15.0},
    "Rain": {"min": 0.0, "max": 300.0, "default": 0.0},
    "FFMC": {"min": 0.0, "max": 101.0, "default": 85.0},
    "DMC": {"min": 0.0, "max": 300.0, "default": 16.0},
    "DC": {"min": 0.0, "max": 900.0, "default": 45.0},
    "ISI": {"min": 0.0, "max": 60.0, "default": 6.5},
    "BUI": {"min": 0.0, "max": 300.0, "default": 18.0},
    "FWI": {"min": 0.0, "max": 100.0, "default": 8.0},
    "Region": {"min": 0, "max": 1, "default": 0}
}

REQUIRED_CORE_FIELDS = ["Temperature", "RH", "Ws", "Rain"]

def assess_data_quality(input_data: dict) -> dict:
    """
    Evaluates input data completeness, physical plausibility, and integrity.
    Returns:
        - data_quality: Score from 0.0 to 1.0 (or percentage 0-100)
        - missing_fields: List of missing inputs
        - invalid_fields: List of fields exceeding physical bounds
        - details: Inspection summary
    """
    missing = []
    invalid = []
    total_expected = len(REQUIRED_CORE_FIELDS)
    inspected = 0
    valid_count = 0

    for field in REQUIRED_CORE_FIELDS:
        inspected += 1
        val = input_data.get(field, None)
        if val is None or str(val).strip() == "":
            missing.append(field)
            continue
        try:
            fval = float(val)
            bounds = PHYSICAL_BOUNDS.get(field)
            if bounds and (fval < bounds["min"] or fval > bounds["max"]):
                invalid.append({"field": field, "value": fval, "expected": f"[{bounds['min']}, {bounds['max']}]"})
            else:
                valid_count += 1
        except (ValueError, TypeError):
            invalid.append({"field": field, "value": val, "expected": "numeric"})

    # Check secondary fields if provided
    optional_fields = ["FFMC", "DMC", "DC", "ISI", "BUI", "FWI"]
    for field in optional_fields:
        if field in input_data and input_data[field] is not None:
            inspected += 1
            try:
                fval = float(input_data[field])
                bounds = PHYSICAL_BOUNDS.get(field)
                if bounds and (fval < bounds["min"] or fval > bounds["max"]):
                    invalid.append({"field": field, "value": fval, "expected": f"[{bounds['min']}, {bounds['max']}]"})
                else:
                    valid_count += 1
            except (ValueError, TypeError):
                invalid.append({"field": field, "value": input_data[field], "expected": "numeric"})

    penalty = (len(missing) * 0.25) + (len(invalid) * 0.15)
    quality_score = max(0.20, min(1.0, 1.0 - penalty))

    return {
        "score": round(quality_score, 2),
        "percentage": round(quality_score * 100, 1),
        "missing_fields": missing,
        "invalid_fields": invalid,
        "is_acceptable": len(missing) == 0 and len(invalid) == 0,
        "notes": f"Verified {valid_count} valid parameters. Missing: {len(missing)}, Anomalous: {len(invalid)}."
    }

def calculate_fire_risk_score(raw_prob: float, inputs: dict) -> dict:
    """
    Computes calibrated 0-100 Forest Fire Risk Score.
    Distinguishes statistical ML class probability from composite field risk.
    Scoring Formula:
      Base Score = raw_prob * 100
      Atmospheric Factor = (Temperature / 45.0) * (1.0 - (RH / 100.0))
      Wind Multiplier = min(1.3, 1.0 + (Ws / 80.0))
      Composite Risk = 0.80 * Base Score + 0.20 * (Atmospheric Factor * 100 * Wind Multiplier)
    """
    temp = float(inputs.get("Temperature", 30.0))
    rh = float(inputs.get("RH", 50.0))
    ws = float(inputs.get("Ws", 15.0))
    rain = float(inputs.get("Rain", 0.0))

    base_score = float(raw_prob) * 100.0
    
    # Environmental vulnerability index
    atm_factor = max(0.0, min(1.0, (temp / 45.0) * (1.0 - (rh / 100.0))))
    wind_mult = min(1.25, 1.0 + (ws / 100.0))
    rain_suppression = 0.5 if rain > 2.0 else (0.8 if rain > 0.5 else 1.0)
    
    env_vulnerability = (atm_factor * 100.0 * wind_mult) * rain_suppression
    
    # Blended score
    composite_score = round(np.clip(0.80 * base_score + 0.20 * env_vulnerability, 0.0, 100.0), 1)
    tier = get_risk_tier(composite_score)

    return {
        "risk_score": tier["score"],
        "risk_level": tier["level"],
        "risk_badge": tier["badge"],
        "risk_color": tier["color"],
        "model_probability": round(float(raw_prob), 4),
        "probability_percent": round(float(raw_prob) * 100.0, 1),
        "environmental_vulnerability": round(float(env_vulnerability), 1),
        "methodology": "Blended formulation: 80% Calibrated ML Probability + 20% Environmental Micro-Climate Vulnerability."
    }
