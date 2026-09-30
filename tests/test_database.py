"""
FIREGUARD X - Database Tests
"""

import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.database.database import Base
from backend.database.repository import (
    seed_zones_if_empty,
    get_all_zones,
    save_prediction,
    get_prediction_history,
)

# Use in-memory SQLite for testing
test_engine = create_engine("sqlite:///:memory:", echo=False)
TestSession = sessionmaker(bind=test_engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=test_engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)

def test_zone_seeding_and_retrieval(db_session):
    seed_zones_if_empty(db_session)
    zones = get_all_zones(db_session)
    assert len(zones) >= 8
    first = zones[0]
    assert first.zone_name != ""
    assert -90 <= first.latitude <= 90

def test_prediction_storage(db_session):
    pred_data = {
        "zone_id": "test-zone",
        "risk_score": 75.5,
        "risk_level": "HIGH",
        "model_probability": 0.81,
        "data_quality": 1.0,
        "inputs": {"Temperature": 34.0},
        "drivers": [{"feature": "Temperature", "contribution": 0.2}]
    }
    rec = save_prediction(db_session, pred_data)
    assert rec.id is not None
    
    history = get_prediction_history(db_session)
    assert len(history) == 1
    assert history[0].risk_score == 75.5
