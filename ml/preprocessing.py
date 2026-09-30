"""
FIREGUARD X - Data Preprocessing Pipeline
Handles data cleaning, missing value imputation, type casting, target encoding,
outlier validation, and train-test partitioning.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from ml.config import (
    RAW_DATA_PATH,
    INTERIM_DATA_PATH,
    PROCESSED_DATA_PATH,
    PREPROCESSOR_PATH,
    FEATURE_NAMES_PATH,
    RANDOM_STATE,
    TEST_SIZE,
)
from ml.feature_engineering import compute_engineered_features

CORE_NUMERICAL_COLS = [
    "Temperature", "RH", "Ws", "Rain", 
    "FFMC", "DMC", "DC", "ISI", "BUI", "FWI"
]

ENGINEERED_COLS = [
    "temp_rh_ratio", "dryness_index", 
    "wind_temp_interaction", "rain_deficit", "ffmc_isi_ratio"
]

ALL_FEATURE_COLS = CORE_NUMERICAL_COLS + ["Region"] + ENGINEERED_COLS

def clean_raw_dataset(input_path: str = RAW_DATA_PATH) -> pd.DataFrame:
    """
    Cleans raw forest fire observations:
    - Strips column name whitespace
    - Casts numeric attributes to proper float/int representations
    - Encodes target 'Classes' ('fire' -> 1, 'not fire' -> 0)
    - Validates missing values and imputes with feature medians if present.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Raw dataset not found at {input_path}")
    
    df = pd.read_csv(input_path)
    df.columns = [col.strip() for col in df.columns]

    # Convert core columns to numeric
    for col in CORE_NUMERICAL_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    if "Region" in df.columns:
        df["Region"] = pd.to_numeric(df["Region"], errors="coerce").fillna(0).astype(int)
    else:
        df["Region"] = 0

    # Impute missing values with median if any exist
    for col in CORE_NUMERICAL_COLS:
        if df[col].isnull().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)

    # Encode target Classes
    if "Classes" in df.columns:
        df["Classes"] = df["Classes"].astype(str).str.strip().str.lower()
        # Fire = 1, Not Fire = 0
        df["target"] = df["Classes"].apply(lambda val: 1 if "not" not in val and "fire" in val else 0)
    elif "target" not in df.columns:
        # Fallback target derivation if burned area or FWI exists
        if "FWI" in df.columns:
            df["target"] = (df["FWI"] > 1.0).astype(int)
        else:
            raise ValueError("No recognizable target column ('Classes' or 'target') in dataset.")

    os.makedirs(os.path.dirname(INTERIM_DATA_PATH), exist_ok=True)
    df.to_csv(INTERIM_DATA_PATH, index=False)
    return df

class FireDataPipeline:
    """
    Stateful preprocessing and scaling pipeline that persists feature configurations
    and ensures zero data leakage during evaluation and live prediction.
    """
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = ALL_FEATURE_COLS
        self.core_features = CORE_NUMERICAL_COLS
        self.fitted = False
        self.medians = {}
        self.means = {}
        self.stds = {}

    def fit(self, X: pd.DataFrame):
        X_eng = compute_engineered_features(X)
        X_subset = X_eng[self.feature_names]
        self.scaler.fit(X_subset)
        
        # Store population statistics for data quality & anomaly detection
        for col in self.feature_names:
            self.medians[col] = float(X_subset[col].median())
            self.means[col] = float(X_subset[col].mean())
            self.stds[col] = float(X_subset[col].std() if X_subset[col].std() > 0 else 1.0)
            
        self.fitted = True
        return self

    def transform(self, X: pd.DataFrame) -> np.ndarray:
        if not self.fitted:
            raise RuntimeError("Pipeline must be fitted before transforming data.")
        X_eng = compute_engineered_features(X)
        for col in self.feature_names:
            if col not in X_eng.columns:
                X_eng[col] = self.medians.get(col, 0.0)
        X_subset = X_eng[self.feature_names]
        return self.scaler.transform(X_subset)

    def fit_transform(self, X: pd.DataFrame) -> np.ndarray:
        return self.fit(X).transform(X)

def prepare_and_split_data():
    """
    Cleans dataset, engineers features, performs stratified train-test split,
    fits preprocessing pipeline, and saves artifacts.
    """
    df = clean_raw_dataset()
    df_featured = compute_engineered_features(df)
    
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df_featured.to_csv(PROCESSED_DATA_PATH, index=False)

    X = df_featured[ALL_FEATURE_COLS]
    y = df_featured["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=TEST_SIZE, 
        stratify=y, 
        random_state=RANDOM_STATE
    )

    pipeline = FireDataPipeline()
    X_train_scaled = pipeline.fit_transform(X_train)
    X_test_scaled = pipeline.transform(X_test)

    os.makedirs(os.path.dirname(PREPROCESSOR_PATH), exist_ok=True)
    joblib.dump(pipeline, PREPROCESSOR_PATH)
    
    import json
    with open(FEATURE_NAMES_PATH, "w") as f:
        json.dump(ALL_FEATURE_COLS, f, indent=2)

    return {
        "X_train": X_train,
        "X_test": X_test,
        "X_train_scaled": X_train_scaled,
        "X_test_scaled": X_test_scaled,
        "y_train": y_train,
        "y_test": y_test,
        "pipeline": pipeline,
        "raw_df": df
    }

if __name__ == "__main__":
    res = prepare_and_split_data()
    print(f"[FIREGUARD X] Preprocessing complete.")
    print(f"X_train shape: {res['X_train'].shape}, X_test shape: {res['X_test'].shape}")
    print(f"Class distribution - Train: {np.bincount(res['y_train'])}, Test: {np.bincount(res['y_test'])}")
