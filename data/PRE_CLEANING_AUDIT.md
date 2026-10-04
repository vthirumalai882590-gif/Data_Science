# Pre-Cleaning Data Audit Report

This report documents the structural, statistical, and hygiene characteristics of all raw datasets prior to any preprocessing. 

**Inspection Timestamp:** 2026-10-02 16:55 UTC
**Integrity Rule:** All raw source files inside `data/raw/` remain strictly immutable and read-only.

---

## 1. Dataset 1: Quebec Wildfire Prediction Dataset

### Location & Dimensions
*   **File Path:** `data/raw/quebec_wildfire/quebec_wildfire_data.csv`
*   **File Size:** Approximately 963 KB
*   **Raw Shape:** 9,171 rows × 12 columns

### Column Names & Detected Data Types
| Column Name | Detected Data Type | Null Count | Null % | Physical Domain Range |
|---|---|---|---|---|
| `DATE_DEBUT` | `object` (string) | 0 | 0.00% | 2018-05-01 to 2024-09-30 |
| `LATITUDE` | `float64` | 0 | 0.00% | 45.02 to 57.98 (Decimal degrees) |
| `LONGITUDE` | `float64` | 0 | 0.00% | -79.88 to -57.13 (Decimal degrees) |
| `MONTH` | `float64` | 0 | 0.00% | 5.0 to 9.0 (May to Sept) |
| `FIRE_RISK` | `int64` | 0 | 0.00% | Binary {0, 1} |
| `MAX_TEMP` | `float64` | 0 | 0.00% | -3.80°C to 38.60°C |
| `PRECIPITATION` | `float64` | 0 | 0.00% | 0.00 mm to 96.40 mm |
| `WIND_SPEED` | `float64` | 0 | 0.00% | 2.50 km/h to 55.40 km/h |
| `MIN_HUMIDITY` | `float64` | 0 | 0.00% | 11.00% to 100.00% |
| `14_DAY_RAIN` | `float64` | 0 | 0.00% | 0.00 mm to 248.80 mm |
| `14_DAY_AVG_TEMP` | `float64` | 0 | 0.00% | 1.85°C to 32.70°C |
| `DAYS_SINCE_RAIN` | `float64` | 0 | 0.00% | 0.00 to 14.00 days |

### Target Distribution
*   **Target Column:** `FIRE_RISK`
*   `FIRE_RISK = 1` (Active Wildfire Ignition): 4,618 records (50.35%)
*   `FIRE_RISK = 0` (Safe Control / Normal Day): 4,553 records (49.65%)
*   **Assessment:** Balanced 1:1 distribution. Zero survivorship/selection bias.

### Specific Anomalies & Hygiene Observations
1.  **Uppercase Column Headers:** Feature names use uppercase syntax (e.g., `MAX_TEMP`, `MIN_HUMIDITY`) which must be standardized to lowercase snake_case for project-wide consistency.
2.  **Date Column Representation:** `DATE_DEBUT` is parsed as a raw string object.
3.  **Missing Values:** Completely clean; zero null entries across all 9,171 records.

---

## 2. Dataset 2: Algerian Forest Fires Dataset (Official UCI Version)

### Location & Dimensions
*   **File Path:** `data/raw/algerian_forest_fires/Algerian_forest_fires_dataset_UPDATE.csv`
*   **File Size:** Approximately 14.8 KB
*   **Raw Default Shape:** 247 rows × 1 column (if loaded with default `header=0`, line 0 is treated as a single title column).
*   **Parsed Shape (`header=1`):** 246 rows × 14 columns

### Column Names & Detected Data Types (with `header=1`)
| Raw Column Name (Exact String) | Detected Data Type | Null Count | Null % | Notes on Detected Values |
|---|---|---|---|---|
| `'day'` | `object` (string) | 0 | 0.00% | Contains day strings, plus subheader `'day'` and banner text |
| `'month'` | `object` (string) | 1 | 0.41% | Contains month strings, plus subheader `'month'` |
| `'year'` | `object` (string) | 1 | 0.41% | Contains `'2012'`, plus subheader `'year'` |
| `'Temperature'` | `object` (string) | 1 | 0.41% | Temperatures parsed as strings due to header rows |
| `' RH'` | `object` (string) | 1 | 0.41% | Leading whitespace in column name |
| `' Ws'` | `object` (string) | 1 | 0.41% | Leading whitespace in column name |
| `'Rain '` | `object` (string) | 1 | 0.41% | Trailing whitespace in column name |
| `'FFMC'` | `object` (string) | 1 | 0.41% | Numeric values stored as strings |
| `'DMC'` | `object` (string) | 1 | 0.41% | Numeric values stored as strings |
| `'DC'` | `object` (string) | 1 | 0.41% | Corrupt space-delimited string `'14.6 9'` at row index 167 |
| `'ISI'` | `object` (string) | 1 | 0.41% | Numeric values stored as strings |
| `'BUI'` | `object` (string) | 1 | 0.41% | Numeric values stored as strings |
| `'FWI'` | `object` (string) | 1 | 0.41% | Contains shifted class token `'fire   '` at row index 167 |
| `'Classes  '` | `object` (string) | 2 | 0.81% | Trailing whitespace; multiple string variants (`'fire   '`, `'not fire'`) |

### Target Distribution (Raw Strings in `'Classes  '`)
*   `'fire   '`: 131
*   `'not fire   '`: 101
*   `'fire'`: 4
*   `'fire '`: 2
*   `'not fire'`: 2
*   `'not fire '`: 2
*   `'not fire     '`: 1
*   `'not fire    '`: 1
*   `'Classes  '` (Subheader artifact): 1
*   `NaN` (Row 122 banner row & Row 167 corrupted row): 2

### Specific Anomalies & Hygiene Observations
1.  **Top Title Banner (Row 0):** Line 0 contains the text `'Bejaia Region Dataset '`, forcing `header=1` on load.
2.  **Mid-File Subheader (Rows 122 and 123):**
    *   Row 122: `'Sidi-Bel Abbes Region Dataset'`, followed by 13 empty/NaN columns.
    *   Row 123: Duplicated column header `'day', 'month', 'year', 'Temperature', ...`.
3.  **Pervasive Whitespace Padding:** Column names contain whitespace (`' RH'`, `' Ws'`, `'Rain '`, `'Classes  '`), and cell strings have up to 5 trailing spaces.
4.  **Corrupt Data Row 167 (Date: 14/07/2012 in Sidi-Bel Abbes):**
    *   Original entry: `DC = '14.6 9'`, `ISI = '12.5'`, `BUI = '10.4'`, `FWI = 'fire   '`, `Classes = NaN`.
    *   A missing comma caused the class token `'fire'` to shift into the `FWI` column and concatenated `'14.6'` with `'9'`.
5.  **Data Type Pollution:** Because of subheaders and row 167, all 14 columns default to Python `object` (strings).

---

## 3. Dataset 3: Montesinho Natural Park Forest Fires Dataset (Portugal)

### Location & Dimensions
*   **File Path:** `data/raw/montesinho_forest_fires/forestfires.csv`
*   **File Size:** Approximately 25.5 KB
*   **Raw Shape:** 517 rows × 13 columns

### Column Names & Detected Data Types
| Column Name | Detected Data Type | Null Count | Null % | Physical Domain Range |
|---|---|---|---|---|
| `X` | `int64` | 0 | 0.00% | 1 to 9 (Park spatial grid coordinate) |
| `Y` | `int64` | 0 | 0.00% | 2 to 9 (Park spatial grid coordinate) |
| `month` | `object` (string) | 0 | 0.00% | `'jan'` through `'dec'` |
| `day` | `object` (string) | 0 | 0.00% | `'mon'` through `'sun'` |
| `FFMC` | `float64` | 0 | 0.00% | 18.70 to 96.20 |
| `DMC` | `float64` | 0 | 0.00% | 1.10 to 291.30 |
| `DC` | `float64` | 0 | 0.00% | 7.90 to 860.60 |
| `ISI` | `float64` | 0 | 0.00% | 0.00 to 56.10 |
| `temp` | `float64` | 0 | 0.00% | 2.20°C to 33.30°C |
| `RH` | `int64` | 0 | 0.00% | 15% to 100% |
| `wind` | `float64` | 0 | 0.00% | 0.40 km/h to 9.40 km/h |
| `rain` | `float64` | 0 | 0.00% | 0.00 mm to 6.40 mm |
| `area` | `float64` | 0 | 0.00% | 0.00 ha to 1,090.84 ha (Burned area) |

### Target Distribution
*   **Target Column:** `area` (Burned area in hectares)
*   `area == 0.00 ha` (Unburned / Contained Days): 247 records (47.78%)
*   `area > 0.00 ha` (Damaging Wildfire Days): 270 records (52.22%)
*   **Skewness Metric:** Raw `area` skewness is 12.85 (extreme right skew). 

### Specific Anomalies & Hygiene Observations
1.  **Severe Positive Skew:** Over 47% of records have `area = 0`, while non-zero values extend up to 1,090 ha. Linear models (Ridge) will struggle with raw `area`. Transformation to `log_area = ln(area + 1)` is required.
2.  **Short Column Naming:** `temp` and `RH` should be aligned with project standards (`temperature`, `relative_humidity`).
3.  **Missing Values:** Completely clean; 0 missing values.

---

## 4. Pre-Cleaning Summary Matrix

| Metric / Attribute | Quebec Wildfire | Algerian Forest Fires | Montesinho Forest Fires |
|---|---|---|---|
| **Raw File Path** | `data/raw/quebec_wildfire/quebec_wildfire_data.csv` | `data/raw/algerian_forest_fires/Algerian_forest_fires_dataset_UPDATE.csv` | `data/raw/montesinho_forest_fires/forestfires.csv` |
| **Raw Dimensions** | 9,171 rows × 12 cols | 246 rows × 14 cols (with `header=1`) | 517 rows × 13 cols |
| **Missing Values** | 0 nulls (0.0%) | 2 rows with nulls (subheaders) + row 167 | 0 nulls (0.0%) |
| **Primary Anomaly** | Uppercase headers | Mid-file subheaders, whitespace, corrupt row 167 | Extreme target skewness |
| **Target Variable** | `FIRE_RISK` | `'Classes  '` | `area` |
| **Target Nature** | Binary Classification (0/1) | Binary Classification (Text) | Continuous Regression (ha) |
| **Negative / Control Balance** | 4,553 safe days (49.65%) | ~106 not fire days (~43.44%) | 247 zero-burn days (47.78%) |
| **Cleaning Priority** | Column standardization | Structural & Type Sanitation | Feature Renaming & Log Target Transform |
