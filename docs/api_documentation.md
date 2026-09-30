# FIREGUARD X — REST API Documentation

Base URL: `http://localhost:8000/api`

Interactive OpenAPI Documentation: `http://localhost:8000/docs`

---

### Endpoints Overview

#### 1. System Health
- **`GET /api/health`**
  - Returns service status, loaded model name, and operational timestamp.

#### 2. Command Center Dashboard
- **`GET /api/dashboard`**
  - Returns fleet-wide average risk, active zones count, high-risk count, critical count, anomalous zones, risk distribution, and top 5 risk zones.

#### 3. Spatial Digital Twin Zones
- **`GET /api/zones`**
  - Returns list of all monitored forest zones with coordinates, latest weather parameters, and risk scores.
- **`GET /api/zones/{zone_id}`**
  - Returns specific zone details.
- **`GET /api/forecast/{zone_id}`**
  - Returns diurnal projected risk horizons (T+6h, T+12h, T+24h, T+48h, T+72h) and escalation status.

#### 4. Prediction & Explainable AI
- **`POST /api/predict`**
  - Input: Meteorological and environmental parameters.
  - Output: Risk score (0-100), qualitative tier, model probability, data quality assessment, anomaly evaluation, SHAP drivers, and explanation narrative.
- **`POST /api/explain`**
  - Input: Meteorological parameters.
  - Output: SHAP baseline value, feature contributions, and plain-language explanation.
- **`POST /api/what-if`**
  - Input: Baseline conditions + modified conditions.
  - Output: Comparative risk delta, direction, and primary drivers of risk change.
- **`GET /api/predictions/history`**
  - Returns previous prediction runs stored in the database.

#### 5. Educational Fire Spread Simulator
- **`POST /api/simulation`**
  - Input: Starting zone, wind speed, wind direction, dryness, duration.
  - Output: Cellular automaton time-step frames (T+0 to T+24), cell states (`SAFE`, `AT_RISK`, `SIMULATED_FIRE`, `AFFECTED`), cell intensities, and educational disclaimer.

#### 6. Model Laboratory & Metrics
- **`GET /api/model/metrics`**
  - Returns authentic training evaluation metrics for all 4 models from `models/metrics.json`.
- **`GET /api/model/features`**
  - Returns engineered and core features with human-readable descriptions.
- **`GET /api/model/metadata`**
  - Returns model provenance, training date, target, and hyperparameters.

#### 7. Audit Reports
- **`POST /api/reports/generate`**
  - Generates HTML/print audit report and stores snapshot.
- **`GET /api/reports`**
  - Returns list of generated reports.
- **`GET /api/reports/{id}/view`**
  - Renders standalone HTML report for printing or PDF export.
