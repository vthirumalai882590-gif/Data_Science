"""
FIREGUARD X - Preprocessing Tests
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from ml.preprocessing import clean_raw_dataset, FireDataPipeline, prepare_and_split_data
from ml.feature_engineering import compute_engineered_features

def test_feature_engineering_computation():
    sample_df = pd.DataFrame([{
        "Temperature": 35.0,
        "RH": 30.0,
        "Ws": 20.0,
        "Rain": 0.0,
        "FFMC": 90.0,
        "ISI": 10.0,
        "Region": 0
    }])
    featured = compute_engineered_features(sample_df)
    
    assert "temp_rh_ratio" in featured.columns
    assert "dryness_index" in featured.columns
    assert "wind_temp_interaction" in featured.columns
    assert "rain_deficit" in featured.columns
    assert featured["wind_temp_interaction"].iloc[0] == 700.0
    assert featured["dryness_index"].iloc[0] > 0

def test_pipeline_transform_consistency():
    split_res = prepare_and_split_data()
    pipeline = split_res["pipeline"]
    X_test = split_res["X_test"]
    
    scaled = pipeline.transform(X_test)
    assert scaled.shape[0] == len(X_test)
    assert scaled.shape[1] == len(pipeline.feature_names)
    assert not np.isnan(scaled).any()
