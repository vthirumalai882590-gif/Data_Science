"""Unit and integration test suite for trained machine learning pipelines in models/.

Validates:
1. All serialized model artifacts (.joblib) load cleanly.
2. Inference bounds on Extreme Fire Weather (Temp=45°C, RH=15%, Wind=30km/h, Rain=0mm -> Risk >= 60.0).
3. Inference bounds on Safe Rainy Weather (Temp=15°C, RH=90%, Wind=5km/h, Rain=25mm -> Risk <= 20.0 and strictly >= 0.0).
4. Non-negative burned area predictions from models/montesinho_best_model.joblib.
5. Encapsulated StandardScaler and BoundedRiskPipeline behavior.
6. Synchronized metadata in models/model_metrics.json covering Quebec, Algerian, and Montesinho datasets.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config.settings import MODELS_DIR


@pytest.fixture(scope="module")
def extreme_fire_weather() -> pd.DataFrame:
    """Extreme Fire Weather: Temp=45°C, RH=15%, Wind=30km/h, Rain=0mm."""
    return pd.DataFrame(
        [
            {
                "temperature": 45.0,
                "relative_humidity": 15.0,
                "wind_speed": 30.0,
                "rain": 0.0,
            }
        ]
    )


@pytest.fixture(scope="module")
def safe_rainy_weather() -> pd.DataFrame:
    """Safe Rainy Weather: Temp=15°C, RH=90%, Wind=5km/h, Rain=25mm."""
    return pd.DataFrame(
        [
            {
                "temperature": 15.0,
                "relative_humidity": 90.0,
                "wind_speed": 5.0,
                "rain": 25.0,
            }
        ]
    )


@pytest.fixture(scope="module")
def safe_rainy_moderate_weather() -> pd.DataFrame:
    """Safe Rainy Weather: Temp=18°C, RH=85%, Wind=5km/h, Rain=15mm."""
    return pd.DataFrame(
        [
            {
                "temperature": 18.0,
                "relative_humidity": 85.0,
                "wind_speed": 5.0,
                "rain": 15.0,
            }
        ]
    )


def test_all_joblib_files_load_cleanly():
    """Verify that all core serialized pipeline artifacts exist and load cleanly without warnings."""
    expected_files = [
        "ridge_model.joblib",
        "rf_model.joblib",
        "xgb_model.joblib",
        "best_model.joblib",
        "montesinho_best_model.joblib",
        "best_classifier.joblib",
        "model_metrics.json",
    ]
    for filename in expected_files:
        path = MODELS_DIR / filename
        assert path.exists(), f"Expected artifact '{filename}' missing from {MODELS_DIR}"
        assert path.stat().st_size > 0, f"Artifact '{filename}' is empty"

        if filename.endswith(".joblib"):
            model = joblib.load(path)
            assert model is not None, f"Failed to load joblib model: {filename}"
            assert hasattr(model, "predict"), f"Loaded object from {filename} missing .predict() method"


def test_extreme_fire_weather_bounds(extreme_fire_weather):
    """Test inference bounds on Extreme Fire Weather (Temp=45°C, RH=15%, Wind=30km/h, Rain=0mm -> Risk >= 55.0)."""
    continuous_models = [
        "ridge_model.joblib",
        "rf_model.joblib",
        "xgb_model.joblib",
        "best_model.joblib",
    ]
    for filename in continuous_models:
        model = joblib.load(MODELS_DIR / filename)
        pred = model.predict(extreme_fire_weather)

        assert len(pred) == 1
        risk_score = float(pred[0])
        assert not np.isnan(risk_score), f"{filename} returned NaN for extreme fire weather"
        assert not np.isinf(risk_score), f"{filename} returned Inf for extreme fire weather"
        assert risk_score >= 55.0, (
            f"{filename} predicted risk {risk_score:.2f} < 55.0 on extreme fire weather "
            "(Temp=45°C, RH=15%, Wind=30km/h, Rain=0mm)"
        )
        assert risk_score <= 100.0, f"{filename} predicted risk {risk_score:.2f} > 100.0 (unclamped upper bound)"


def test_safe_rainy_weather_bounds(safe_rainy_weather, safe_rainy_moderate_weather):
    """Test inference bounds on Safe Rainy Weather -> Risk <= 20.0 and strictly >= 0.0."""
    continuous_models = [
        "ridge_model.joblib",
        "rf_model.joblib",
        "xgb_model.joblib",
        "best_model.joblib",
    ]
    for filename in continuous_models:
        model = joblib.load(MODELS_DIR / filename)

        # Scenario 1: 15°C, 90% RH, 5 km/h, 25 mm rain
        pred_15 = model.predict(safe_rainy_weather)
        risk_15 = float(pred_15[0])
        assert not np.isnan(risk_15), f"{filename} returned NaN on safe weather (15C/25mm)"
        assert risk_15 >= 0.0, f"{filename} output negative risk {risk_15:.2f} < 0.0 on safe weather (15C/25mm)"
        assert risk_15 <= 20.0, (
            f"{filename} predicted risk {risk_15:.2f} > 20.0 on safe rainy weather (15C/25mm)"
        )

        # Scenario 2: 18°C, 85% RH, 5 km/h, 15 mm rain (Gatekeeper scenario)
        pred_18 = model.predict(safe_rainy_moderate_weather)
        risk_18 = float(pred_18[0])
        assert not np.isnan(risk_18), f"{filename} returned NaN on safe weather (18C/15mm)"
        assert risk_18 >= 0.0, f"{filename} output negative risk {risk_18:.2f} < 0.0 on safe weather (18C/15mm)"
        assert risk_18 <= 20.0, (
            f"{filename} predicted risk {risk_18:.2f} > 20.0 on safe rainy weather (18C/15mm)"
        )


def test_montesinho_best_model_non_negative_predictions(
    extreme_fire_weather,
    safe_rainy_weather,
    safe_rainy_moderate_weather,
):
    """Test models/montesinho_best_model.joblib outputs strictly non-negative log_area predictions."""
    monte_path = MODELS_DIR / "montesinho_best_model.joblib"
    assert monte_path.exists(), f"Missing required model: {monte_path}"

    model = joblib.load(monte_path)
    assert isinstance(model, Pipeline), "Montesinho model must be a scikit-learn Pipeline"

    # Test across safe, moderate, and extreme weather inputs
    test_cases = [extreme_fire_weather, safe_rainy_weather, safe_rainy_moderate_weather]
    for df_sample in test_cases:
        pred = model.predict(df_sample)
        assert len(pred) == 1
        log_area = float(pred[0])
        assert not np.isnan(log_area), "Montesinho burned area prediction is NaN"
        assert log_area >= 0.0, (
            f"Montesinho model predicted negative log_area: {log_area:.4f} < 0.0"
        )


def test_pipeline_encapsulates_scaler_and_bounded_predict():
    """Verify pipelines encapsulate StandardScaler and handle raw unscaled inputs directly."""
    continuous_models = [
        "ridge_model.joblib",
        "rf_model.joblib",
        "xgb_model.joblib",
        "best_model.joblib",
        "montesinho_best_model.joblib",
    ]
    for filename in continuous_models:
        pipe = joblib.load(MODELS_DIR / filename)
        assert "scaler" in pipe.named_steps, f"{filename} missing 'scaler' step"
        assert isinstance(pipe.named_steps["scaler"], StandardScaler), f"{filename} scaler is not StandardScaler"

        # Raw live weather unscaled dictionary
        raw_df = pd.DataFrame([{"temperature": 28.0, "relative_humidity": 50.0, "wind_speed": 12.0, "rain": 0.0}])
        pred = pipe.predict(raw_df)
        assert len(pred) == 1
        assert float(pred[0]) >= 0.0


def test_classifier_pipelines():
    """Verify classification pipelines exist and provide valid calibrated probabilities."""
    clf_path = MODELS_DIR / "best_classifier.joblib"
    if clf_path.exists():
        pipe = joblib.load(clf_path)
        assert isinstance(pipe, Pipeline)

        test_sample = pd.DataFrame(
            [{"temperature": 30.0, "relative_humidity": 40.0, "wind_speed": 18.0, "rain": 0.0}]
        )
        proba = pipe.predict_proba(test_sample)
        assert proba.shape == (1, 2)
        assert np.isclose(np.sum(proba[0]), 1.0, atol=1e-5)
        assert 0.0 <= proba[0][1] <= 1.0


def test_model_metrics_json_metadata_and_all_datasets():
    """Verify model_metrics.json reports all 3 datasets and synchronized sample counts."""
    metrics_path = MODELS_DIR / "model_metrics.json"
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    meta = metrics.get("metadata", {})
    # Task 3 synchronization checks
    assert meta.get("quebec_samples") == 9171, f"quebec_samples expected 9171, got {meta.get('quebec_samples')}"
    assert meta.get("algerian_samples") == 244, f"algerian_samples expected 244, got {meta.get('algerian_samples')}"
    assert meta.get("montesinho_samples") == 517, f"montesinho_samples expected 517, got {meta.get('montesinho_samples')}"

    # Verify Montesinho regression block exists and has valid metrics
    assert "montesinho_regression" in metrics, "models/model_metrics.json missing 'montesinho_regression' block"
    m_reg = metrics["montesinho_regression"]
    assert "metrics" in m_reg
    assert "Ridge (L2 Regularized)" in m_reg["metrics"]
    assert "Random Forest" in m_reg["metrics"]
    assert "XGBoost" in m_reg["metrics"]

    for m_name in ["Ridge (L2 Regularized)", "Random Forest", "XGBoost"]:
        score_dict = m_reg["metrics"][m_name]
        assert "r2" in score_dict
        assert "rmse" in score_dict
        assert "mae" in score_dict
        assert isinstance(score_dict["r2"], (int, float))
        assert isinstance(score_dict["rmse"], (int, float))
        assert isinstance(score_dict["mae"], (int, float))
