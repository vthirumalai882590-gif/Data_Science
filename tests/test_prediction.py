"""
FIREGUARD X - Prediction & Inference Unit Tests
"""

import os
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.services.prediction_service import run_prediction_pipeline, run_what_if_analysis

def test_prediction_pipeline_high_risk():
    high_risk_input = {
        "Temperature": 40.0,
        "RH": 20.0,
        "Ws": 25.0,
        "Rain": 0.0,
        "FFMC": 94.0,
        "DMC": 38.0,
        "DC": 140.0,
        "ISI": 15.0,
        "BUI": 42.0,
        "FWI": 28.0,
        "Region": 1
    }
    res = run_prediction_pipeline(high_risk_input)
    assert res["risk_score"] >= 60.0
    assert res["risk_level"] in ("HIGH", "CRITICAL")
    assert res["model_probability"] > 0.60
    assert len(res["drivers"]) > 0

def test_prediction_pipeline_low_risk():
    low_risk_input = {
        "Temperature": 22.0,
        "RH": 85.0,
        "Ws": 8.0,
        "Rain": 5.0,
        "FFMC": 45.0,
        "DMC": 3.0,
        "DC": 8.0,
        "ISI": 0.5,
        "BUI": 2.0,
        "FWI": 0.2,
        "Region": 0
    }
    res = run_prediction_pipeline(low_risk_input)
    assert res["risk_score"] < 40.0
    assert res["risk_level"] in ("LOW", "MODERATE")
    assert res["model_probability"] < 0.40

def test_what_if_counterfactual():
    baseline = {"Temperature": 38.0, "RH": 25.0, "Ws": 20.0, "Rain": 0.0}
    # Simulate rainfall and cooling
    modified = {"Temperature": 28.0, "RH": 65.0, "Ws": 10.0, "Rain": 4.0}
    
    analysis = run_what_if_analysis(baseline, modified)
    assert analysis["risk_delta"] < 0
    assert analysis["delta_direction"] == "DECREASED RISK"
    assert len(analysis["primary_drivers_of_change"]) > 0
