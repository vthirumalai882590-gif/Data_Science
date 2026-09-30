"""
FIREGUARD X - Prediction Service
Orchestrates model inference, preprocessing, risk index calculation,
SHAP feature explanation, data quality auditing, and environmental anomaly detection.
"""

import datetime
import pandas as pd
import numpy as np
from ml.model_registry import get_registry
from ml.predict import calculate_fire_risk_score, assess_data_quality, PHYSICAL_BOUNDS
from ml.feature_engineering import compute_engineered_features

def run_prediction_pipeline(inputs_dict: dict) -> dict:
    """
    Executes the complete production prediction workflow.
    """
    registry = get_registry()
    if not registry.is_loaded:
        raise RuntimeError("ML Models and Preprocessors have not been loaded into the registry.")

    # 1. Audit Data Quality
    quality_audit = assess_data_quality(inputs_dict)

    # 2. Impute defaults for any unsupplied optional fields
    normalized_inputs = {}
    for feat, bounds in PHYSICAL_BOUNDS.items():
        if feat in inputs_dict and inputs_dict[feat] is not None:
            normalized_inputs[feat] = float(inputs_dict[feat])
        else:
            normalized_inputs[feat] = float(bounds["default"])

    # 3. Anomaly Detection
    anomaly_result = registry.anomaly_detector.analyze(normalized_inputs)

    # 4. Feature Preprocessing
    df_raw = pd.DataFrame([normalized_inputs])
    X_scaled = registry.preprocessor.transform(df_raw)

    # 5. Model Inference
    # Calibrated class probability
    if hasattr(registry.model, "predict_proba"):
        prob = float(registry.model.predict_proba(X_scaled)[0, 1])
    else:
        prob = float(registry.model.predict(X_scaled)[0])

    # 6. Composite Risk Score
    risk_info = calculate_fire_risk_score(prob, normalized_inputs)

    # 7. Local SHAP Explanation
    explain_result = registry.explainer.explain_instance(X_scaled[0], normalized_inputs)

    return {
        "risk_score": risk_info["risk_score"],
        "risk_level": risk_info["risk_level"],
        "risk_badge": risk_info["risk_badge"],
        "risk_color": risk_info["risk_color"],
        "model_probability": risk_info["model_probability"],
        "probability_percent": risk_info["probability_percent"],
        "environmental_vulnerability": risk_info["environmental_vulnerability"],
        "data_quality": quality_audit,
        "anomaly": anomaly_result,
        "drivers": explain_result["top_drivers"],
        "narrative": explain_result["narrative"],
        "model_name": registry.metadata.get("model_name", "XGBoost"),
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "inputs": normalized_inputs,
    }

def run_what_if_analysis(baseline_inputs: dict, modified_inputs: dict) -> dict:
    """
    Evaluates scenario changes and computes comparative risk delta and drivers of change.
    """
    base_res = run_prediction_pipeline(baseline_inputs)
    mod_res = run_prediction_pipeline(modified_inputs)

    risk_delta = round(mod_res["risk_score"] - base_res["risk_score"], 1)
    
    if risk_delta > 0:
        delta_direction = "INCREASED RISK"
    elif risk_delta < 0:
        delta_direction = "DECREASED RISK"
    else:
        delta_direction = "UNCHANGED"

    # Identify primary drivers of delta
    drivers_of_change = []
    key_features = ["Temperature", "RH", "Ws", "Rain"]
    
    for feat in key_features:
        b_val = float(baseline_inputs.get(feat, 0.0))
        m_val = float(modified_inputs.get(feat, 0.0))
        diff = m_val - b_val
        
        if abs(diff) > 0.01:
            if feat == "Temperature":
                reason = "Higher temperature accelerates fuel evaporation" if diff > 0 else "Lower temperature reduces thermal stress"
            elif feat == "RH":
                reason = "Lower humidity severely dries fine fuels" if diff < 0 else "Higher humidity re-hydrates combustible leaf litter"
            elif feat == "Ws":
                reason = "Stronger winds enhance convective fire oxygenation" if diff > 0 else "Calmer winds slow spread velocity"
            elif feat == "Rain":
                reason = "Precipitation directly extinguishes/saturates organic matter" if diff > 0 else "Absence of rain perpetuates drought"
            else:
                reason = f"Parameter changed from {b_val} to {m_val}"

            drivers_of_change.append({
                "feature": feat,
                "baseline_value": b_val,
                "modified_value": m_val,
                "direction": "increased" if diff > 0 else "decreased",
                "reason": reason
            })

    return {
        "baseline_risk": base_res["risk_score"],
        "baseline_level": base_res["risk_level"],
        "modified_risk": mod_res["risk_score"],
        "modified_level": mod_res["risk_level"],
        "risk_delta": risk_delta,
        "delta_direction": delta_direction,
        "baseline_probability": base_res["model_probability"],
        "modified_probability": mod_res["model_probability"],
        "primary_drivers_of_change": drivers_of_change,
        "disclaimer": "The model associates this change with the statistical relationships observed in historical training data. Not a claim of isolated causal certainty."
    }
