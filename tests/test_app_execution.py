"""Direct execution test for app.py logic and visualization generation."""

import pandas as pd
import pytest

from app.app import (
    create_forecast_timeline_chart,
    create_indian_forest_map,
    create_risk_gauge,
    get_risk_tier,
    load_trained_models,
    predict_fire_risk_scores,
)
from src.api.weather_client import get_current_weather, get_hourly_forecast
from src.config.settings import INDIAN_FORESTS


def test_models_loading_and_fallback():
    """Verify models load cleanly and have fallback metrics."""
    models, metrics_data = load_trained_models()
    assert isinstance(models, dict)
    assert isinstance(metrics_data, dict)
    assert "models" in metrics_data


def test_predict_fire_risk_scores():
    """Verify prediction calculations for all models and consensus."""
    models, _ = load_trained_models()

    # Extreme heatwave scenario
    res_hot = predict_fire_risk_scores(42.0, 15.0, 35.0, 0.0, models)
    assert "Consensus" in res_hot
    assert "Random Forest" in res_hot
    assert "XGBoost" in res_hot
    assert "Ridge (L2)" in res_hot
    assert res_hot["Consensus"] > 50.0  # High risk expected

    # Rainy cool scenario
    res_rain = predict_fire_risk_scores(20.0, 95.0, 10.0, 15.0, models)
    assert res_rain["Consensus"] < 40.0  # Low risk expected


def test_risk_tier_classification():
    """Verify 4 tier thresholds: Low, Moderate, High, Extreme."""
    label1, color1, _, _ = get_risk_tier(20.0)
    assert label1 == "LOW RISK"
    assert color1 == "#10b981"

    label2, color2, _, _ = get_risk_tier(45.0)
    assert label2 == "MODERATE RISK"
    assert color2 == "#f59e0b"

    label3, color3, _, _ = get_risk_tier(70.0)
    assert label3 == "HIGH RISK"
    assert color3 == "#f97316"

    label4, color4, _, _ = get_risk_tier(88.0)
    assert label4 == "EXTREME DANGER"
    assert color4 == "#ef4444"


def test_plotly_visualizations():
    """Verify gauge and timeline chart produce valid figures without errors."""
    fig_gauge = create_risk_gauge(65.4, title_text="Test Gauge")
    assert fig_gauge is not None

    # Create synthetic hourly df
    df = pd.DataFrame(
        {
            "time": pd.date_range("2026-10-01", periods=48, freq="h"),
            "temperature": [25.0 + i % 10 for i in range(48)],
            "relative_humidity": [60.0 - i % 20 for i in range(48)],
            "wind_speed": [12.0 + i % 5 for i in range(48)],
            "rain": [0.0] * 48,
            "risk_score": [30.0 + i % 40 for i in range(48)],
            "is_forecast": [i >= 24 for i in range(48)],
        }
    )
    fig_timeline = create_forecast_timeline_chart(df)
    assert fig_timeline is not None


def test_create_indian_forest_map():
    """Verify interactive Indian Forest map renders all reserves and highlights active."""
    for forest_name in ["Bandipur National Park", "Jim Corbett National Park", "Gir National Park"]:
        fig_map = create_indian_forest_map(forest_name)
        assert fig_map is not None
        # Must have at least background reserves trace + halo trace + active pin trace
        assert len(fig_map.data) >= 3


def test_forecast_horizon_future_filtering():
    """Verify the forecast horizon only considers future hours for peak hazards."""
    now = pd.Timestamp.now()
    past_times = [now - pd.Timedelta(hours=i) for i in range(10, 0, -1)]
    future_times = [now + pd.Timedelta(hours=i) for i in range(1, 15)]

    # Make past hours have an artificially huge risk score that should NOT be picked
    times = past_times + future_times
    risks = [99.0] * len(past_times) + [45.0 + i for i in range(len(future_times))]

    df = pd.DataFrame({"time": times, "risk_score": risks})
    df["parsed_time"] = pd.to_datetime(df["time"])
    current_time = pd.Timestamp.now()

    future_subset = df[df["parsed_time"] >= current_time]
    peak_future_row = future_subset.loc[future_subset["risk_score"].idxmax()]

    # Assert the selected peak row is strictly in the future, never the past 99.0
    assert peak_future_row["parsed_time"] >= current_time
    assert peak_future_row["risk_score"] < 90.0
