"""
FIREGUARD X - Risk Engine & Tier Tests
"""

import os
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ml.config import get_risk_tier
from ml.predict import calculate_fire_risk_score, assess_data_quality

def test_risk_tiers_mapping():
    assert get_risk_tier(10)["level"] == "LOW"
    assert get_risk_tier(30)["level"] == "MODERATE"
    assert get_risk_tier(50)["level"] == "ELEVATED"
    assert get_risk_tier(75)["level"] == "HIGH"
    assert get_risk_tier(92)["level"] == "CRITICAL"

def test_data_quality_assessment():
    clean_input = {"Temperature": 32.0, "RH": 40.0, "Ws": 15.0, "Rain": 0.0}
    clean_audit = assess_data_quality(clean_input)
    assert clean_audit["score"] == 1.0
    assert clean_audit["is_acceptable"] is True

    # Missing humidity & negative wind speed
    flawed_input = {"Temperature": 32.0, "Ws": -50.0}
    flawed_audit = assess_data_quality(flawed_input)
    assert flawed_audit["score"] < 1.0
    assert "RH" in flawed_audit["missing_fields"]
    assert len(flawed_audit["invalid_fields"]) > 0
