"""
FIREGUARD X - Model Training and Evaluation Pipeline
Trains multiple machine learning models (Logistic Regression, Decision Tree,
Random Forest, XGBoost), conducts rigorous stratified evaluation,
trains an environmental anomaly detector, generates diagnostic figures,
and persists all production artifacts.
"""

import os
import sys

# Bootstrap repository root into sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json
import datetime
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from ml.config import (
    MODEL_PATH,
    ALL_MODELS_PATH,
    METRICS_PATH,
    METADATA_PATH,
    ANOMALY_MODEL_PATH,
    RANDOM_STATE,
    RAW_DATA_PATH,
)
from ml.preprocessing import prepare_and_split_data, CORE_NUMERICAL_COLS
from ml.evaluate import evaluate_classifier, generate_evaluation_visualizations
from ml.anomaly import EnvironmentalAnomalyDetector, save_anomaly_detector

def train_and_evaluate_all():
    print("=" * 60)
    print("      FIREGUARD X - MODEL TRAINING & EVALUATION PIPELINE      ")
    print("=" * 60)

    # 1. Prepare and split data
    print("\n[1/6] Loading & Preprocessing Dataset...")
    split_data = prepare_and_split_data()
    X_train = split_data["X_train"]
    X_test = split_data["X_test"]
    X_train_scaled = split_data["X_train_scaled"]
    X_test_scaled = split_data["X_test_scaled"]
    y_train = split_data["y_train"]
    y_test = split_data["y_test"]
    pipeline = split_data["pipeline"]
    raw_df = split_data["raw_df"]

    num_rows = len(raw_df)
    feature_names = pipeline.feature_names
    num_features = len(feature_names)
    print(f"Dataset Verified: {num_rows} rows, {num_features} total features.")
    print(f"Training Instances: {len(X_train)} | Test Instances: {len(X_test)}")

    # 2. Define Model Candidates
    print("\n[2/6] Initializing Candidate Model Architectures...")
    models = {
        "Logistic Regression": LogisticRegression(
            C=1.0, 
            max_iter=1000, 
            random_state=RANDOM_STATE
        ),
        "Decision Tree": DecisionTreeClassifier(
            max_depth=5, 
            min_samples_leaf=4, 
            random_state=RANDOM_STATE
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=150, 
            max_depth=7, 
            min_samples_leaf=2, 
            random_state=RANDOM_STATE
        ),
        "XGBoost": XGBClassifier(
            n_estimators=100, 
            max_depth=4, 
            learning_rate=0.08, 
            eval_metric="logloss", 
            random_state=RANDOM_STATE
        )
    }

    # 3. Train and Evaluate each model
    print("\n[3/6] Training & Evaluating Models with Stratified Test Split...")
    evaluation_results = {}
    fitted_models = {}

    for name, model in models.items():
        print(f"  -> Training {name}...")
        model.fit(X_train_scaled, y_train)
        fitted_models[name] = model
        
        metrics = evaluate_classifier(model, X_test_scaled, y_test, model_name=name)
        evaluation_results[name] = metrics
        print(f"     Acc: {metrics['accuracy']:.4f} | Prec: {metrics['precision']:.4f} | "
              f"Rec: {metrics['recall']:.4f} | F1: {metrics['f1']:.4f} | ROC-AUC: {metrics['roc_auc']:.4f}")

    # 4. Model Selection based on F1-Score & Recall (Fire safety preference)
    print("\n[4/6] Conducting Model Selection...")
    # Prioritize F1-Score with tie-breaker on Recall to minimize catastrophic False Negatives
    best_name = max(
        evaluation_results.keys(),
        key=lambda k: (evaluation_results[k]["f1"], evaluation_results[k]["recall"])
    )
    best_model = fitted_models[best_name]
    best_metrics = evaluation_results[best_name]
    print(f"  Selected Primary Model: {best_name}")
    print(f"  Selection Rationale: Highest combined harmonic mean (F1 = {best_metrics['f1']:.4f}) "
          f"and sensitivity (Recall = {best_metrics['recall']:.4f}) minimizing false negatives.")

    # 5. Fit Environmental Anomaly Detector
    print("\n[5/6] Fitting Isolation Forest Environmental Anomaly Detector...")
    anomaly_detector = EnvironmentalAnomalyDetector(contamination=0.08)
    anomaly_detector.fit(raw_df, CORE_NUMERICAL_COLS)
    save_anomaly_detector(anomaly_detector, ANOMALY_MODEL_PATH)
    print(f"  Anomaly Detector saved to {ANOMALY_MODEL_PATH}")

    # 6. Generate Figures & Persist Artifacts
    print("\n[6/6] Generating Visualizations and Saving Artifacts...")
    generate_evaluation_visualizations(fitted_models, X_test_scaled, y_test, feature_names)

    # Save best model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    
    # Save all models dictionary for live Model Lab comparison
    joblib.dump(fitted_models, ALL_MODELS_PATH)

    # Save metrics JSON
    metrics_payload = {
        "models": evaluation_results,
        "selected_model": best_name,
        "best_metrics": best_metrics,
        "features": feature_names,
        "test_size": len(y_test),
        "train_size": len(y_train),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics_payload, f, indent=2)

    # Save model metadata
    metadata = {
        "model_name": best_name,
        "model_type": type(best_model).__name__,
        "training_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "dataset": "UCI Algerian Forest Fires (Bejaia & Sidi Bel-abbes regions)",
        "features": feature_names,
        "core_features": CORE_NUMERICAL_COLS,
        "target": "Fire Occurrence (Classes: fire=1, not fire=0)",
        "metrics": best_metrics,
        "random_state": RANDOM_STATE,
        "evaluation_strategy": "Stratified 80/20 Train-Test Partition"
    }
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n" + "=" * 60)
    print("Training completed.")
    print(f"Dataset:")
    print(f"  Rows: {num_rows}")
    print(f"  Features: {num_features}")
    print("\nModels trained:")
    for name in models.keys():
        print(f"  - {name}")
    print(f"\nFinal model:")
    print(f"  {best_name}")
    print("\nMetrics:")
    print(f"  Accuracy:  {best_metrics['accuracy']:.4f}")
    print(f"  Precision: {best_metrics['precision']:.4f}")
    print(f"  Recall:    {best_metrics['recall']:.4f}")
    print(f"  F1:        {best_metrics['f1']:.4f}")
    print(f"  ROC-AUC:   {best_metrics['roc_auc']:.4f}")
    print("=" * 60)
    return metrics_payload

if __name__ == "__main__":
    train_and_evaluate_all()
