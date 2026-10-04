"""Data cleaning and preprocessing pipeline for Forest Fire Predictor.

Strictly follows immutability rules: reads from data/raw/ and writes to data/processed/.
"""

import sys
from pathlib import Path

# Add project root to sys.path to allow direct script execution
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd

from src.config.settings import PROCESSED_DATA_DIR, RAW_DATA_DIR


def clean_quebec_wildfire(
    raw_path: Path | None = None,
    output_path: Path | None = None,
) -> pd.DataFrame:
    """Clean the Quebec Wildfire Prediction dataset.

    Standardizes column names to lowercase, aligns meteorological variables,
    retains 14-day rolling drought indicators, and saves to data/processed/.
    """
    if raw_path is None:
        raw_path = RAW_DATA_DIR / "quebec_wildfire" / "quebec_wildfire_data.csv"
    if output_path is None:
        output_path = PROCESSED_DATA_DIR / "quebec_cleaned.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(raw_path)

    # Standardize column mappings
    rename_mapping = {
        "MAX_TEMP": "temperature",
        "MIN_HUMIDITY": "relative_humidity",
        "WIND_SPEED": "wind_speed",
        "PRECIPITATION": "rain",
        "FIRE_RISK": "fire_risk",
        "DAYS_SINCE_RAIN": "days_since_rain",
        "14_DAY_RAIN": "rain_14_day",
        "14_DAY_AVG_TEMP": "temp_14_day_avg",
        "DATE_DEBUT": "date",
        "LATITUDE": "latitude",
        "LONGITUDE": "longitude",
        "MONTH": "month",
    }
    df = df.rename(columns=rename_mapping)
    df.columns = [c.lower() for c in df.columns]

    # Verify no missing values
    assert df.isnull().sum().sum() == 0, "Quebec dataset contains unexpected nulls"

    # Save processed CSV
    df.to_csv(output_path, index=False)
    print(f"[OK] Quebec Wildfire cleaned: {df.shape} -> {output_path}")
    return df


def clean_algerian_forest_fires(
    raw_path: Path | None = None,
    output_path: Path | None = None,
) -> pd.DataFrame:
    """Clean the official Algerian Forest Fires dataset.

    Skips the top title banner, eliminates the mid-file subheader for
    Sidi-Bel Abbes, trims string whitespace, repairs corrupt tokens, casts
    features to float64, encodes Classes into binary fire_class, and standardizes columns.
    """
    if raw_path is None:
        raw_path = (
            RAW_DATA_DIR
            / "algerian_forest_fires"
            / "Algerian_forest_fires_dataset_UPDATE.csv"
        )
    if output_path is None:
        output_path = PROCESSED_DATA_DIR / "algerian_cleaned.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Step 1: Skip top banner (header=1)
    df = pd.read_csv(raw_path, header=1)

    # Step 2: Strip column names
    df.columns = df.columns.str.strip()

    # Step 3: Remove mid-file subheader row containing "Sidi-Bel Abbes Region Dataset"
    df = df[~df["day"].astype(str).str.contains("Sidi-Bel|day", na=False, case=False)]
    df = df.dropna(how="all").copy()

    # Step 4: Strip leading and trailing whitespace from string cells
    for col in df.columns:
        if df[col].dtype == object or "str" in str(df[col].dtype):
            df[col] = df[col].astype(str).str.strip()

    # Step 5: Address corrupt token in row index with '14.6 9'
    mask_corrupt = df["DC"] == "14.6 9"
    if mask_corrupt.any():
        df.loc[mask_corrupt, "DC"] = "14.69"
        df.loc[mask_corrupt, "FWI"] = "9.0"
        df.loc[mask_corrupt, "Classes"] = "fire"

    # Step 6: Convert all numerical columns to float64
    num_cols = [
        "Temperature",
        "RH",
        "Ws",
        "Rain",
        "FFMC",
        "DMC",
        "DC",
        "ISI",
        "BUI",
        "FWI",
    ]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")

    # Step 7: Encode Classes into binary fire_class: 1 for fire, 0 for not fire
    df["fire_class"] = df["Classes"].apply(
        lambda x: 1 if "not" not in str(x).lower() and "fire" in str(x).lower() else 0
    ).astype(int)

    # Step 8: Standardize column names
    rename_mapping = {
        "Temperature": "temperature",
        "RH": "relative_humidity",
        "Ws": "wind_speed",
        "Rain": "rain",
        "FFMC": "ffmc",
        "DMC": "dmc",
        "DC": "dc",
        "ISI": "isi",
        "BUI": "bui",
        "FWI": "fwi",
    }
    df = df.rename(columns=rename_mapping)

    final_cols = [
        "temperature",
        "relative_humidity",
        "wind_speed",
        "rain",
        "ffmc",
        "dmc",
        "dc",
        "isi",
        "bui",
        "fwi",
        "fire_class",
    ]
    df_clean = df[final_cols].copy().reset_index(drop=True)

    # Verify no missing values
    assert df_clean.isnull().sum().sum() == 0, "Algerian dataset contains nulls after cleaning"
    assert len(df_clean) == 244, f"Expected 244 rows, got {len(df_clean)}"

    df_clean.to_csv(output_path, index=False)
    print(f"[OK] Algerian Forest Fires cleaned: {df_clean.shape} -> {output_path}")
    return df_clean


def clean_montesinho_forest_fires(
    raw_path: Path | None = None,
    output_path: Path | None = None,
) -> pd.DataFrame:
    """Clean the Montesinho Forest Fires dataset.

    Standardizes meteorological column names to lowercase, computes the
    log-transformed target variable log_area = ln(area + 1), and saves to data/processed/.
    """
    if raw_path is None:
        raw_path = RAW_DATA_DIR / "montesinho_forest_fires" / "forestfires.csv"
    if output_path is None:
        output_path = PROCESSED_DATA_DIR / "montesinho_cleaned.csv"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(raw_path)

    rename_mapping = {
        "temp": "temperature",
        "RH": "relative_humidity",
        "wind": "wind_speed",
        "rain": "rain",
    }
    df = df.rename(columns=rename_mapping)
    df.columns = [c.lower() for c in df.columns]

    # Add log-transformed area for linear/L2 regularized modeling
    df["log_area"] = np.log1p(df["area"])

    # Verify no missing values
    assert df.isnull().sum().sum() == 0, "Montesinho dataset contains unexpected nulls"
    assert len(df) == 517, f"Expected 517 rows, got {len(df)}"

    df.to_csv(output_path, index=False)
    print(f"[OK] Montesinho Forest Fires cleaned: {df.shape} -> {output_path}")
    return df


def clean_all_datasets() -> dict[str, pd.DataFrame]:
    """Execute cleaning for all three raw datasets."""
    print("--- Starting Non-Destructive Cleaning Pipeline ---")
    quebec_df = clean_quebec_wildfire()
    algerian_df = clean_algerian_forest_fires()
    montesinho_df = clean_montesinho_forest_fires()
    print("--- Cleaning Complete for All Datasets ---")
    return {
        "quebec": quebec_df,
        "algerian": algerian_df,
        "montesinho": montesinho_df,
    }


if __name__ == "__main__":
    clean_all_datasets()
