# `src/features/`: Feature Engineering & Transformation Pipelines

This package prepares features for Machine Learning algorithms, handling scaling, mathematical transformations, and alignment between historical datasets and live weather APIs.

## Subagent Responsibilities in `src/features/`
- **Feature Transformers (`transformers.py`):**
  - Implement `scikit-learn` compatible transformers (`ColumnTransformer`, `StandardScaler`, `RobustScaler`).
  - Handle extreme skewness in regression targets (e.g. logarithmic transformation $y' = \log(1 + y)$ and inverse transform $\exp(y') - 1$).
- **API Feature Alignment:**
  - Ensure features required by the trained model (e.g., `temperature`, `relative_humidity`, `wind_speed`, `rain`) match the exact unit formats produced by the Open-Meteo live API.
  - Temperature in °C, Relative Humidity in %, Wind Speed in km/h, Rain/Precipitation in mm.
- **Pipeline Serialization:**
  - Persist fitted scalers and preprocessors together with model pipelines so raw input can be directly passed during inference.
