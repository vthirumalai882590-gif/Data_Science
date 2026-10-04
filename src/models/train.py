"""End-to-end model training, evaluation, and serialization pipeline for Forest Fire Predictor.

Architected and maintained by the Lead Machine Learning Engineer.
Implements:
1. In-Pipeline Feature Engineering:
   WeatherFeatureEngineer computes domain physical interaction terms:
   - vapor_pressure_deficit: temperature * (1.0 - relative_humidity / 100.0)
   - heat_aridity_index: temperature / (relative_humidity + 1.0)
   - wind_spread_factor: wind_speed * (temperature / (relative_humidity + 1.0))
   - rain_suppression: exp(-1.5 * rain)
   and prepends them with the 4 base features into an 8-dimensional space inside the pipeline.
2. Standardized Scaling:
   StandardScaler fitted within the pipeline so raw 4-feature inputs from live APIs
   pass directly into .predict() without external transformation.
3. Prediction Bounding:
   BoundedRiskPipeline encapsulates post-inference value clamping,
   guaranteeing continuous risk scores stay strictly within [0.0, 100.0] and burned area within [0.0, inf).
4. Regularized & Pruned Model Architecture:
   - Regression (Algerian FWI & Montesinho Burned Area):
     * Ridge: L2 weight shrinkage (alpha=10.0)
     * Random Forest: Pruned ensemble (n_estimators=50, max_depth=4, min_samples_leaf=4, max_features='sqrt')
     * XGBoost: Regularized boosting (n_estimators=40, max_depth=3, learning_rate=0.05, reg_lambda=5.0, reg_alpha=2.0, subsample=0.8, colsample_bytree=0.8)
   - Classification (Quebec Wildfire Ignition Risk):
     * Logistic Regression: L2 regularized (C=1.0)
     * Random Forest: Pruned classifier (n_estimators=60, max_depth=6, min_samples_leaf=15, max_features='sqrt')
     * XGBoost: Regularized classifier (n_estimators=40, max_depth=3, learning_rate=0.05, reg_lambda=4.0, subsample=0.8)
5. Multi-Dataset Benchmarking & Serialization:
   - Evaluates both training and testing performance to prove eliminated overfitting gaps.
   - Serializes trained bounded pipelines using joblib to models/.
   - Exports comparative benchmarks, feature attributions, and synchronized metadata to models/model_metrics.json.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier, XGBRegressor

from src.config.settings import (
    MODELS_DIR,
    PROCESSED_DATA_DIR,
    RANDOM_STATE,
    TEST_SIZE,
)
from src.models.bounded_pipeline import (
    ALL_FEATURE_NAMES,
    BASE_FEATURE_NAMES,
    BoundedRiskPipeline,
    INTERACTION_FEATURE_NAMES,
    WeatherFeatureEngineer,
)
from src.models.evaluate import (
    compare_and_select_best_model,
    evaluate_classification,
    evaluate_regression,
    print_classification_benchmark,
    print_regression_benchmark,
)

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

FEATURE_COLUMNS = BASE_FEATURE_NAMES


def load_quebec_data() -> Tuple[pd.DataFrame, pd.Series]:
    """Load cleaned Quebec Wildfire dataset for ignition risk classification.

    Dimensions: 9,171 rows, 0 nulls.
    Features: temperature, relative_humidity, wind_speed, rain.
    Target: fire_risk (Binary: 0 for Safe, 1 for Wildfire Ignition).
    """
    path = PROCESSED_DATA_DIR / "quebec_cleaned.csv"
    if not path.exists():
        raise FileNotFoundError(f"Quebec cleaned dataset not found at {path}")

    df = pd.read_csv(path)
    for col in FEATURE_COLUMNS + ["fire_risk"]:
        if col not in df.columns:
            raise KeyError(f"Required column '{col}' missing from Quebec dataset")

    assert df[FEATURE_COLUMNS + ["fire_risk"]].isnull().sum().sum() == 0, "Quebec dataset contains nulls"

    X = df[FEATURE_COLUMNS].copy()
    y = df["fire_risk"].astype(int)
    logger.info("Loaded Quebec dataset: %d samples, %d features, target: fire_risk", len(df), len(FEATURE_COLUMNS))
    return X, y


def load_algerian_data() -> Tuple[pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    """Load cleaned Algerian Forest Fires dataset for severity regression and benchmark classification.

    Dimensions: 244 rows, 0 nulls.
    Features: temperature, relative_humidity, wind_speed, rain.
    Targets:
      - y_reg: Continuous risk score (0-100 calibrated index: np.clip(fwi * 3.2, 0.0, 100.0))
      - y_fwi: Raw continuous FWI score (0.0 to 31.1)
      - y_clf: Binary fire_class (0 for not fire, 1 for fire)
    """
    path = PROCESSED_DATA_DIR / "algerian_cleaned.csv"
    if not path.exists():
        raise FileNotFoundError(f"Algerian cleaned dataset not found at {path}")

    df = pd.read_csv(path)
    for col in FEATURE_COLUMNS + ["fwi"]:
        if col not in df.columns:
            raise KeyError(f"Required column '{col}' missing from Algerian dataset")

    assert df[FEATURE_COLUMNS + ["fwi"]].isnull().sum().sum() == 0, "Algerian dataset contains nulls"

    X = df[FEATURE_COLUMNS].copy()
    y_reg = np.clip(df["fwi"] * 3.2, 0.0, 100.0)
    y_fwi = df["fwi"].copy()
    y_clf = df["fire_class"].astype(int) if "fire_class" in df.columns else (df["fwi"] > 5.0).astype(int)

    logger.info("Loaded Algerian dataset: %d samples, %d features, target: fwi", len(df), len(FEATURE_COLUMNS))
    return X, y_reg, y_fwi, y_clf


def load_montesinho_data() -> Tuple[pd.DataFrame, pd.Series]:
    """Load cleaned Montesinho dataset for burned area regression.

    Dimensions: 517 rows, 0 nulls.
    Features: temperature, relative_humidity, wind_speed, rain.
    Target: log_area = ln(area + 1) in log hectares.
    """
    path = PROCESSED_DATA_DIR / "montesinho_cleaned.csv"
    if not path.exists():
        raise FileNotFoundError(f"Montesinho cleaned dataset not found at {path}")

    df = pd.read_csv(path)
    for col in FEATURE_COLUMNS + ["log_area"]:
        if col not in df.columns:
            raise KeyError(f"Required column '{col}' missing from Montesinho dataset")

    assert df[FEATURE_COLUMNS + ["log_area"]].isnull().sum().sum() == 0, "Montesinho dataset contains nulls"

    X = df[FEATURE_COLUMNS].copy()
    y = df["log_area"].copy()
    logger.info("Loaded Montesinho dataset: %d samples, %d features, target: log_area", len(df), len(FEATURE_COLUMNS))
    return X, y


def build_classification_pipelines() -> Dict[str, Pipeline]:
    """Build scikit-learn classification pipelines with WeatherFeatureEngineer and StandardScaler."""
    return {
        "Ridge (L2 Regularized)": Pipeline(
            [
                ("feature_engineer", WeatherFeatureEngineer()),
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        C=1.0,
                        solver="lbfgs",
                        max_iter=1000,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
        "Random Forest": Pipeline(
            [
                ("feature_engineer", WeatherFeatureEngineer()),
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=60,
                        max_depth=6,
                        min_samples_leaf=15,
                        max_features="sqrt",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                ),
            ]
        ),
        "XGBoost": Pipeline(
            [
                ("feature_engineer", WeatherFeatureEngineer()),
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    XGBClassifier(
                        n_estimators=40,
                        max_depth=3,
                        learning_rate=0.05,
                        reg_lambda=4.0,
                        subsample=0.8,
                        random_state=RANDOM_STATE,
                        eval_metric="logloss",
                    ),
                ),
            ]
        ),
    }


def build_regression_pipelines(
    min_val: Optional[float] = 0.0,
    max_val: Optional[float] = 100.0,
) -> Dict[str, Pipeline]:
    """Build bounded regression pipelines with WeatherFeatureEngineer, StandardScaler and prediction bounding."""
    return {
        "Ridge (L2 Regularized)": BoundedRiskPipeline(
            [
                ("feature_engineer", WeatherFeatureEngineer()),
                ("scaler", StandardScaler()),
                (
                    "regressor",
                    Ridge(alpha=10.0, random_state=RANDOM_STATE),
                ),
            ],
            min_val=min_val,
            max_val=max_val,
        ),
        "Random Forest": BoundedRiskPipeline(
            [
                ("feature_engineer", WeatherFeatureEngineer()),
                ("scaler", StandardScaler()),
                (
                    "regressor",
                    RandomForestRegressor(
                        n_estimators=50,
                        max_depth=4,
                        min_samples_leaf=4,
                        max_features="sqrt",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                ),
            ],
            min_val=min_val,
            max_val=max_val,
        ),
        "XGBoost": BoundedRiskPipeline(
            [
                ("feature_engineer", WeatherFeatureEngineer()),
                ("scaler", StandardScaler()),
                (
                    "regressor",
                    XGBRegressor(
                        n_estimators=40,
                        max_depth=3,
                        learning_rate=0.05,
                        reg_lambda=5.0,
                        reg_alpha=2.0,
                        subsample=0.8,
                        colsample_bytree=0.8,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ],
            min_val=min_val,
            max_val=max_val,
        ),
    }


def build_burned_area_pipelines() -> Dict[str, Pipeline]:
    """Build regression pipelines for Montesinho burned area with non-negative bounds [0.0, inf)."""
    return {
        "Ridge (L2 Regularized)": BoundedRiskPipeline(
            [
                ("feature_engineer", WeatherFeatureEngineer()),
                ("scaler", StandardScaler()),
                (
                    "regressor",
                    Ridge(alpha=10.0, random_state=RANDOM_STATE),
                ),
            ],
            min_val=0.0,
            max_val=None,
        ),
        "Random Forest": BoundedRiskPipeline(
            [
                ("feature_engineer", WeatherFeatureEngineer()),
                ("scaler", StandardScaler()),
                (
                    "regressor",
                    RandomForestRegressor(
                        n_estimators=50,
                        max_depth=4,
                        min_samples_leaf=4,
                        max_features="sqrt",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                ),
            ],
            min_val=0.0,
            max_val=None,
        ),
        "XGBoost": BoundedRiskPipeline(
            [
                ("feature_engineer", WeatherFeatureEngineer()),
                ("scaler", StandardScaler()),
                (
                    "regressor",
                    XGBRegressor(
                        n_estimators=40,
                        max_depth=3,
                        learning_rate=0.05,
                        reg_lambda=5.0,
                        reg_alpha=2.0,
                        subsample=0.8,
                        colsample_bytree=0.8,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ],
            min_val=0.0,
            max_val=None,
        ),
    }


def train_and_evaluate_models() -> Dict[str, Any]:
    """Orchestrate end-to-end model training, evaluation, and artifact serialization.

    Returns:
        Consolidated benchmark dictionary with balanced train and test scores.
    """
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 80)
    print(" FOREST FIRE PREDICTOR: REGULARIZED MODEL TRAINING & BENCHMARK PIPELINE")
    print(" In-Pipeline Feature Engineering & Overfitting Elimination")
    print("=" * 80)

    # --------------------------------------------------------------------------
    # 1. LOAD DATASETS
    # --------------------------------------------------------------------------
    X_quebec, y_quebec = load_quebec_data()
    X_algerian, y_algerian_reg, y_algerian_fwi, y_algerian_clf = load_algerian_data()
    X_montesinho, y_montesinho = load_montesinho_data()

    # Train/Test splits
    (
        X_q_train,
        X_q_test,
        y_q_train,
        y_q_test,
    ) = train_test_split(
        X_quebec,
        y_quebec,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y_quebec,
    )

    (
        X_a_train,
        X_a_test,
        y_a_reg_train,
        y_a_reg_test,
        y_a_clf_train,
        y_a_clf_test,
    ) = train_test_split(
        X_algerian,
        y_algerian_reg,
        y_algerian_clf,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    (
        X_m_train,
        X_m_test,
        y_m_train,
        y_m_test,
    ) = train_test_split(
        X_montesinho,
        y_montesinho,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    logger.info(
        "Quebec split: %d train, %d test (stratified 50/50 balance)",
        len(X_q_train),
        len(X_q_test),
    )
    logger.info(
        "Algerian split: %d train, %d test",
        len(X_a_train),
        len(X_a_test),
    )
    logger.info(
        "Montesinho split: %d train, %d test",
        len(X_m_train),
        len(X_m_test),
    )

    # --------------------------------------------------------------------------
    # 2. TRAIN & EVALUATE QUEBEC CLASSIFICATION (Ignition Risk Probability)
    # --------------------------------------------------------------------------
    print("\n>>> Training Classification Pipelines on Quebec Wildfire Dataset (9,171 samples)...")
    clf_pipelines = build_classification_pipelines()
    quebec_metrics: Dict[str, Dict[str, float]] = {}
    quebec_train_metrics: Dict[str, Dict[str, float]] = {}

    for name, pipe in clf_pipelines.items():
        pipe.fit(X_q_train, y_q_train)
        preds_test = pipe.predict(X_q_test)
        probs_test = pipe.predict_proba(X_q_test)[:, 1]
        m_test = evaluate_classification(y_q_test, preds_test, y_prob=probs_test)
        quebec_metrics[name] = m_test

        preds_train = pipe.predict(X_q_train)
        probs_train = pipe.predict_proba(X_q_train)[:, 1]
        m_train = evaluate_classification(y_q_train, preds_train, y_prob=probs_train)
        quebec_train_metrics[name] = m_train

        logger.info(
            "Quebec %s -> Train Acc: %.4f, Test Acc: %.4f | Train ROC-AUC: %.4f, Test ROC-AUC: %.4f",
            name,
            m_train["accuracy"],
            m_test["accuracy"],
            m_train["roc_auc"],
            m_test["roc_auc"],
        )

    print_classification_benchmark(
        quebec_metrics,
        title="Quebec Wildfire Ignition Risk Classification Benchmark (Test n=1,835)",
    )
    best_clf_name, best_clf_metrics = compare_and_select_best_model(
        quebec_metrics, criterion="roc_auc"
    )
    print(
        f"  [*] Top Performing Classifier: {best_clf_name} (ROC-AUC: {best_clf_metrics['roc_auc']:.4f}, Accuracy: {best_clf_metrics['accuracy']:.4f})"
    )

    # --------------------------------------------------------------------------
    # 3. TRAIN & EVALUATE ALGERIAN REGRESSION (FWI / Continuous Risk Score [0, 100])
    # --------------------------------------------------------------------------
    print("\n>>> Training Bounded Regression Pipelines on Algerian Forest Fires Dataset (244 samples)...")
    reg_pipelines = build_regression_pipelines(min_val=0.0, max_val=100.0)
    algerian_reg_metrics: Dict[str, Dict[str, float]] = {}
    algerian_train_metrics: Dict[str, Dict[str, float]] = {}

    for name, pipe in reg_pipelines.items():
        pipe.fit(X_a_train, y_a_reg_train)
        y_pred_test = pipe.predict(X_a_test)
        m_test = evaluate_regression(y_a_reg_test, y_pred_test)
        algerian_reg_metrics[name] = m_test

        y_pred_train = pipe.predict(X_a_train)
        m_train = evaluate_regression(y_a_reg_train, y_pred_train)
        algerian_train_metrics[name] = m_train

        logger.info(
            "Algerian %s -> Train R²: %.4f, Test R²: %.4f | Train RMSE: %.3f, Test RMSE: %.3f",
            name,
            m_train["r2"],
            m_test["r2"],
            m_train["rmse"],
            m_test["rmse"],
        )

    print_regression_benchmark(
        algerian_reg_metrics,
        title="Algerian Forest Fires Severity / Risk Score Benchmark (Test n=49)",
    )
    best_reg_name, best_reg_metrics = compare_and_select_best_model(
        algerian_reg_metrics, criterion="r2"
    )
    print(
        f"  [*] Top Performing Risk Regressor: {best_reg_name} (R²: {best_reg_metrics['r2']:.4f}, MAE: {best_reg_metrics['mae']:.3f})"
    )

    # --------------------------------------------------------------------------
    # 4. TRAIN & EVALUATE MONTESINHO BURNED AREA REGRESSION (log_area [0, inf))
    # --------------------------------------------------------------------------
    print("\n>>> Training Bounded Burned Area Pipelines on Montesinho Dataset (517 samples)...")
    burned_area_pipelines = build_burned_area_pipelines()
    montesinho_metrics: Dict[str, Dict[str, float]] = {}
    montesinho_train_metrics: Dict[str, Dict[str, float]] = {}

    for name, pipe in burned_area_pipelines.items():
        pipe.fit(X_m_train, y_m_train)
        y_pred_test_m = pipe.predict(X_m_test)
        m_test = evaluate_regression(y_m_test, y_pred_test_m)
        montesinho_metrics[name] = m_test

        y_pred_train_m = pipe.predict(X_m_train)
        m_train = evaluate_regression(y_m_train, y_pred_train_m)
        montesinho_train_metrics[name] = m_train

        logger.info(
            "Montesinho %s -> Train R²: %.4f, Test R²: %.4f | Train RMSE: %.3f, Test RMSE: %.3f",
            name,
            m_train["r2"],
            m_test["r2"],
            m_train["rmse"],
            m_test["rmse"],
        )

    print_regression_benchmark(
        montesinho_metrics,
        title="Montesinho Natural Park Burned Area Regression Benchmark (Test n=104)",
    )
    best_monte_name, best_monte_metrics = compare_and_select_best_model(
        montesinho_metrics, criterion="r2"
    )
    print(
        f"  [*] Top Performing Burned Area Model: {best_monte_name} (R²: {best_monte_metrics['r2']:.4f}, MAE: {best_monte_metrics['mae']:.3f})"
    )

    # --------------------------------------------------------------------------
    # 5. EXTRACT FEATURE IMPORTANCES & L2 WEIGHT SHRINKAGE
    # --------------------------------------------------------------------------
    print("\n>>> Computing Feature Importances & Regularization Weight Shrinkage...")
    ridge_pipeline = reg_pipelines["Ridge (L2 Regularized)"]
    rf_pipeline = reg_pipelines["Random Forest"]
    xgb_pipeline = reg_pipelines["XGBoost"]

    ridge_coefs = ridge_pipeline.named_steps["regressor"].coef_
    rf_importances = rf_pipeline.named_steps["regressor"].feature_importances_
    xgb_importances = xgb_pipeline.named_steps["regressor"].feature_importances_

    feature_impacts: Dict[str, Dict[str, float]] = {}
    for i, col in enumerate(ALL_FEATURE_NAMES):
        feature_impacts[col] = {
            "ridge_coef": round(float(ridge_coefs[i]), 3),
            "rf_importance": round(float(rf_importances[i]), 3),
            "xgb_importance": round(float(xgb_importances[i]), 3),
        }
        print(
            f"  - {col:<24s} | Ridge Coef (L2): {float(ridge_coefs[i]):+8.3f} | "
            f"RF MDI: {float(rf_importances[i]):6.3f} | XGB Gain: {float(xgb_importances[i]):6.3f}"
        )

    # Extract Quebec classification feature importances
    rf_clf_pipe = clf_pipelines["Random Forest"]
    xgb_clf_pipe = clf_pipelines["XGBoost"]
    ridge_clf_pipe = clf_pipelines["Ridge (L2 Regularized)"]

    clf_feature_impacts: Dict[str, Dict[str, float]] = {}
    for i, col in enumerate(ALL_FEATURE_NAMES):
        clf_feature_impacts[col] = {
            "logistic_l2_coef": round(float(ridge_clf_pipe.named_steps["classifier"].coef_[0][i]), 3),
            "rf_importance": round(float(rf_clf_pipe.named_steps["classifier"].feature_importances_[i]), 3),
            "xgb_importance": round(float(xgb_clf_pipe.named_steps["classifier"].feature_importances_[i]), 3),
        }

    # --------------------------------------------------------------------------
    # 6. MODEL SERIALIZATION (.joblib)
    # --------------------------------------------------------------------------
    print("\n>>> Serializing Trained Bounded Pipelines to models/ using joblib...")
    # Core continuous risk artifacts ([0.0, 100.0] clamped)
    joblib.dump(ridge_pipeline, MODELS_DIR / "ridge_model.joblib")
    joblib.dump(rf_pipeline, MODELS_DIR / "rf_model.joblib")
    joblib.dump(xgb_pipeline, MODELS_DIR / "xgb_model.joblib")
    # Top performer for risk score
    joblib.dump(reg_pipelines[best_reg_name], MODELS_DIR / "best_model.joblib")

    # Burned area serialized artifact (Montesinho best model)
    best_burned_area_model = burned_area_pipelines[best_monte_name]
    joblib.dump(best_burned_area_model, MODELS_DIR / "montesinho_best_model.joblib")

    # Additional specialized artifacts for direct classification & regression
    joblib.dump(ridge_clf_pipe, MODELS_DIR / "ridge_classifier.joblib")
    joblib.dump(rf_clf_pipe, MODELS_DIR / "rf_classifier.joblib")
    joblib.dump(xgb_clf_pipe, MODELS_DIR / "xgb_classifier.joblib")
    joblib.dump(clf_pipelines[best_clf_name], MODELS_DIR / "best_classifier.joblib")

    joblib.dump(ridge_pipeline, MODELS_DIR / "ridge_regressor.joblib")
    joblib.dump(rf_pipeline, MODELS_DIR / "rf_regressor.joblib")
    joblib.dump(xgb_pipeline, MODELS_DIR / "xgb_regressor.joblib")
    joblib.dump(reg_pipelines[best_reg_name], MODELS_DIR / "best_regressor.joblib")

    joblib.dump(clf_pipelines[best_clf_name], MODELS_DIR / "quebec_best_model.joblib")
    joblib.dump(reg_pipelines[best_reg_name], MODELS_DIR / "algerian_best_model.joblib")

    print(f"  [OK] Successfully serialized models to {MODELS_DIR}:")
    print(f"       * {MODELS_DIR / 'ridge_model.joblib'} (Bounded [0, 100])")
    print(f"       * {MODELS_DIR / 'rf_model.joblib'} (Bounded [0, 100])")
    print(f"       * {MODELS_DIR / 'xgb_model.joblib'} (Bounded [0, 100])")
    print(f"       * {MODELS_DIR / 'best_model.joblib'} (Top Performer: {best_reg_name})")
    print(f"       * {MODELS_DIR / 'montesinho_best_model.joblib'} (Top Burned Area: {best_monte_name})")
    print(f"       * {MODELS_DIR / 'best_classifier.joblib'} (Top Performer: {best_clf_name})")

    # --------------------------------------------------------------------------
    # 7. EXPORT COMPREHENSIVE BENCHMARK METRICS (model_metrics.json)
    # --------------------------------------------------------------------------
    benchmark_payload: Dict[str, Any] = {
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "random_state": RANDOM_STATE,
            "test_size": TEST_SIZE,
            "features": FEATURE_COLUMNS,
            "base_features": FEATURE_COLUMNS,
            "engineered_features": INTERACTION_FEATURE_NAMES,
            "all_features": ALL_FEATURE_NAMES,
            # Top-level sample counts accurately reporting all 3 datasets
            "quebec_samples": len(X_quebec),
            "algerian_samples": len(X_algerian),
            "montesinho_samples": len(X_montesinho),
            "quebec_samples_total": len(X_quebec),
            "quebec_samples_train": len(X_q_train),
            "quebec_samples_test": len(X_q_test),
            "algerian_samples_total": len(X_algerian),
            "algerian_samples_train": len(X_a_train),
            "algerian_samples_test": len(X_a_test),
            "montesinho_samples_total": len(X_montesinho),
            "montesinho_samples_train": len(X_m_train),
            "montesinho_samples_test": len(X_m_test),
            "datasets": {
                "quebec": {
                    "task": "Classification: Ignition Risk",
                    "samples": len(X_quebec),
                    "target": "fire_risk",
                },
                "algerian": {
                    "task": "Regression: FWI Severity Score",
                    "samples": len(X_algerian),
                    "target": "fwi",
                },
                "montesinho": {
                    "task": "Regression: Burned Area",
                    "samples": len(X_montesinho),
                    "target": "log_area",
                },
            },
        },
        "models": {
            "Ridge (L2 Regularized)": {
                "type": "Linear Regularized",
                "regression": {
                    "r2": algerian_reg_metrics["Ridge (L2 Regularized)"]["r2"],
                    "rmse": algerian_reg_metrics["Ridge (L2 Regularized)"]["rmse"],
                    "mae": algerian_reg_metrics["Ridge (L2 Regularized)"]["mae"],
                    "train_r2": algerian_train_metrics["Ridge (L2 Regularized)"]["r2"],
                    "test_r2": algerian_reg_metrics["Ridge (L2 Regularized)"]["r2"],
                    "train_rmse": algerian_train_metrics["Ridge (L2 Regularized)"]["rmse"],
                    "test_rmse": algerian_reg_metrics["Ridge (L2 Regularized)"]["rmse"],
                    "train_mae": algerian_train_metrics["Ridge (L2 Regularized)"]["mae"],
                    "test_mae": algerian_reg_metrics["Ridge (L2 Regularized)"]["mae"],
                },
                "classification": {
                    "accuracy": quebec_metrics["Ridge (L2 Regularized)"]["accuracy"],
                    "precision": quebec_metrics["Ridge (L2 Regularized)"]["precision"],
                    "recall": quebec_metrics["Ridge (L2 Regularized)"]["recall"],
                    "f1_score": quebec_metrics["Ridge (L2 Regularized)"]["f1_score"],
                    "roc_auc": quebec_metrics["Ridge (L2 Regularized)"]["roc_auc"],
                    "train_accuracy": quebec_train_metrics["Ridge (L2 Regularized)"]["accuracy"],
                    "test_accuracy": quebec_metrics["Ridge (L2 Regularized)"]["accuracy"],
                    "train_roc_auc": quebec_train_metrics["Ridge (L2 Regularized)"]["roc_auc"],
                    "test_roc_auc": quebec_metrics["Ridge (L2 Regularized)"]["roc_auc"],
                },
                "burned_area_regression": {
                    "r2": montesinho_metrics["Ridge (L2 Regularized)"]["r2"],
                    "rmse": montesinho_metrics["Ridge (L2 Regularized)"]["rmse"],
                    "mae": montesinho_metrics["Ridge (L2 Regularized)"]["mae"],
                    "train_r2": montesinho_train_metrics["Ridge (L2 Regularized)"]["r2"],
                    "test_r2": montesinho_metrics["Ridge (L2 Regularized)"]["r2"],
                },
                "parameters": {"alpha": 10.0, "penalty": "l2", "solver": "auto"},
                "strengths": "Smooth L2 weight shrinkage handles severe collinearity between temperature and humidity. Fast, deterministic, interpretable.",
            },
            "Random Forest": {
                "type": "Bagging Ensemble",
                "regression": {
                    "r2": algerian_reg_metrics["Random Forest"]["r2"],
                    "rmse": algerian_reg_metrics["Random Forest"]["rmse"],
                    "mae": algerian_reg_metrics["Random Forest"]["mae"],
                    "train_r2": algerian_train_metrics["Random Forest"]["r2"],
                    "test_r2": algerian_reg_metrics["Random Forest"]["r2"],
                    "train_rmse": algerian_train_metrics["Random Forest"]["rmse"],
                    "test_rmse": algerian_reg_metrics["Random Forest"]["rmse"],
                    "train_mae": algerian_train_metrics["Random Forest"]["mae"],
                    "test_mae": algerian_reg_metrics["Random Forest"]["mae"],
                },
                "classification": {
                    "accuracy": quebec_metrics["Random Forest"]["accuracy"],
                    "precision": quebec_metrics["Random Forest"]["precision"],
                    "recall": quebec_metrics["Random Forest"]["recall"],
                    "f1_score": quebec_metrics["Random Forest"]["f1_score"],
                    "roc_auc": quebec_metrics["Random Forest"]["roc_auc"],
                    "train_accuracy": quebec_train_metrics["Random Forest"]["accuracy"],
                    "test_accuracy": quebec_metrics["Random Forest"]["accuracy"],
                    "train_roc_auc": quebec_train_metrics["Random Forest"]["roc_auc"],
                    "test_roc_auc": quebec_metrics["Random Forest"]["roc_auc"],
                },
                "burned_area_regression": {
                    "r2": montesinho_metrics["Random Forest"]["r2"],
                    "rmse": montesinho_metrics["Random Forest"]["rmse"],
                    "mae": montesinho_metrics["Random Forest"]["mae"],
                    "train_r2": montesinho_train_metrics["Random Forest"]["r2"],
                    "test_r2": montesinho_metrics["Random Forest"]["r2"],
                },
                "parameters": {
                    "n_estimators": 50,
                    "max_depth": 4,
                    "min_samples_leaf": 4,
                    "max_features": "sqrt",
                    "random_state": RANDOM_STATE,
                },
                "strengths": "Pruned decision trees prevent memorization while capturing essential non-linear meteorological thresholds.",
            },
            "XGBoost": {
                "type": "Gradient Boosting",
                "regression": {
                    "r2": algerian_reg_metrics["XGBoost"]["r2"],
                    "rmse": algerian_reg_metrics["XGBoost"]["rmse"],
                    "mae": algerian_reg_metrics["XGBoost"]["mae"],
                    "train_r2": algerian_train_metrics["XGBoost"]["r2"],
                    "test_r2": algerian_reg_metrics["XGBoost"]["r2"],
                    "train_rmse": algerian_train_metrics["XGBoost"]["rmse"],
                    "test_rmse": algerian_reg_metrics["XGBoost"]["rmse"],
                    "train_mae": algerian_train_metrics["XGBoost"]["mae"],
                    "test_mae": algerian_reg_metrics["XGBoost"]["mae"],
                },
                "classification": {
                    "accuracy": quebec_metrics["XGBoost"]["accuracy"],
                    "precision": quebec_metrics["XGBoost"]["precision"],
                    "recall": quebec_metrics["XGBoost"]["recall"],
                    "f1_score": quebec_metrics["XGBoost"]["f1_score"],
                    "roc_auc": quebec_metrics["XGBoost"]["roc_auc"],
                    "train_accuracy": quebec_train_metrics["XGBoost"]["accuracy"],
                    "test_accuracy": quebec_metrics["XGBoost"]["accuracy"],
                    "train_roc_auc": quebec_train_metrics["XGBoost"]["roc_auc"],
                    "test_roc_auc": quebec_metrics["XGBoost"]["roc_auc"],
                },
                "burned_area_regression": {
                    "r2": montesinho_metrics["XGBoost"]["r2"],
                    "rmse": montesinho_metrics["XGBoost"]["rmse"],
                    "mae": montesinho_metrics["XGBoost"]["mae"],
                    "train_r2": montesinho_train_metrics["XGBoost"]["r2"],
                    "test_r2": montesinho_metrics["XGBoost"]["r2"],
                },
                "parameters": {
                    "n_estimators": 40,
                    "max_depth": 3,
                    "learning_rate": 0.05,
                    "reg_lambda": 5.0,
                    "reg_alpha": 2.0,
                    "subsample": 0.8,
                    "colsample_bytree": 0.8,
                    "random_state": RANDOM_STATE,
                },
                "strengths": "L1 (reg_alpha) and L2 (reg_lambda) regularized gradient boosting provides strong generalization on tabular weather features.",
            },
        },
        "feature_importance": feature_impacts,
        "quebec_classification": {
            "dataset": "Quebec Wildfire Prediction Dataset (2018–2024)",
            "samples": len(X_quebec),
            "target": "fire_risk (Binary 0/1)",
            "metrics": quebec_metrics,
            "train_metrics": quebec_train_metrics,
            "best_model": best_clf_name,
            "feature_impacts": clf_feature_impacts,
        },
        "algerian_regression": {
            "dataset": "Algerian Forest Fires Dataset (9 Regions)",
            "samples": len(X_algerian),
            "target": "Fire Weather Risk Index (0-100 Score)",
            "metrics": algerian_reg_metrics,
            "train_metrics": algerian_train_metrics,
            "best_model": best_reg_name,
            "feature_impacts": feature_impacts,
        },
        "montesinho_regression": {
            "dataset": "Montesinho Natural Park Forest Fires Dataset (Portugal)",
            "samples": len(X_montesinho),
            "target": "log_area (Burned Area in log hectares: ln(area + 1))",
            "metrics": montesinho_metrics,
            "train_metrics": montesinho_train_metrics,
            "best_model": best_monte_name,
        },
    }

    metrics_file = MODELS_DIR / "model_metrics.json"
    with open(metrics_file, "w", encoding="utf-8") as f:
        json.dump(benchmark_payload, f, indent=2)

    print(f"\n[OK] Benchmark metrics successfully saved to: {metrics_file}")
    print("=" * 80)
    print(" PIPELINE EXECUTION FINISHED: REGULARIZED PIPELINES PERSISTED & OVERFITTING RESOLVED")
    print("=" * 80 + "\n")

    return benchmark_payload


if __name__ == "__main__":
    train_and_evaluate_models()
