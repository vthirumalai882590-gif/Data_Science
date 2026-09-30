"""
FIREGUARD X - FastAPI Integration Tests
"""

import os
import sys
import pytest
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.main import app
from backend.database.database import Base, engine, SessionLocal
from backend.database.repository import seed_zones_if_empty

Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_zones_if_empty(db)
db.close()

client = TestClient(app)

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert data["model_loaded"] is True

def test_api_dashboard():
    res = client.get("/api/dashboard")
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data
    assert "top_risk_zones" in data
    assert data["summary"]["active_zones"] > 0

def test_api_predict():
    payload = {
        "Temperature": 35.0,
        "RH": 30.0,
        "Ws": 18.0,
        "Rain": 0.0,
        "Region": 0
    }
    res = client.post("/api/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "risk_score" in data
    assert "risk_level" in data
    assert "drivers" in data
    assert "anomaly" in data
    assert "data_quality" in data

def test_api_zones():
    res = client.get("/api/zones")
    assert res.status_code == 200
    zones = res.json()
    assert len(zones) > 0
    
    first_id = zones[0]["id"]
    res_single = client.get(f"/api/zones/{first_id}")
    assert res_single.status_code == 200
    assert res_single.json()["id"] == first_id

def test_api_forecast():
    res = client.get("/api/zones")
    zone_id = res.json()[0]["id"]
    f_res = client.get(f"/api/forecast/{zone_id}")
    assert f_res.status_code == 200
    data = f_res.json()
    assert "forecast" in data
    assert len(data["forecast"]) >= 4

def test_api_models_metrics():
    res = client.get("/api/model/metrics")
    assert res.status_code == 200
    data = res.json()
    assert "models" in data
    assert "selected_model" in data

def test_api_simulation():
    payload = {
        "start_zone": "zone-bej-01",
        "wind_speed": 18.0,
        "wind_direction": "NE",
        "dryness": 65.0,
        "duration_hours": 24,
        "grid_size": 7
    }
    res = client.post("/api/simulation", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "steps" in data
    assert len(data["steps"]) > 0
