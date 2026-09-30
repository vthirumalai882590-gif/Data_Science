"""
FIREGUARD X - Risk Forecasting Engine
Projects short-to-medium horizon environmental and fire-risk trajectories (6h, 12h, 24h, 48h, 72h)
using diurnal solar-radiation thermodynamic cycles and historical meteorological inertia.
"""

import numpy as np
import pandas as pd
from ml.config import get_risk_tier
from ml.predict import calculate_fire_risk_score

HORIZONS = [
    {"hours": 6, "label": "T+6 Hours", "period": "Afternoon Peak", "temp_delta": 2.5, "rh_delta": -8.0, "ws_delta": 2.0},
    {"hours": 12, "label": "T+12 Hours", "period": "Night Inversion", "temp_delta": -6.0, "rh_delta": 18.0, "ws_delta": -3.0},
    {"hours": 24, "label": "T+24 Hours", "period": "Next Day Noon", "temp_delta": 1.0, "rh_delta": -2.0, "ws_delta": 1.0},
    {"hours": 48, "label": "T+48 Hours", "period": "Day 2 Trend", "temp_delta": 1.8, "rh_delta": -4.0, "ws_delta": 2.5},
    {"hours": 72, "label": "T+72 Hours", "period": "Day 3 Trend", "temp_delta": 0.5, "rh_delta": 1.0, "ws_delta": -1.0},
]

def generate_zone_forecast(base_conditions: dict, model, preprocessor) -> dict:
    """
    Simulates physical weather evolution across diurnal cycles and computes
    projected fire risk scores at 6h, 12h, 24h, 48h, and 72h.
    """
    forecast_points = []
    
    curr_temp = float(base_conditions.get("Temperature", 32.0))
    curr_rh = float(base_conditions.get("RH", 50.0))
    curr_ws = float(base_conditions.get("Ws", 15.0))
    curr_rain = float(base_conditions.get("Rain", 0.0))
    region = int(base_conditions.get("Region", 0))

    # Current baseline
    base_input = dict(base_conditions)
    base_df = pd.DataFrame([base_input])
    base_scaled = preprocessor.transform(base_df)
    base_prob = float(model.predict_proba(base_scaled)[0, 1])
    base_risk = calculate_fire_risk_score(base_prob, base_input)

    current_summary = {
        "hours": 0,
        "label": "Current (T+0)",
        "period": "Baseline Observation",
        "temperature": round(curr_temp, 1),
        "rh": round(curr_rh, 1),
        "ws": round(curr_ws, 1),
        "rain": round(curr_rain, 1),
        "risk_score": base_risk["risk_score"],
        "risk_level": base_risk["risk_level"],
        "risk_color": base_risk["risk_color"],
        "probability": base_risk["model_probability"]
    }

    for step in HORIZONS:
        f_temp = max(10.0, min(50.0, curr_temp + step["temp_delta"]))
        f_rh = max(10.0, min(98.0, curr_rh + step["rh_delta"]))
        f_ws = max(2.0, min(60.0, curr_ws + step["ws_delta"]))
        f_rain = max(0.0, curr_rain * 0.5)

        step_inputs = dict(base_conditions)
        step_inputs["Temperature"] = f_temp
        step_inputs["RH"] = f_rh
        step_inputs["Ws"] = f_ws
        step_inputs["Rain"] = f_rain
        step_inputs["Region"] = region

        step_df = pd.DataFrame([step_inputs])
        step_scaled = preprocessor.transform(step_df)
        step_prob = float(model.predict_proba(step_scaled)[0, 1])
        step_risk = calculate_fire_risk_score(step_prob, step_inputs)

        forecast_points.append({
            "hours": step["hours"],
            "label": step["label"],
            "period": step["period"],
            "temperature": round(f_temp, 1),
            "rh": round(f_rh, 1),
            "ws": round(f_ws, 1),
            "rain": round(f_rain, 1),
            "risk_score": step_risk["risk_score"],
            "risk_level": step_risk["risk_level"],
            "risk_color": step_risk["risk_color"],
            "risk_badge": step_risk["risk_badge"],
            "probability": step_risk["model_probability"]
        })

    # Detect escalation
    max_forecast_score = max([pt["risk_score"] for pt in forecast_points])
    score_change = round(max_forecast_score - base_risk["risk_score"], 1)
    is_escalating = score_change >= 15.0

    return {
        "baseline": current_summary,
        "forecast": forecast_points,
        "is_escalating": is_escalating,
        "score_delta": score_change,
        "escalation_warning": "⚠️ RAPID RISK ESCALATION DETECTED: Forecast shows elevated microclimate risk." if is_escalating else "Stable trajectory observed across projected horizons.",
        "methodology": "Diurnal atmospheric thermodynamic projection combined with historical meteorological inertia.",
        "label": "SIMULATED METEOROLOGICAL FORECAST"
    }
