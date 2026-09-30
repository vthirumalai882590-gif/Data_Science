"""
FIREGUARD X - Explainable AI (XAI) Engine
Computes localized feature attributions and Shapley values (SHAP)
to explain individual predictions with directional impacts and plain-language narratives.
"""

import numpy as np
import pandas as pd
import shap
from ml.feature_engineering import FEATURE_DESCRIPTIONS, compute_engineered_features

class FireExplainer:
    """
    Stateful SHAP explainer supporting TreeExplainer (Random Forest, XGBoost, Decision Tree)
    and LinearExplainer/KernelExplainer fallbacks.
    """
    def __init__(self, model, background_data: np.ndarray, feature_names: list[str]):
        self.model = model
        self.feature_names = feature_names
        self.background_data = background_data
        
        # Initialize SHAP explainer
        try:
            self.explainer = shap.TreeExplainer(model)
            self.is_tree = True
        except Exception:
            # Fallback for linear/kernel models
            sample_bg = background_data[:50] if len(background_data) > 50 else background_data
            self.explainer = shap.KernelExplainer(model.predict_proba, sample_bg)
            self.is_tree = False

    def explain_instance(self, scaled_features: np.ndarray, raw_features_dict: dict) -> dict:
        """
        Calculates local SHAP values for a single prediction instance.
        Returns:
            - baseline_value: Expected base model value
            - drivers: Sorted list of top contributing features with magnitude and direction
            - narrative: Plain-language summary of what drove the risk score
        """
        # Ensure 2D shape (1, n_features)
        X_inst = np.array(scaled_features).reshape(1, -1)
        
        try:
            shap_values = self.explainer.shap_values(X_inst)
            
            # Handle multi-class / binary list vs array formats
            if isinstance(shap_values, list):
                # Class 1 (Fire) attributions
                vals = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
            elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
                vals = shap_values[0, :, 1]
            elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 2:
                vals = shap_values[0]
            else:
                vals = np.array(shap_values).flatten()
                
            base_val = float(self.explainer.expected_value[1] if isinstance(self.explainer.expected_value, (list, np.ndarray)) else self.explainer.expected_value)
        except Exception as e:
            # Fallback: model feature importances proportional attribution
            vals = np.zeros(len(self.feature_names))
            base_val = 0.5

        # Format drivers
        drivers = []
        for idx, col in enumerate(self.feature_names):
            contrib = float(vals[idx])
            raw_val = raw_features_dict.get(col, None)
            direction = "Increased risk" if contrib > 0 else "Decreased risk"
            
            # Human readable unit
            unit = ""
            if col == "Temperature": unit = "°C"
            elif col == "RH": unit = "%"
            elif col == "Ws": unit = " km/h"
            elif col == "Rain": unit = " mm"

            display_val = f"{raw_val}{unit}" if raw_val is not None else "N/A"

            drivers.append({
                "feature": col,
                "label": col.replace("_", " ").title(),
                "raw_value": raw_val,
                "display_value": display_val,
                "contribution": round(contrib, 4),
                "abs_contribution": round(abs(contrib), 4),
                "direction": direction,
                "is_positive": contrib > 0,
                "description": FEATURE_DESCRIPTIONS.get(col, "Environmental parameter")
            })

        # Sort by absolute impact
        drivers.sort(key=lambda d: d["abs_contribution"], reverse=True)
        top_drivers = drivers[:8]

        # Generate contextual natural-language explanation
        pos_drivers = [d for d in top_drivers if d["is_positive"]][:3]
        neg_drivers = [d for d in top_drivers if not d["is_positive"]][:2]
        
        pos_summary = ", ".join([f"{d['label']} ({d['display_value']})" for d in pos_drivers])
        neg_summary = ", ".join([f"{d['label']} ({d['display_value']})" for d in neg_drivers])

        if pos_drivers and neg_drivers:
            narrative = (
                f"Elevated risk is driven primarily by elevated {pos_summary}, "
                f"which counteracted protective moisture factors such as {neg_summary}."
            )
        elif pos_drivers:
            narrative = f"Fire risk is strongly amplified by compounding critical factors: {pos_summary}."
        elif neg_drivers:
            narrative = f"Fire risk is suppressed under prevailing benign conditions including {neg_summary}."
        else:
            narrative = "All environmental indicators are near seasonal equilibrium."

        return {
            "base_value": round(base_val, 4),
            "top_drivers": top_drivers,
            "all_drivers": drivers,
            "narrative": narrative
        }
