# FIREGUARD X: Explainable Forest Fire Risk Intelligence, Prediction & Simulation Platform

> **Predict. Explain. Simulate. Monitor.**
>
> An intelligent forest-fire risk analysis platform that utilizes historical environmental observations and machine learning to estimate forest-fire vulnerability, explain contributing drivers via SHAP, visualize spatial risk zones, forecast diurnal microclimates, evaluate what-if counterfactual scenarios, detect atmospheric anomalies, and execute an educational fire-spread cellular automaton simulation.

---

## 1. Project Overview
FIREGUARD X is a full-lifecycle, production-quality academic Data Science and Machine Learning platform. Rather than a superficial "input $\rightarrow$ prediction $\rightarrow$ output" demonstration, FIREGUARD X implements and visualizes the complete Data Science lifecycle:

```
Data Collection & Cleaning
           ↓
Exploratory Data Analysis (EDA)
           ↓
Domain Feature Engineering
           ↓
Multiple ML Architectures (Logistic Regression, Decision Tree, Random Forest, XGBoost)
           ↓
Rigorous Stratified Holdout Evaluation & Safety Trade-off Analysis
           ↓
Model Selection (Champion: XGBoost, F1: 0.9655, Recall: 100%)
           ↓
Explainable AI Engine (Localized SHAP Values & Attributions)
           ↓
Environmental Anomaly Detection (Isolation Forest & Multi-Variate Z-Scores)
           ↓
Spatial Risk Intelligence (Leaflet Forest Digital Twin)
           ↓
What-If Counterfactual Laboratory
           ↓
Diurnal Risk Trajectory Forecasting (6h to 72h)
           ↓
Educational Fire Spread Cellular Automaton Simulation
           ↓
Audit Report Generation & SQLite Telemetry Logging
```

---

## 2. Problem Statement
Wildfires cause massive ecological destruction, biodiversity loss, carbon emissions, and endanger human settlements. Rapid changes in surface air temperature, severe relative humidity deficits, and high winds create conditions where combustible leaf litter and surface organic fuels ignite instantaneously. 

Most existing machine learning models operate as uninterpretable black boxes that:
1. Fail to explain *why* risk is high or low.
2. Suffer from silent data corruption due to out-of-bounds sensor readings.
3. Overlook the catastrophic asymmetry between **False Negatives** (unpredicted fires) and **False Positives** (precautionary patrols).
4. Lack counterfactual simulation capabilities to assess how weather interventions alter risk.

---

## 3. Proposed Solution
FIREGUARD X delivers an explainable environmental risk platform that answers six core operational questions:
1. **Where is fire risk high?** → Interactive Leaflet Spatial Risk Map of monitored forest zones.
2. **Why is the risk high?** → Local SHAP (Shapley Additive exPlanations) attribution ranking positive and negative risk contributors.
3. **How could risk change?** → What-If Scenario Lab recalculating associated risk deltas from environmental perturbations.
4. **How might risk evolve?** → Diurnal thermodynamic forecasting projecting 6h, 12h, 24h, 48h, and 72h horizons.
5. **Are current conditions unusual?** → Unsupervised Isolation Forest detecting compound heatwave/drought anomalies.
6. **What happens in an educational fire-spread scenario?** → 2D cellular automaton demonstrating wind vector and fuel dryness propagation dynamics.

---

## 4. Key Features
- **Authentic Data Foundation**: Grounded in the authentic UCI Algerian Forest Fires dataset (243 verified records from Bejaia and Sidi Bel-abbes regions).
- **Multi-Model Benchmark**: Transparent comparative metrics across Logistic Regression, Decision Tree, Random Forest, and XGBoost stored directly in `models/metrics.json`.
- **Zero Fabricated Statistics**: All accuracy, precision, recall, F1, and AUC numbers reflect actual holdout test evaluations.
- **Explainable AI (XAI)**: Directional attributions, magnitude bars, and synthesized natural language narratives.
- **Calibrated Risk Index (0–100)**: Distinguishes statistical class probability from composite environmental vulnerability across 5 standardized tiers (`LOW`, `MODERATE`, `ELEVATED`, `HIGH`, `CRITICAL`).
- **Data Quality Engine**: Pre-flight audit scoring inputs for completeness and physical boundary plausibility.
- **Interactive Spatial Digital Twin**: Real-world geographical coordinates, microclimate conditions, and historical fire incident records.
- **Counterfactual What-If Simulator**: Real-time scenario comparisons with explicit causal disclaimers.
- **Educational Fire Spread Simulation**: 2D cellular automaton with adjustable wind velocity, wind heading, and fuel dryness.
- **Audit Report Generator**: HTML report compilation with downloadable/printable format.
- **Persistent Storage**: SQLite database via SQLAlchemy 2.0 recording prediction logs, zone telemetry, and simulation runs.

---

## 5. Technology Stack
- **Data Science & ML Core**: Python 3.11+, NumPy, Pandas, SciPy, Scikit-learn, XGBoost, SHAP, Joblib, Matplotlib, Seaborn.
- **Backend**: FastAPI, Pydantic V2, SQLAlchemy 2.0, Uvicorn.
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, Leaflet, Lucide React, Recharts.
- **Database**: SQLite (architected for drop-in PostgreSQL migration).
- **DevOps**: Docker, Docker Compose.

---

## 6. Project Structure
```
FIREGUARD-X/
│
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── docker-compose.yml
├── Dockerfile
│
├── data/
│   ├── raw/                 # Authentic UCI Algerian Forest Fires dataset
│   ├── interim/             # Cleaned intermediate records
│   ├── processed/           # Feature-engineered training sets
│   └── README.md
│
├── notebooks/               # Academic Jupyter Notebooks (Phases 1-7)
│   ├── 01_data_loading.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_model_training.ipynb
│   ├── 06_model_evaluation.ipynb
│   └── 07_explainable_ai.ipynb
│
├── ml/
│   ├── config.py            # Paths, seeds, 5-tier risk boundaries
│   ├── preprocessing.py     # Pipeline, imputation, stratified splitting
│   ├── feature_engineering.py # Domain fire-weather indicators
│   ├── train.py             # Multi-model training orchestrator
│   ├── evaluate.py          # Metric calculations & figure generation
│   ├── predict.py           # Risk calculation & data quality engine
│   ├── explain.py           # Local SHAP explainer & narrative generator
│   ├── anomaly.py           # Isolation Forest anomaly detector
│   ├── forecasting.py       # Diurnal trajectory forecasting
│   └── model_registry.py   # Thread-safe artifact caching
│
├── models/                  # Serialized production artifacts
│   ├── model.pkl            # Champion model (XGBoost)
│   ├── all_models.pkl       # All 4 fitted candidate models
│   ├── preprocessor.pkl     # Fitted StandardScaler & metadata
│   ├── anomaly_model.pkl    # Fitted Isolation Forest
│   ├── feature_names.json   # Validated feature list
│   ├── metrics.json         # Real empirical evaluation results
│   └── model_metadata.json  # Provenance & training date
│
├── backend/
│   ├── main.py              # FastAPI entrypoint & lifespan pre-warming
│   ├── config.py            # App settings & CORS
│   ├── api/                 # Endpoints: predict, dashboard, zones, simulation, etc.
│   ├── services/            # Business logic & simulation engines
│   ├── database/            # SQLAlchemy models, SQLite session, repository
│   └── schemas/             # Pydantic V2 input/output schemas
│
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI cards, gauges, maps, tables
│   │   ├── pages/           # Command Center, Map, Prediction, Forecast, etc.
│   │   ├── services/        # Typed API communication layer (api.ts)
│   │   ├── types/           # TypeScript interfaces
│   │   └── App.tsx          # Main application & routing state
│   ├── vite.config.ts
│   └── package.json
│
├── tests/                   # Pytest test suite (17 passed tests)
│   ├── test_preprocessing.py
│   ├── test_prediction.py
│   ├── test_risk.py
│   ├── test_simulation.py
│   ├── test_api.py
│   └── test_database.py
│
├── reports/
│   ├── figures/             # Auto-generated ROC, Confusion, & Feature plots
│   └── generated/           # Compiled printable HTML reports
│
└── docs/                    # Academic Documentation
    ├── architecture.md
    ├── data_dictionary.md
    ├── ml_methodology.md
    ├── api_documentation.md
    └── deployment.md
```

---

## 7. Dataset & Preprocessing
The platform uses the **Algerian Forest Fires Dataset** from the UCI Machine Learning Repository:
- **Regions**: Bejaia Region (Coastal Mediterranean) and Sidi Bel-abbes Region (Inland Steppe).
- **Instances**: 243 validated observations across 15 attributes.
- **Target Distribution**: Fire: 137 (56.4%) | Not Fire: 106 (43.6%).
- **Cleaning**: Whitespace stripped from column headers and class tags, numeric values cast from text representations, and zero missing values in primary features.

---

## 8. Domain Feature Engineering
In addition to raw weather and Canadian Fire Weather Index components, the following features were engineered:
1. `temp_rh_ratio`: $\frac{\text{Temperature}}{\text{RH} + 10^{-4}}$ (compounding heat-dryness desiccation factor).
2. `dryness_index`: $\frac{(100 - \text{RH}) \times \text{Temperature}}{100.0}$ (atmospheric evapotranspiration pressure on fine surface fuels).
3. `wind_temp_interaction`: $\text{Ws} \times \text{Temperature}$ (convective thermal advection).
4. `rain_deficit`: $\frac{1}{\text{Rain} + 0.1}$ (inverse moisture suppression index).
5. `ffmc_isi_ratio`: $\frac{\text{ISI}}{\text{FFMC} + 10^{-4}}$ (flame spread potential relative to fine fuel moisture).

---

## 9. Machine Learning Evaluation & Model Selection

Trained with a **Stratified 80/20 Train-Test Partition** (194 training instances, 49 holdout test instances, seed 42):

| Candidate Architecture | Accuracy | Precision | Recall (Sensitivity) | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (L2)** | 95.92% | 96.43% | 96.43% | 0.9643 | 0.9932 |
| **Decision Tree (depth=5)** | 93.88% | 90.32% | 100.00% | 0.9492 | 0.9949 |
| **Random Forest (150 trees)** | 93.88% | 90.32% | 100.00% | 0.9492 | 1.0000 |
| **XGBoost (Champion)** | **95.92%** | **93.33%** | **100.00%** | **0.9655** | **0.9983** |

*All metrics generated dynamically from `models/metrics.json`.*

### Why XGBoost was selected:
In wildfire detection, **False Negatives** (failing to predict an active fire) carry catastrophic consequences. XGBoost delivered **100.00% Recall** on test data (zero missed fires) alongside the highest overall **F1-Score (0.9655)**.

---

## 10. Installation & Local Execution

### Backend
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Acquire authentic UCI dataset & train models
python scripts/prepare_dataset.py
python ml/train.py

# 3. Launch FastAPI server
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/api/health`

### Frontend
```bash
# In another terminal:
cd frontend
npm install
npm run dev
```
- Application: `http://localhost:5173`

### Run Automated Test Suite
```bash
python -m pytest -v
```
*(All 17 tests covering ML preprocessing, inference, risk engine, CA simulation, SQLite repository, and FastAPI endpoints pass).*

---

## 11. Docker Execution
```bash
docker-compose up --build -d
```

---

## 12. Responsible AI & Academic Disclaimer
1. **Probabilistic Nature**: Fire risk scores represent statistical estimations of microclimate vulnerability and fuel drying potential, not deterministic physical guarantees.
2. **Geographic Scope**: Models were calibrated on Mediterranean and North African forest ecosystems; transfer to other biomes requires local re-training.
3. **Educational Simulation**: The 2D cellular automaton fire-spread simulator is strictly intended for educational demonstrations of wind-dryness propagation dynamics and **must not be used for operational emergency response or evacuation routing**.

---

## 13. License
Academic MIT License. Developed for research and educational purposes.
