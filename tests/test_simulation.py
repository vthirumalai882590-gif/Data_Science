"""
FIREGUARD X - Simulation & CA Progression Tests
"""

import os
import sys
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.services.simulation_service import run_fire_spread_simulation

def test_cellular_simulation_runs():
    res = run_fire_spread_simulation(
        start_zone="zone-bej-01",
        wind_speed=25.0,
        wind_direction="NE",
        dryness=80.0,
        duration_hours=24,
        grid_size=9
    )
    
    assert res["start_zone"] == "zone-bej-01"
    assert len(res["steps"]) >= 4
    # Initial step T+0 must have 1 active fire cell at ignition
    t0 = res["steps"][0]
    assert t0["active_fire_count"] >= 1
    # Check disclaimer exists
    assert "educational simulation" in res["disclaimer"].lower()
