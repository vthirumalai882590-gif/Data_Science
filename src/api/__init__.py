"""API package for external weather and meteorological integrations."""

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

__all__ = [
    "get_current_weather",
    "get_hourly_forecast",
    "get_forest_weather",
    "aggregate_forest_risk_forecast",
    "resolve_forest_name",
    "get_mock_current_weather",
    "get_mock_hourly_weather",
    "get_regional_baseline",
    "predict_point_risk",
    "validate_coordinates",
    "validate_weather_data",
    "validate_forecast_dataframe",
    "PHYSICAL_LIMITS",
]
