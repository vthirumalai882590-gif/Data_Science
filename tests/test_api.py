"""Unit and integration test suite for Open-Meteo live weather client.

Tests schema contracts, physical limit boundaries, fuzzy forest lookup,
status provenance, network failure resilience, regional baselines,
true 24-hour rolling horizon, and forecast risk aggregation.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import pytest
import requests

from src.api.weather_client import (
    PHYSICAL_LIMITS,
    aggregate_forest_risk_forecast,
    get_current_weather,
    get_forest_weather,
    get_hourly_forecast,
    get_mock_current_weather,
    get_mock_hourly_weather,
    get_regional_baseline,
    predict_point_risk,
    resolve_forest_name,
    validate_coordinates,
    validate_forecast_dataframe,
    validate_weather_data,
)
from src.config.settings import INDIAN_FORESTS


class TestCoordinateValidation:
    """Test geographical coordinate range enforcement."""

    def test_valid_coordinates(self):
        validate_coordinates(11.6667, 76.6333)
        validate_coordinates(0.0, 0.0)
        validate_coordinates(-90.0, -180.0)
        validate_coordinates(90.0, 180.0)

    def test_invalid_latitude(self):
        with pytest.raises(ValueError, match="Latitude"):
            validate_coordinates(95.0, 76.6333)
        with pytest.raises(ValueError, match="Latitude"):
            validate_coordinates(-90.1, 76.6333)

    def test_invalid_longitude(self):
        with pytest.raises(ValueError, match="Longitude"):
            validate_coordinates(11.6667, 185.0)
        with pytest.raises(ValueError, match="Longitude"):
            validate_coordinates(11.6667, -180.5)


class TestPhysicalLimitsValidation:
    """Test meteorological physical bounds checks."""

    def test_valid_weather_data(self):
        valid = {
            "temperature": 28.5,
            "relative_humidity": 65.0,
            "wind_speed": 12.0,
            "rain": 0.0,
            "timestamp": "2026-10-02T12:00",
            "source": "live",
        }
        assert validate_weather_data(valid) is True

    def test_missing_weather_key(self):
        incomplete = {
            "temperature": 28.5,
            "relative_humidity": 65.0,
            "wind_speed": 12.0,
            # missing rain & timestamp
        }
        with pytest.raises(ValueError, match="Missing required key"):
            validate_weather_data(incomplete)

    def test_temperature_out_of_bounds(self):
        too_hot = {
            "temperature": 75.0,  # Exceeds max 60°C
            "relative_humidity": 50.0,
            "wind_speed": 10.0,
            "rain": 0.0,
            "timestamp": "2026-10-02T12:00",
        }
        with pytest.raises(ValueError, match="outside physical limits"):
            validate_weather_data(too_hot)

    def test_humidity_out_of_bounds(self):
        negative_humidity = {
            "temperature": 25.0,
            "relative_humidity": -5.0,
            "wind_speed": 10.0,
            "rain": 0.0,
            "timestamp": "2026-10-02T12:00",
        }
        with pytest.raises(ValueError, match="outside physical limits"):
            validate_weather_data(negative_humidity)

    def test_valid_forecast_dataframe(self):
        df = pd.DataFrame({
            "time": ["2026-10-01T00:00", "2026-10-01T01:00"],
            "temperature": [22.0, 23.5],
            "relative_humidity": [80.0, 75.0],
            "wind_speed": [5.0, 7.5],
            "rain": [0.0, 0.2],
        })
        assert validate_forecast_dataframe(df) is True

    def test_invalid_forecast_dataframe_missing_column(self):
        df = pd.DataFrame({
            "time": ["2026-10-01T00:00"],
            "temperature": [22.0],
        })
        with pytest.raises(ValueError, match="missing required columns"):
            validate_forecast_dataframe(df)


class TestForestResolution:
    """Test fuzzy and case-insensitive forest name resolution."""

    def test_exact_match(self):
        assert resolve_forest_name("Bandipur National Park") == "Bandipur National Park"
        assert resolve_forest_name("Jim Corbett National Park") == "Jim Corbett National Park"

    def test_case_insensitive_match(self):
        assert resolve_forest_name("bandipur national park") == "Bandipur National Park"
        assert resolve_forest_name("GIR NATIONAL PARK") == "Gir National Park"

    def test_substring_match(self):
        assert resolve_forest_name("Bandipur") == "Bandipur National Park"
        assert resolve_forest_name("Corbett") == "Jim Corbett National Park"
        assert resolve_forest_name("Kaziranga") == "Kaziranga National Park"

    def test_unknown_forest_raises_key_error(self):
        with pytest.raises(KeyError, match="not found in INDIAN_FORESTS"):
            resolve_forest_name("Sherwood Forest")


class TestStatusProvenanceAndResilience:
    """Test source provenance tracking ('live' vs 'fallback') and offline resilience."""

    @patch("src.api.weather_client._SESSION.get")
    def test_current_weather_fallback_under_simulated_timeout(self, mock_get):
        """Verify source == 'fallback' and status_message set when simulated timeout occurs."""
        mock_get.side_effect = requests.Timeout("Connection timed out after 5000ms")

        # Fallback enabled: should safely return fallback dictionary without crashing
        data = get_current_weather(
            latitude=29.5300,
            longitude=78.7747,
            fallback_on_error=True,
        )

        assert isinstance(data, dict)
        assert data["source"] == "fallback"
        assert data["status_message"] == "Offline / Using Climatological Baseline"
        assert validate_weather_data(data) is True
        assert all(k in data for k in ["temperature", "relative_humidity", "wind_speed", "rain", "timestamp"])

    @patch("src.api.weather_client._SESSION.get")
    def test_current_weather_raises_when_fallback_disabled(self, mock_get):
        """Verify exception is re-raised when fallback_on_error is False."""
        mock_get.side_effect = requests.Timeout("Network timed out")

        with pytest.raises(requests.Timeout):
            get_current_weather(
                latitude=20.0,
                longitude=80.0,
                fallback_on_error=False,
            )

    @patch("src.api.weather_client._SESSION.get")
    def test_hourly_forecast_fallback_on_server_error(self, mock_get):
        """Verify 48-hour continuous rolling fallback is returned on HTTP 503."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("503 Service Unavailable")
        mock_get.return_value = mock_response

        df = get_hourly_forecast(
            latitude=20.0,
            longitude=80.0,
            fallback_on_error=True,
        )
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 48
        assert validate_forecast_dataframe(df) is True
        expected_cols = ["time", "temperature", "relative_humidity", "wind_speed", "rain"]
        assert list(df.columns) == expected_cols

    def test_regional_baselines_tailored_by_coordinates(self):
        """Verify regional climatological baselines reflect distinct Indian biospheres."""
        corbett_base = get_regional_baseline(29.53, 78.77)  # Himalayan foothills
        gir_base = get_regional_baseline(21.12, 70.82)      # Kathiawar / Arid
        kaziranga_base = get_regional_baseline(26.57, 93.17) # Brahmaputra

        # Corbett should be cooler than arid Gir
        assert corbett_base["temperature"] < gir_base["temperature"]
        # Kaziranga floodplains should be more humid than arid Gir
        assert kaziranga_base["relative_humidity"] > gir_base["relative_humidity"]


class TestLiveWeatherIntegration:
    """Integration test against live Open-Meteo API for Indian Forests."""

    def test_live_current_weather_source_is_live(self):
        """Verify source == 'live' when querying Open-Meteo online."""
        lat = INDIAN_FORESTS["Bandipur National Park"]["latitude"]
        lon = INDIAN_FORESTS["Bandipur National Park"]["longitude"]

        weather = get_current_weather(lat, lon, timeout=5.0)

        assert isinstance(weather, dict)
        assert weather["source"] == "live"
        assert "Active" in weather.get("status_message", "")
        assert validate_weather_data(weather) is True
        assert 5.0 <= weather["temperature"] <= 50.0
        assert 0.0 <= weather["relative_humidity"] <= 100.0

    def test_live_hourly_forecast_rolling_48_hours(self):
        """Verify get_hourly_forecast returns true continuous 48-hour rolling window."""
        lat = INDIAN_FORESTS["Jim Corbett National Park"]["latitude"]
        lon = INDIAN_FORESTS["Jim Corbett National Park"]["longitude"]

        df = get_hourly_forecast(lat, lon, past_days=1, forecast_days=2, timeout=5.0)

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 48  # Exactly 48 continuous rolling hours
        expected_cols = ["time", "temperature", "relative_humidity", "wind_speed", "rain"]
        assert list(df.columns) == expected_cols
        assert validate_forecast_dataframe(df) is True

        # Check temporal continuity: consecutive timestamps must be exactly 1 hour apart
        times = pd.to_datetime(df["time"])
        diffs = times.diff().dropna()
        assert (diffs == pd.Timedelta(hours=1)).all(), "Hourly forecast timestamps must be continuous 1-hour intervals"

    def test_live_get_forest_weather_convenience(self):
        result = get_forest_weather("Bandipur National Park", timeout=5.0)

        assert result["forest_name"] == "Bandipur National Park"
        assert result["current"]["source"] == "live"
        assert isinstance(result["hourly_forecast"], pd.DataFrame)
        assert len(result["hourly_forecast"]) == 48


class TestForecastAggregator:
    """Test aggregate_forest_risk_forecast and consensus scoring."""

    def test_aggregate_forest_risk_forecast_structure(self):
        """Verify aggregator enriches DataFrame with risk_score and is_forecast."""
        df = aggregate_forest_risk_forecast("Bandipur National Park", models={})

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 48

        # Required columns
        expected_cols = [
            "time",
            "temperature",
            "relative_humidity",
            "wind_speed",
            "rain",
            "is_forecast",
            "risk_score",
        ]
        for col in expected_cols:
            assert col in df.columns, f"Missing required column '{col}' in aggregated forecast"

        # Check is_forecast boolean split
        assert df["is_forecast"].dtype == bool
        past_hours = (~df["is_forecast"]).sum()
        future_hours = df["is_forecast"].sum()
        assert past_hours > 0, "Aggregated forecast must contain past hours"
        assert future_hours > 0, "Aggregated forecast must contain future hours"
        assert past_hours + future_hours == 48

        # Check risk_score bounds
        assert (df["risk_score"] >= 0.0).all()
        assert (df["risk_score"] <= 100.0).all()
        assert not df["risk_score"].isnull().any()

    def test_predict_point_risk_responsiveness(self):
        """Verify analytical risk prediction responds correctly to hot/dry vs cool/wet conditions."""
        hot_dry_risk = predict_point_risk(
            temperature=42.0,
            relative_humidity=15.0,
            wind_speed=30.0,
            rain=0.0,
            models={},
        )
        cool_wet_risk = predict_point_risk(
            temperature=18.0,
            relative_humidity=90.0,
            wind_speed=5.0,
            rain=10.0,
            models={},
        )

        assert hot_dry_risk > 50.0, f"Expected high risk in heatwave, got {hot_dry_risk}"
        assert cool_wet_risk < 30.0, f"Expected low risk in rain, got {cool_wet_risk}"
        assert hot_dry_risk > cool_wet_risk
