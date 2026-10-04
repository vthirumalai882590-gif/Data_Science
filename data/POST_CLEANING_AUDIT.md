# Post-Cleaning Data Audit Report

This report confirms the validation, structural schemas, statistical profiles, and data integrity of all processed datasets following the execution of the non-destructive cleaning pipeline.

**Execution Timestamp:** 2026-10-02 16:58 UTC
**Storage Isolation:** All cleaned artifacts are saved in `data/processed/`. The original source files in `data/raw/` remain untouched and immutable.

---

## 1. Processed Artifacts & File Inventory

| Dataset Identifier | Raw Source Path | Processed File Path | Clean Shape | File Size | Verified Null Count |
|---|---|---|---|---|---|
| **Quebec Wildfire** | `data/raw/quebec_wildfire/quebec_wildfire_data.csv` | `data/processed/quebec_cleaned.csv` | 9,171 rows × 12 cols | 954 KB | **0 (0.00%)** |
| **Algerian Forest Fires** | `data/raw/algerian_forest_fires/Algerian_forest_fires_dataset_UPDATE.csv` | `data/processed/algerian_cleaned.csv` | 244 rows × 11 cols | 12 KB | **0 (0.00%)** |
| **Montesinho Forest Fires**| `data/raw/montesinho_forest_fires/forestfires.csv` | `data/processed/montesinho_cleaned.csv` | 517 rows × 14 cols | 33 KB | **0 (0.00%)** |

---

## 2. Dataset 1: Quebec Wildfire Prediction (`quebec_cleaned.csv`)

### Schema & Data Types
*   **Target Column:** `fire_risk` (`int64`, binary: 1 = Wildfire Ignition, 0 = Safe / Normal Day)
*   **Features:**

| Column Name | Data Type | Non-Null Count | Domain / Description |
|---|---|---|---|
| `date` | `object` (string) | 9,171 | Observation date (YYYY-MM-DD) |
| `latitude` | `float64` | 9,171 | Latitude coordinate (45.02 to 58.74) |
| `longitude` | `float64` | 9,171 | Longitude coordinate (-79.50 to -57.25) |
| `month` | `float64` | 9,171 | Month of fire season (5.0 to 9.0) |
| `temperature` | `float64` | 9,171 | Daily maximum temperature in °C |
| `relative_humidity` | `float64` | 9,171 | Daily minimum relative humidity in % |
| `wind_speed` | `float64` | 9,171 | Daily maximum wind speed in km/h |
| `rain` | `float64` | 9,171 | Total daily rainfall in mm |
| `rain_14_day` | `float64` | 9,171 | 14-day cumulative rainfall in mm |
| `temp_14_day_avg` | `float64` | 9,171 | 14-day rolling average maximum temperature in °C |
| `days_since_rain` | `float64` | 9,171 | Consecutive dry days (0.0 to 14.0) |
| `fire_risk` | `int64` | 9,171 | Target indicator (1 = Fire, 0 = Safe) |

### Summary Statistics (`df.describe().T`)
| Feature | Count | Mean | Std | Min | 25% | 50% (Median) | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| `latitude` | 9171.0 | 50.0503 | 3.6877 | 45.0154 | 46.8823 | 49.1270 | 52.6178 | 58.7447 |
| `longitude` | 9171.0 | -70.7343 | 5.7577 | -79.5020 | -75.1776 | -72.0358 | -66.8305 | -57.2500 |
| `month` | 9171.0 | 6.6282 | 1.3332 | 5.0000 | 5.0000 | 6.0000 | 8.0000 | 9.0000 |
| `temperature` | 9171.0 | 18.9936 | 7.6293 | -9.5000 | 14.0000 | 20.1000 | 24.8000 | 34.6000 |
| `relative_humidity` | 9171.0 | 50.5810 | 18.3842 | 14.0000 | 36.0000 | 48.0000 | 64.0000 | 98.0000 |
| `wind_speed` | 9171.0 | 20.0761 | 8.5535 | 4.4000 | 14.1000 | 17.9000 | 23.7000 | 90.9000 |
| `rain` | 9171.0 | 2.7175 | 5.8423 | 0.0000 | 0.0000 | 0.3000 | 2.8000 | 77.6000 |
| `rain_14_day` | 9171.0 | 39.3004 | 24.3593 | 0.1000 | 21.9000 | 35.0000 | 51.9000 | 262.9000 |
| `temp_14_day_avg` | 9171.0 | 16.6558 | 6.3627 | -6.6286 | 12.6357 | 17.7214 | 21.5286 | 31.3929 |
| `days_since_rain` | 9171.0 | 3.4931 | 2.7823 | 1.0000 | 1.0000 | 3.0000 | 5.0000 | 14.0000 |
| `fire_risk` | 9171.0 | 0.5035 | 0.5000 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |

### Target Distribution
*   `fire_risk = 1`: 4,618 records (50.35%)
*   `fire_risk = 0`: 4,553 records (49.65%)
*   **Status:** Confirmed balanced representation for classification models.

---

## 3. Dataset 2: Algerian Forest Fires (`algerian_cleaned.csv`)

### Schema & Data Types
*   **Target Column:** `fire_class` (`int64`, binary: 1 = Fire, 0 = Not Fire)
*   **Continuous Severity Target:** `fwi` (`float64`, continuous index for Ridge regression)

| Column Name | Data Type | Non-Null Count | Domain / Description |
|---|---|---|---|
| `temperature` | `float64` | 244 | Daily maximum temperature in °C |
| `relative_humidity` | `float64` | 244 | Relative humidity in % |
| `wind_speed` | `float64` | 244 | Wind speed in km/h |
| `rain` | `float64` | 244 | Outside rain in mm/m² |
| `ffmc` | `float64` | 244 | Fine Fuel Moisture Code |
| `dmc` | `float64` | 244 | Duff Moisture Code |
| `dc` | `float64` | 244 | Drought Code |
| `isi` | `float64` | 244 | Initial Spread Index |
| `bui` | `float64` | 244 | Buildup Index |
| `fwi` | `float64` | 244 | Fire Weather Index score |
| `fire_class` | `int64` | 244 | Binary classification target (1 = Fire, 0 = Not Fire) |

### Summary Statistics (`df.describe().T`)
| Feature | Count | Mean | Std | Min | 25% | 50% (Median) | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| `temperature` | 244.0 | 32.1721 | 3.6338 | 22.0000 | 30.0000 | 32.0000 | 35.0000 | 42.0000 |
| `relative_humidity` | 244.0 | 61.9385 | 14.8842 | 21.0000 | 52.0000 | 63.0000 | 73.2500 | 90.0000 |
| `wind_speed` | 244.0 | 15.5041 | 2.8102 | 6.0000 | 14.0000 | 15.0000 | 17.0000 | 29.0000 |
| `rain` | 244.0 | 0.7607 | 1.9994 | 0.0000 | 0.0000 | 0.0000 | 0.5000 | 16.8000 |
| `ffmc` | 244.0 | 77.8877 | 14.3376 | 28.6000 | 72.0750 | 83.5000 | 88.3000 | 96.0000 |
| `dmc` | 244.0 | 14.6734 | 12.3680 | 0.7000 | 5.8000 | 11.3000 | 20.7500 | 65.9000 |
| `dc` | 244.0 | 49.2885 | 47.6194 | 6.9000 | 13.2750 | 33.1000 | 68.1500 | 220.4000 |
| `isi` | 244.0 | 4.7742 | 4.1753 | 0.0000 | 1.4000 | 3.5000 | 7.3000 | 19.0000 |
| `bui` | 244.0 | 16.6648 | 14.2048 | 1.1000 | 6.0000 | 12.2500 | 22.5250 | 68.0000 |
| `fwi` | 244.0 | 7.0434 | 7.4263 | 0.0000 | 0.7000 | 4.4500 | 11.3750 | 31.1000 |
| `fire_class` | 244.0 | 0.5656 | 0.4967 | 0.0000 | 0.0000 | 1.0000 | 1.0000 | 1.0000 |

### Target Distribution
*   `fire_class = 1` (Fire): 138 records (56.56%)
*   `fire_class = 0` (Not Fire): 106 records (43.44%)
*   **Status:** Preserved regional balance across Bejaia (122 records) and Sidi-Bel Abbes (122 records).

---

## 4. Dataset 3: Montesinho Natural Park (`montesinho_cleaned.csv`)

### Schema & Data Types
*   **Target Columns:** 
    *   `area`: Raw continuous burned area in hectares (0.0 to 1090.84 ha)
    *   `log_area`: Natural log-transformed burned area: `log_area = ln(area + 1)`

| Column Name | Data Type | Non-Null Count | Domain / Description |
|---|---|---|---|
| `x` | `int64` | 517 | Spatial coordinate X (1 to 9) |
| `y` | `int64` | 517 | Spatial coordinate Y (2 to 9) |
| `month` | `object` | 517 | Month string ('jan' to 'dec') |
| `day` | `object` | 517 | Day of week ('mon' to 'sun') |
| `ffmc` | `float64` | 517 | Fine Fuel Moisture Code (18.7 to 96.2) |
| `dmc` | `float64` | 517 | Duff Moisture Code (1.1 to 291.3) |
| `dc` | `float64` | 517 | Drought Code (7.9 to 860.6) |
| `isi` | `float64` | 517 | Initial Spread Index (0.0 to 56.1) |
| `temperature` | `float64` | 517 | Temperature in °C (2.2 to 33.3) |
| `relative_humidity` | `int64` | 517 | Relative humidity in % (15 to 100) |
| `wind_speed` | `float64` | 517 | Wind speed in km/h (0.4 to 9.4) |
| `rain` | `float64` | 517 | Rain in mm/m² (0.0 to 6.4) |
| `area` | `float64` | 517 | Raw burned area in hectares |
| `log_area` | `float64` | 517 | Log-transformed target: ln(area + 1) |

### Summary Statistics (`df.describe().T`)
| Feature | Count | Mean | Std | Min | 25% | 50% (Median) | 75% | Max |
|---|---|---|---|---|---|---|---|---|
| `x` | 517.0 | 4.6692 | 2.3138 | 1.0000 | 3.0000 | 4.0000 | 7.0000 | 9.0000 |
| `y` | 517.0 | 4.2998 | 1.2299 | 2.0000 | 4.0000 | 4.0000 | 5.0000 | 9.0000 |
| `ffmc` | 517.0 | 90.6447 | 5.5201 | 18.7000 | 90.2000 | 91.6000 | 92.9000 | 96.2000 |
| `dmc` | 517.0 | 110.8723 | 64.0465 | 1.1000 | 68.6000 | 108.3000 | 142.4000 | 291.3000 |
| `dc` | 517.0 | 547.9400 | 248.0662 | 7.9000 | 437.7000 | 664.2000 | 713.9000 | 860.6000 |
| `isi` | 517.0 | 9.0217 | 4.5595 | 0.0000 | 6.5000 | 8.4000 | 10.8000 | 56.1000 |
| `temperature` | 517.0 | 18.8892 | 5.8066 | 2.2000 | 15.5000 | 19.3000 | 22.8000 | 33.3000 |
| `relative_humidity` | 517.0 | 44.2882 | 16.3175 | 15.0000 | 33.0000 | 42.0000 | 53.0000 | 100.0000 |
| `wind_speed` | 517.0 | 4.0176 | 1.7917 | 0.4000 | 2.7000 | 4.0000 | 4.9000 | 9.4000 |
| `rain` | 517.0 | 0.0217 | 0.2960 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 6.4000 |
| `area` | 517.0 | 12.8473 | 63.6558 | 0.0000 | 0.0000 | 0.5200 | 6.5700 | 1090.8400 |
| `log_area` | 517.0 | 1.1110 | 1.3984 | 0.0000 | 0.0000 | 0.4187 | 2.0242 | 6.9956 |

### Target Distribution
*   `area == 0.00 ha` (`log_area == 0.0`): 247 records (47.78%)
*   `area > 0.00 ha` (`log_area > 0.0`): 270 records (52.22%)
*   **Skewness Improvement:** Raw `area` skewness of 12.85 reduced to 0.94 in `log_area`, making it suitable for Ridge regression and gradient-based models.

---

## 5. Before vs. After Transformation Summary

| Issue / Attribute | Raw State | Processed State | Resolution Strategy |
|---|---|---|---|
| **Algerian Top Title Banner** | Line 0 text `'Bejaia Region Dataset '` forced single-column reading | Removed | Skipped top banner via `header=1` parameter in loader |
| **Algerian Mid-File Subheader** | Rows 122 & 123 contained section text and repeated column headers | Removed | Filtered out rows where `day` contained text tokens (`'Sidi-Bel'`, `'day'`) |
| **Algerian Corrupt Token Row 167** | `DC = '14.6 9'`, `FWI = 'fire   '`, `Classes = NaN` | `dc = 14.69`, `fwi = 9.0`, `fire_class = 1` | Repaired misaligned data values, preventing loss of statistical record |
| **Algerian Column Whitespace** | Columns had leading/trailing spaces (`' RH'`, `' Ws'`, `'Classes  '`) | Clean snake_case: `temperature`, `relative_humidity`, `fire_class` | Trimmed all whitespace and standardized names |
| **Algerian Data Types** | All columns detected as `object` (string) | Numeric features converted to `float64`, target to `int64` | Systematic type coercion and schema enforcement |
| **Quebec Column Names** | Uppercase headers (`MAX_TEMP`, `MIN_HUMIDITY`, `FIRE_RISK`) | Standardized lowercase: `temperature`, `relative_humidity`, `fire_risk` | Renamed to uniform project convention |
| **Quebec Rolling Memory** | Present as `14_DAY_RAIN`, `DAYS_SINCE_RAIN` | Standardized: `rain_14_day`, `days_since_rain` | Formatted to clean snake_case while preserving memory signals |
| **Montesinho Column Names** | Abbreviated headers: `temp`, `RH`, `wind` | Aligned: `temperature`, `relative_humidity`, `wind_speed` | Standardized to match Quebec and Algerian naming |
| **Montesinho Target Skewness** | Skewness of 12.85 on raw `area` in hectares | Skewness reduced to 0.94 via `log_area = ln(area + 1)` | Logarithmic transformation to support Ridge L2 regularized regression |
| **Missing Values Across Datasets**| Present in raw Algerian subheaders | **Zero missing values** across all three datasets | Full non-null integrity verified |
