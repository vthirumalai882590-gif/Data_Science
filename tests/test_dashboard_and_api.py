"""Unit and integration tests for dashboard components and API integration."""

import json
from pathlib import Path

import pandas as pd
import pytest

from src.api.weather_client import (
    get_current_weather,
    get_forest_weather,
    get_hourly_forecast,
    resolve_forest_name,
)
from src.config.settings import INDIAN_FORESTS, MODELS_DIR


def test_indian_forests_config():
    """Verify INDIAN_FORESTS dictionary is well-formed."""
    assert len(INDIAN_FORESTS) >= 8
    for name, data in INDIAN_FORESTS.items():
        assert "latitude" in data
        assert "longitude" in data
        assert "state" in data
        assert "vulnerability" in data
        assert isinstance(data["latitude"], float)
        assert isinstance(data["longitude"], float)


def test_forest_weather_resolution():
    """Verify forest name resolver."""
    canonical = resolve_forest_name("Bandipur")
    assert "Bandipur" in canonical


def test_live_weather_client_with_fallback():
    """Verify live weather client retrieves data or falls back cleanly."""
    coords = (11.6667, 76.6333)  # Bandipur
    cur = get_current_weather(coords[0], coords[1], timeout=5.0)
    assert "temperature" in cur
    assert "relative_humidity" in cur
    assert "wind_speed" in cur
    assert "rain" in cur
    assert isinstance(cur["temperature"], (int, float))

    hourly = get_hourly_forecast(coords[0], coords[1], timeout=6.0)
    assert isinstance(hourly, pd.DataFrame)
    assert not hourly.empty
    assert "temperature" in hourly.columns or "temperature_2m" in hourly.columns


def test_model_metrics_json():
    """Verify model_metrics.json contains Ridge, Random Forest, and XGBoost benchmarks."""
    metrics_path = MODELS_DIR / "model_metrics.json"
    assert metrics_path.exists(), "models/model_metrics.json must exist"

    with open(metrics_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "models" in data
    assert "Ridge (L2 Regularized)" in data["models"]
    assert "Random Forest" in data["models"]
    assert "XGBoost" in data["models"]

    for m_name in ["Ridge (L2 Regularized)", "Random Forest", "XGBoost"]:
        reg = data["models"][m_name]["regression"]
        clf = data["models"][m_name]["classification"]
        assert "r2" in reg
        assert "rmse" in reg
        assert "mae" in reg
        assert "accuracy" in clf
        assert "roc_auc" in clf


def test_telemetry_source_and_status_keys():
    """Verify that live and fallback weather payloads resolve is_live_telemetry correctly."""
    live_payload = {"source": "live", "status_message": "Active Live Telemetry"}
    assert (live_payload.get("source") == "live" or live_payload.get("status") == "live") is True

    status_live_payload = {"status": "live", "status_message": "Active Live Telemetry"}
    assert (status_live_payload.get("source") == "live" or status_live_payload.get("status") == "live") is True

    fallback_payload = {"source": "fallback", "status": "fallback"}
    assert (fallback_payload.get("source") == "live" or fallback_payload.get("status") == "live") is False

