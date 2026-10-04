# `app/`: Streamlit Dashboard & Web Interface

This directory contains the user-facing web dashboard built with Streamlit and Plotly.

## Application Features & Tabs
1. **Live Indian Forest Monitor:**
   - Interactive dropdown / map of Indian forests (Bandipur, Corbett, Simlipal, Gir, Kanha, etc.).
   - Instant live weather data retrieval from Open-Meteo API.
   - Fire risk dial / gauge with danger classification (Low / Moderate / High / Extreme).
2. **24-Hour Weather & Fire Risk Forecast:**
   - Line chart tracking temperature, humidity, wind, and the predicted fire risk curve hour-by-hour (past 24h + next 24h).
3. **Model Benchmark & Comparison:**
   - Visual charts comparing Ridge (L2), Random Forest, and XGBoost on test metrics ($R^2$, RMSE, MAE).
4. **Interactive What-If Weather Simulator:**
   - Sliders for Temperature, Humidity, Wind Speed, and Rain to simulate custom extreme weather scenarios.

## Subagent Responsibilities in `app/`
- Keep UI fast, responsive, and aesthetically polished.
- Handle API failures gracefully (display a friendly warning if the network times out).
- Run locally via `streamlit run app/app.py`.
