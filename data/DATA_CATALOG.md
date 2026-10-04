# Forest Fire Predictor — Comprehensive Data Catalog & Data Science Reference Guide

This reference document serves as the single source of truth for all data sources, schemas, validation functions, diagnostic commands, and methodological rationales used in the **Forest Fire Predictor** project.

---

## 1. Quick Diagnostic Toolkit: Essential Inspection Commands

When auditing, loading, or presenting data during reviews and project defenses, run and refer to these standard Python and pandas evaluation functions:

```python
import pandas as pd
import numpy as np

# 1. Structural Dimensions
print("Dataset Dimensions (Rows, Columns):", df.shape)
print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))
print("Column Names:", df.columns.tolist())

# 2. Data Types, Memory & Non-Null Audit
df.info(memory_usage="deep")
print("\nExplicit Data Types:\n", df.dtypes)

# 3. Missing Values & Hygiene Verification
missing_summary = pd.DataFrame({
    "Missing_Count": df.isnull().sum(),
    "Missing_Percentage": (df.isnull().sum() / len(df)) * 100
})
print("\nMissing Value Audit:\n", missing_summary)

# 4. Five-Number Summary & Statistical Distributions
print("\nDescriptive Statistics (Numeric Features):\n", df.describe().T)

# 5. Target Variable Class Balance & Distribution (Critical Verification)
# For Binary Classification (e.g. FIRE_RISK or Classes):
print("\nTarget Class Counts:\n", df["target"].value_counts(dropna=False))
print("\nTarget Class Proportions (%):\n", df["target"].value_counts(normalize=True) * 100)

# 6. Physical Boundary Assertions (Domain Validation)
assert (df["relative_humidity"] >= 0).all() and (df["relative_humidity"] <= 100).all(), "RH out of range [0, 100]%"
assert (df["precipitation"] >= 0).all(), "Precipitation must be non-negative"
assert (df["temperature"] >= -15).all() and (df["temperature"] <= 55).all(), "Temperature outside physical limits"

# 7. Distribution Skewness & Target Transformation Check
print("\nFeature Skewness:\n", df.select_dtypes(include=[np.number]).skew())
# For right-skewed regression targets (such as burnt area in hectares):
# Apply log transform: y_trans = np.log1p(y)

# 8. Collinearity & Feature Correlation Audit
corr_matrix = df.select_dtypes(include=[np.number]).corr()
print("\nCorrelation with Target:\n", corr_matrix["target"].sort_values(ascending=False))
```

---

## 2. In-Depth Dataset Briefs

---

### Dataset 1: Quebec Wildfire Prediction Dataset (2018–2024)
*   **Role in Project:** **Primary Engine — Ignition Risk Classifier**
*   **Repository / Origin:** Kaggle (Engineered from SOPFEU Quebec Provincial Fire Logs and Open-Meteo ERA5 Reanalysis Archive)
*   **Exact Dimensions:**
    *   **Rows:** Exactly 9,000 instances
    *   **Columns:** 11 features
    *   **File Size:** Approximately 336 KB (CSV)
*   **Target Variable & Nature of Task:**
    *   `FIRE_RISK` — Binary Classification
    *   `1` = Wildfire Ignition Event
    *   `0` = Safe / Normal Day (Pseudo-absence control day)
*   **Class Distribution & Negative Control Balance:**
    *   Confirmed Ignition Events (`FIRE_RISK = 1`): 4,500 rows (50.00%)
    *   Safe Control Days (`FIRE_RISK = 0`): 4,500 rows (50.00%)
    *   *Quality Rating:* Perfect 1:1 balance. Completely prevents selection and survivorship bias.
*   **Complete Feature Schema:**
    1.  `DATE_DEBUT` (Timestamp / Date of observation, May through September)
    2.  `LATITUDE` (Decimal degrees, geographic coordinate)
    3.  `LONGITUDE` (Decimal degrees, geographic coordinate)
    4.  `MONTH` (Categorical / Integer 5 to 9, active fire season)
    5.  `MAX_TEMP` (Daily maximum temperature in degrees Celsius)
    6.  `MIN_HUMIDITY` (Daily minimum relative humidity percentage)
    7.  `WIND_SPEED` (Daily maximum wind speed in km/h)
    8.  `PRECIPITATION` (Total daily rainfall in mm)
    9.  `14_DAY_RAIN` (Cumulative rainfall over the preceding 14 days in mm)
    10. `14_DAY_AVG_TEMP` (Rolling average maximum temperature over the preceding 14 days in degrees Celsius)
    11. `DAYS_SINCE_RAIN` (Consecutive dry days without significant precipitation, 0 to 14)
*   **Data Quality & Preprocessing Protocol:**
    *   Missing Values: 0 nulls across all 9,000 rows.
    *   Data Types: Clean numeric floats and integers.
    *   Transformation Needs: Standard scaling (`StandardScaler`) required on meteorological variables prior to Ridge classification.
*   **Why It Was Selected:**
    *   Native compatibility with the Open-Meteo API. The weather parameters correspond 1:1 with live API outputs.
    *   The 14-day rolling drought memory accurately captures cumulative dryness, which is a primary driver of seasonal Indian forest fires.

---

### Dataset 2: The Extended Algerian Forest Fires Dataset (9 Regions)
*   **Role in Project:** **Secondary Engine — Fire Severity & FWI Score Regressor**
*   **Repository / Origin:** Mendeley Data (DOI: 10.17632/8rkd9cdgs5.1, Faroudja Abid et al.)
*   **Exact Dimensions:**
    *   **Rows:** 1,215 instances (aggregates 971 new regional instances with the original 244-row benchmark)
    *   **Columns:** 12 features
    *   **File Size:** Approximately 95 KB (CSV)
*   **Target Variables & Problem Types:**
    *   *Regression Target (Primary):* `FWI` (Fire Weather Index score, continuous numerical metric)
    *   *Classification Target (Secondary):* `Classes` (Binary: `fire` vs. `not fire`)
*   **Class Distribution & Negative Control Balance:**
    *   `fire` days: 633 rows (52.10%)
    *   `not fire` days: 582 rows (47.90%)
    *   *Quality Rating:* Balanced split across 9 diverse climate regions and multiple fire seasons.
*   **Complete Feature Schema:**
    1.  `Date` (Day, month, year across fire seasons in 2012, 2017, and 2021)
    2.  `Region` (Categorical: Tizi Ouzou, Bejaia, Bouira, Khenchela, Tiaret, Setif, Blida, Sidi-Bel-Abbess, Tipaza)
    3.  `Temperature` (Noon maximum temperature in degrees Celsius, 20°C to 45°C)
    4.  `RH` (Relative Humidity percentage, 20% to 92%)
    5.  `Ws` / `Wind Speed` (Wind velocity in km/h, 6 to 30 km/h)
    6.  `Rain` (Outside precipitation in mm/m², 0.0 to 18.0 mm)
    7.  `FFMC` (Fine Fuel Moisture Code: litter and fine fuel ignition ease, 28.0 to 96.0)
    8.  `DMC` (Duff Moisture Code: decomposition layer fuel moisture, 1.0 to 295.0)
    9.  `DC` (Drought Code: deep organic sub-surface moisture, 7.0 to 860.0)
    10. `ISI` (Initial Spread Index: rate of fire spread potential, 0.0 to 56.0)
    11. `BUI` (Buildup Index: total fuel available for combustion, 1.0 to 300.0)
    12. `FWI` (Fire Weather Index: overall fire intensity rating, 0.0 to 35.0+)
*   **Data Quality & Preprocessing Protocol:**
    *   Stripping whitespace padding from class strings.
    *   Casting all numeric columns to `float64`.
    *   Handling severe multicollinearity: `FFMC`, `DMC`, `DC`, and `ISI` are mathematical derivations of `Temperature`, `RH`, `Wind`, and `Rain`. Ridge regression (L2 regularization) is specifically employed to shrink these correlated coefficients and stabilize the model.
*   **Why It Was Selected:**
    *   Provides an ideal testbed for L2 regularized regression on continuous fire risk indices.
    *   Open-Meteo maintains an active FWI endpoint that outputs these exact Canadian components for any coordinate in India.

---

### Dataset 3: Montesinho Natural Park Forest Fires Dataset (Portugal)
*   **Role in Project:** **Benchmark Regression Comparison (Burnt Area)**
*   **Repository / Origin:** UCI Machine Learning Repository (DOI: 10.24432/C5D88D, Cortez & Morais, 2007) / OpenML ID: 42363
*   **Exact Dimensions:**
    *   **Rows:** 517 instances
    *   **Columns:** 13 features
    *   **File Size:** Approximately 25 KB (CSV)
*   **Target Variable & Nature of Task:**
    *   `area` — Continuous Burnt Area in hectares (0.00 to 1,090.84 ha)
*   **Class Distribution & Negative Control Balance:**
    *   Zero Burnt Area (`area == 0.00 ha`, Safe / Contained days): 247 rows (47.78%)
    *   Positive Burnt Area (`area > 0.00 ha`, Damaging Fire days): 270 rows (52.22%)
*   **Key Insight on Skewness:**
    *   The positive values of `area` are heavily right-skewed. The original researchers established that models must target `ln(area + 1)` rather than raw `area` to stabilize gradient descent and variance.
*   **Features:**
    *   `X`, `Y` (Park grid coordinates 1–9)
    *   `month`, `day` (Cyclical time features)
    *   `FFMC`, `DMC`, `DC`, `ISI` (FWI indices)
    *   `temp`, `RH`, `wind`, `rain` (Meteorological readings)

---

### Dataset 4: Global Wildfire Dataset (NASA FIRMS + Open-Meteo)
*   **Role in Project:** **Large-Scale Multi-Region Reference**
*   **Repository / Origin:** Kaggle (Vijayaragul VR)
*   **Exact Dimensions:**
    *   **Rows:** 118,858 instances
    *   **Columns:** 17 features (all numerical `float64`)
    *   **File Size:** 11.2 MB (CSV)
*   **Target Variable:**
    *   `occured` (Binary: 0 = No fire, 1 = Fire occurred)
    *   `frp` (Fire Radiative Power in Megawatts, Continuous regression)
*   **Class Distribution:**
    *   Contains approximately 35% active fire detections and 65% unburned background control samples.
*   **Features:** `lat`, `lon`, `temp_mean`, `humidity_min`, `wind_speed_max`, `pressure_mean`, `dewpoint_temp`, `fire_weather_index`.
---

## 3. Advanced Feature Engineering: Derived Meteorological Physics Features

To bridge raw meteorological inputs with empirical fire behavior physics, the ML modeling pipeline incorporates 4 domain-derived meteorological features. These engineered variables enable linear models (Ridge L2) to capture critical non-linear thermodynamic thresholds, while reducing tree depth and overfitting risks in Random Forest and XGBoost.

---

### Feature 1: Vapor Pressure Deficit (VPD)

#### Mathematical Formula (Magnus-Tetens Formulation)
Vapor Pressure Deficit represents the difference between the saturation vapor pressure and the actual vapor pressure of ambient air:

```
# Saturation vapor pressure es(T) in kilopascals (kPa)
es(T) = 0.61078 * exp((17.27 * temperature) / (temperature + 237.3))

# Actual vapor pressure ea in kilopascals (kPa)
ea = es(T) * (relative_humidity / 100.0)

# Vapor Pressure Deficit (VPD) in kilopascals (kPa)
VPD = es(T) - ea = es(T) * (1.0 - relative_humidity / 100.0)
```

Where:
*   `temperature` is in degrees Celsius (°C).
*   `relative_humidity` is in percentage (0% to 100%).
*   `VPD` is expressed in kilopascals (kPa).

#### Physical Rationale in Wildfire Science
Relative Humidity is a temperature-dependent relative fraction, not an absolute measure of drying potential. At 35°C and 40% RH, the atmospheric evaporative demand is dramatically harsher than at 15°C and 40% RH. 

VPD directly quantifies this drying suction force. When atmospheric VPD exceeds critical thresholds (typically > 1.5 to 2.0 kPa), the vapor pressure gradient between plant tissues and the ambient air causes rapid, uninhibited moisture extraction from living tree foliage and dead forest floor litter (1-hour and 10-hour fuels). This severe fuel desiccation drastically lowers the ignition energy required to spark a wildfire and enables rapid fire expansion. In wildfire literature, VPD is recognized as a superior standalone bioclimatic predictor compared to temperature or relative humidity in isolation.

---

### Feature 2: Heat-Aridity Index

#### Mathematical Formula
A composite ratio and interaction term capturing compound thermal and drought stress:

```
# Primary Ratio Formulation (with zero-division protection)
Heat_Aridity_Index = temperature / (relative_humidity + 1.0)

# Normalized Interaction Variant
Heat_Aridity_Product = temperature * (1.0 - relative_humidity / 100.0)
```

Where:
*   `temperature` is in degrees Celsius (°C).
*   `relative_humidity` is in percentage (0% to 100%).
*   The denominator constant `+ 1.0` prevents division-by-zero anomalies in hyper-arid microclimates where humidity drops near 0%.

#### Physical Rationale in Wildfire Science
Forest fire ignitions are driven primarily by compound extremes (simultaneous heatwaves and humidity depressions) rather than elevated temperature alone. A hot day with high humidity (e.g., 35°C and 80% RH) presents negligible fire risk because fuels remain damp. Conversely, when high temperatures coincide with collapsing relative humidity, fuel drying rates accelerate exponentially.

The Heat-Aridity Index constructs an explicit interaction boundary. It supplies Ridge (L2 regularized) models with a non-linear compounding signal, ensuring the linear model penalizes high-temperature, low-humidity combinations without needing high-dimensional polynomial expansion.

---

### Feature 3: Wind Spread Factor

#### Mathematical Formula
A coupled advection-aridity metric modeling kinetic flame propagation over dry fuels:

```
# Advective Spread Index
Wind_Spread_Factor = wind_speed * (1.0 - relative_humidity / 100.0)

# Kinetic Energy Variant (Dynamic Power)
Wind_Spread_Power = (wind_speed ** 2) * (1.0 - relative_humidity / 100.0)
```

Where:
*   `wind_speed` is in kilometers per hour (km/h).
*   `relative_humidity` is in percentage (0% to 100%).

#### Physical Rationale in Wildfire Science
Wind velocity is the dominant driver of fire Rate of Spread (ROS). Aerodynamically, wind tilts the convection column forward, pre-heating unburned fuels ahead of the flame front via radiant flux, while simultaneously providing fresh oxygen to the combustion zone and transporting burning embers to generate spot fires.

Crucially, high wind speed alone does not cause fire if the fuel bed is saturated (e.g. 40 km/h wind at 90% RH during rainfall produces zero fire propagation). The Wind Spread Factor physically couples mechanical wind propulsion with fuel aridity. Wind speed only scales fire risk when the dryness multiplier `(1.0 - relative_humidity / 100.0)` approaches 1.0, reflecting Rothermel's empirical fire propagation models.

---

### Feature 4: Rain Suppression

#### Mathematical Formula
An exponential decay dampening factor modeling the non-linear threshold extinguishing effect of precipitation:

```
# Immediate Precipitation Suppression
Rain_Suppression = exp(-0.5 * rain)

# Multi-Day Cumulative Moisture Retention
Rain_Suppression_Cumulative = exp(-0.3 * (rain + 0.5 * rain_14_day))
```

Where:
*   `rain` is 24-hour precipitation in millimeters (mm).
*   `rain_14_day` is 14-day cumulative rainfall in millimeters (mm).
*   When `rain = 0.0 mm`, `Rain_Suppression = exp(0) = 1.0` (zero dampening, baseline fire risk).
*   As rainfall increases (e.g. 2.0 mm, 5.0 mm, 15.0 mm), `Rain_Suppression` decays exponentially toward 0.0 (near-instantaneous quenching of fine fuels).

#### Physical Rationale in Wildfire Science
Precipitation exerts a sharp, non-linear threshold effect on fire activity. In forest ecology, light rain (1 to 3 mm) is sufficient to wet fine surface fuels (leaves, needles, cured grass) past their moisture of extinction (~20% to 30% fuel moisture content), temporarily halting surface fire spread. Higher precipitation amounts (e.g. 20 mm vs 50 mm) exhibit diminishing returns on immediate surface suppression because surface fuels are already saturated.

A simple linear representation in linear models falsely implies that moving from 50 mm to 60 mm reduces risk by the same increment as moving from 0 mm to 10 mm. The exponential decay formulation `exp(-k * rain)` accurately captures the physical reality of rapid surface saturation, providing a naturally bounded dampening multiplier between 0.0 and 1.0.

---

## 4. Indian Forest Reserve Testbed: Coordinates & Vulnerability Profiles

Rather than training on noisy, raw satellite feeds lacking negative control samples, our system uses the trained models to perform live inference against prominent Indian forest reserves.

The table below lists the 8 forest coordinates configured in `src/config/settings.py`:

| Reserve / National Park | State | Latitude (°N) | Longitude (°E) | Forest Type | Primary Fire Danger Season |
|---|---|---|---|---|---|
| **Bandipur National Park** | Karnataka | 11.6667 | 76.6333 | Dry Deciduous / Teak | February – May (Summer dry spells) |
| **Jim Corbett National Park**| Uttarakhand | 29.5300 | 78.7747 | Moist Deciduous / Sal | March – June (Pre-monsoon dry period) |
| **Simlipal National Park** | Odisha | 21.6833 | 86.3500 | Dense Sal / Moist Deciduous | February – April (Frequent surface leaf-litter fires)|
| **Kanha Tiger Reserve** | Madhya Pradesh| 22.3345 | 80.6115 | Sal and Bamboo Forests | March – May (Intense central heatwaves) |
| **Gir National Park** | Gujarat | 21.1243 | 70.8242 | Dry Deciduous Scrub & Teak | January – May (Arid Kathiawar climate) |
| **Wayanad Wildlife Sanctuary**| Kerala | 11.6854 | 76.3693 | Semi-Evergreen & Moist Deciduous | February – April (Western Ghats dry season) |
| **Kaziranga National Park** | Assam | 26.5775 | 93.1711 | Tropical Moist / Tall Grasslands| February – March (Controlled grassland burns) |
| **Ranthambore National Park**| Rajasthan | 26.0173 | 76.5026 | Tropical Dry Deciduous / Dhok | March – June (Severe arid heat) |

---

## 5. Senior Data Science Interview & Project Defense FAQ

### Q1: Why is having negative samples (normal days without fire) a non-negotiable project constraint?
**Answer:**
If a model is trained exclusively on active fire incidents, it experiences severe **survivorship / selection bias**. The training data contains zero examples of high temperatures or low humidities that did *not* result in a fire. As a result, the model cannot learn a true probabilistic decision boundary; it can only measure the conditional probability of weather given a fire, not the probability of a fire given weather. Negative samples (normal, fire-free days) provide the necessary counterfactual baseline for models to calculate true risk odds.

### Q2: Why compare Ridge Regression (L2) with Random Forest and XGBoost?
**Answer:**
1.  **L2 Regularization (Ridge):** Meteorological features exhibit heavy multicollinearity. For instance, temperature and relative humidity have a strong inverse correlation, while FWI indices are direct polynomial derivatives of weather features. Ordinary Least Squares (OLS) produces unstable coefficients with extreme variance under multicollinearity. Ridge penalizes the sum of squared coefficients (L2 penalty), shrinking redundant weights smoothly toward zero while maintaining a stable, interpretable linear baseline.
2.  **Random Forest:** An ensemble bagging technique that evaluates whether non-linear combinations and threshold cutoffs improve upon linear baselines without requiring feature scaling.
3.  **XGBoost:** A gradient boosting framework that captures high-order interactions and sharp threshold shifts (e.g. when RH drops below 25% while wind speed exceeds 20 km/h).

### Q3: Why does Ridge require feature scaling, while Random Forest and XGBoost do not?
**Answer:**
Ridge regression minimizes the sum of squared residuals plus the L2 penalty:
`Loss = MSE + alpha * sum(w_i^2)`.
Because the penalty treats all weight values symmetrically, a feature with large natural magnitude (e.g. Drought Code ranging from 1 to 800) will have tiny coefficient values and escape penalization, whereas a feature with small magnitude (e.g. Rain ranging from 0 to 15 mm) will be unfairly suppressed. Applying `StandardScaler()` (zero mean, unit variance) ensures every feature contributes equally to the regularization penalty. Tree-based algorithms (RF and XGBoost) only evaluate monotonic splits along single feature axes, making them completely invariant to feature scaling.

### Q4: How does our feature pipeline connect with live weather in India?
**Answer:**
The features in our primary engine (`MAX_TEMP`, `MIN_HUMIDITY`, `WIND_SPEED`, `PRECIPITATION`) were extracted from the Open-Meteo ERA5 archive. When a user selects an Indian reserve like Bandipur or Simlipal in our application, the backend queries Open-Meteo for that exact coordinate, extracts the same four meteorological parameters, runs them through the pre-fit scaler, and produces instantaneous ignition probability and severity scores.

### Q5: Why engineer derived meteorological features (VPD, Heat-Aridity, Wind Spread, Rain Suppression) when tree models like XGBoost can already learn interactions?
**Answer:**
While gradient boosted trees and random forests can partition feature space using axis-aligned orthogonal splits, they require significant tree depth and extensive sample sizes to approximate smooth, non-linear physical functions (such as the exponential Magnus-Tetens vapor curve or exponential precipitation quenching). Explicitly engineering these physics-based features:
1.  **Enables Linear / Ridge (L2) Models to Capture Critical Physics:** Linear models cannot inherently model ratios or products. Injecting VPD, Heat-Aridity, and Rain Suppression allows Ridge regression to benefit from non-linear thermodynamics while maintaining low variance and high interpretability.
2.  **Prevents Tree Model Overfitting:** Providing continuous physical curves directly constrains tree depth, preventing models from fitting noisy step-functions across regional datasets.
3.  **Aligns Model Reasoning with Fire Science:** Grounding features in empirical wildfire research (Rothermel spread models, Canadian FWI) ensures that feature importances and SHAP values correspond directly to real-world fire drivers.
