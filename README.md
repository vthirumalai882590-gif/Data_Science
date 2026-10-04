# Forest Fire Predictor & Real-Time Monitoring System

An end-to-end Machine Learning project that predicts forest fire risk and burnt area using meteorological conditions, compares regularized linear models (Ridge L2) with ensemble and gradient boosting algorithms (Random Forest, XGBoost), and connects to live weather APIs for prominent forests across India.

---

## Project Structure Overview

```text
.
├── README.md                 # Project vision, architecture, and orchestration guidelines
├── requirements.txt          # Python dependencies
├── .gitignore                # Ignored cache, virtual environments, and large binaries
├── data/                     # Data storage (raw, processed) with strict schema guidelines
│   ├── raw/                  # Immutable original datasets (UCI, NASA, etc.)
│   └── processed/            # Cleaned, standardized, ready-to-train datasets
├── notebooks/                # Exploratory Data Analysis (EDA) and experimental prototypes
├── src/                      # Production-grade Python modular source code
│   ├── config/               # Indian forest coordinates, API endpoints, hyperparameters
│   ├── data/                 # Ingestion, validation, and cleaning pipelines
│   ├── features/             # FWI calculations, scaling, encoding pipelines
│   ├── models/               # Model training (Ridge, RF, XGBoost), evaluation, tuning
│   ├── api/                  # Open-Meteo live weather client & 24-hr forecast service
│   └── utils/                # Logging, serialization, and metric helpers
├── models/                   # Persisted model artifacts (.joblib), metadata, and benchmarks
├── app/                      # Interactive Streamlit dashboard (India Live Risk & Forecast)
└── tests/                    # Automated unit tests for data schemas and model inference
```

---

## Subagent Orchestration & Role Directory Guide

If you are an AI subagent or developer operating inside this repository, refer to the individual `README.md` inside each folder for your specific scope, constraints, and responsibilities:

| Folder | Domain / Subagent Role | Key Responsibility |
|---|---|---|
| [`data/`](file:///Users/sreekanth/Desktop/DataScience/data/README.md) | **Data Ingestion & Integrity** | Acquire, validate, and isolate raw vs. processed datasets. Ensure balance of fire vs. normal days. |
| [`src/config/`](file:///Users/sreekanth/Desktop/DataScience/src/config/README.md) | **Configuration Specialist** | Manage preset coordinates of Indian forests, API endpoints, random seeds, and thresholds. |
| [`src/data/`](file:///Users/sreekanth/Desktop/DataScience/src/data/README.md) | **Data Cleaning Specialist** | Parse raw CSVs, handle missing values, strip whitespace, enforce numeric schemas. |
| [`src/features/`](file:///Users/sreekanth/Desktop/DataScience/src/features/README.md) | **Feature Engineer** | Standard/Robust scalers, FWI components, skewness handling (`np.log1p`). |
| [`src/models/`](file:///Users/sreekanth/Desktop/DataScience/src/models/README.md) | **ML Modeling Engineer** | Train and benchmark Ridge (L2), Random Forest, and XGBoost with Stratified CV. |
| [`src/api/`](file:///Users/sreekanth/Desktop/DataScience/src/api/README.md) | **External API Integrator** | Fetch live weather and 24-hour historical/future forecast from Open-Meteo API. |
| [`models/`](file:///Users/sreekanth/Desktop/DataScience/models/README.md) | **Model Registry / MLOps** | Save and load serialized `.joblib` pipelines and JSON performance metrics. |
| [`app/`](file:///Users/sreekanth/Desktop/DataScience/app/README.md) | **UI / Dashboard Developer** | Build the Streamlit dashboard with risk gauges, Indian forest map/selector, and forecast charts. |
| [`tests/`](file:///Users/sreekanth/Desktop/DataScience/tests/README.md) | **QA & Test Engineer** | Enforce test coverage on API latency, data ranges, and model inference contracts. |
