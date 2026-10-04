# Notebooks Directory: Guidelines & Structure

This directory holds Jupyter notebooks used for initial exploratory data analysis (EDA), visual inspections, and prototyping ML models before porting code to `src/`.

## Recommended Notebook Flow
1. `01_exploratory_data_analysis.ipynb`:
   - Inspect distributions of weather features (Temp, RH, Wind, Rain).
   - Correlation heatmaps between weather parameters and fire occurrence / FWI index.
   - Analysis of fire vs. non-fire day contrasts (boxplots and violin plots).
2. `02_model_experimentation.ipynb`:
   - Baseline linear regression with L2 regularization (Ridge).
   - Random Forest Regressor & feature importances.
   - XGBoost Regressor tuning and residual error analysis.
3. `03_live_weather_api_test.ipynb`:
   - Prototyping API requests to Open-Meteo for Indian forest coordinates.

## Subagent Responsibilities in `notebooks/`
- Keep notebooks modular, well-commented, and runnable top-to-bottom without manual hacks.
- Clear cell outputs if saving large visual data to avoid bloating git commits.
- All core functions defined in notebooks should eventually be factored into clean, reusable modules inside `src/`.
