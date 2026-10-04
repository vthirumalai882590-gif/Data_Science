# `src/api/`: Live Weather & Forecast Integration

This package handles communication with external meteorological APIs (Open-Meteo) to fetch real-time weather and 24-hour historical/forecast data for Indian forests.

## Subagent Responsibilities in `src/api/`
- **Weather Client (`weather_client.py`):**
  - Implement resilient HTTP requests to Open-Meteo (`https://api.open-meteo.com/v1/forecast`).
  - Retrieve:
    - Current conditions: `temperature_2m`, `relative_humidity_2m`, `wind_speed_10m`, `precipitation`.
    - Hourly data: Past 24 hours (`past_days=1`) and Next 24 hours.
  - Implement request timeouts (5–10s) and fallback gracefully if the user is offline.
- **Data Harmonization:**
  - Map Open-Meteo JSON responses into `pandas.DataFrame` or structured dictionaries matching the feature names expected by the trained ML models.
- **Forecast Aggregator:**
  - Produce time-series arrays of predicted fire risk across the 24-hour timeline for interactive charting.
