"""
FIREGUARD X - Explainable AI (XAI) Engine
Computes localized feature attributions and Shapley values (SHAP)
to explain individual predictions with directional impacts and plain-language narratives.
"""

import numpy as np
import pandas as pd
from ml.feature_engineering import FEATURE_DESCRIPTIONS, compute_engineered_features

try:
    import shap
    HAS_SHAP = True
except ImportError:
    shap = None
    HAS_SHAP = False

class FireExplainer:
    """
    High-performance Explainable AI (XAI) engine supporting:
    1. Native XGBoost C++ TreeSHAP (pred_contribs=True) for zero-dependency sub-millisecond attributions
    2. SHAP TreeExplainer / KernelExplainer if shap library is present
    3. Model importance-weighted deviation fallback
    """
    def __init__(self, model, background_data: np.ndarray, feature_names: list[str]):
        self.model = model
        self.feature_names = feature_names
        self.background_data = background_data
        self.explainer = None
        self.is_tree = False
        
        # Check if model has native XGBoost TreeSHAP capability
        if hasattr(self.model, "get_booster"):
            self.has_native_xgb = True
        else:
            self.has_native_xgb = False
            if HAS_SHAP and shap is not None:
                try:
                    self.explainer = shap.TreeExplainer(model)
                    self.is_tree = True
                except Exception:
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
        
        vals = None
        base_val = 0.5
        
        # 1. Native XGBoost TreeSHAP (C++ optimized, zero extra dependencies)
        if self.has_native_xgb:
            try:
                import xgboost as xgb
                dmat = xgb.DMatrix(X_inst, feature_names=self.feature_names)
                contribs = self.model.get_booster().predict(dmat, pred_contribs=True)
                vals = contribs[0, :-1]
                base_val = float(contribs[0, -1])
            except Exception:
                vals = None

        # 2. Standard SHAP library if available
        if vals is None and self.explainer is not None and HAS_SHAP:
            try:
                shap_values = self.explainer.shap_values(X_inst)
                if isinstance(shap_values, list):
                    vals = shap_values[1][0] if len(shap_values) > 1 else shap_values[0][0]
                elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
                    vals = shap_values[0, :, 1]
                elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 2:
                    vals = shap_values[0]
                else:
                    vals = np.array(shap_values).flatten()
                base_val = float(
                    self.explainer.expected_value[1]
                    if isinstance(self.explainer.expected_value, (list, np.ndarray))
                    else self.explainer.expected_value
                )
            except Exception:
                vals = None

        # 3. Fallback: feature importances / linear weights
        if vals is None:
            if hasattr(self.model, "feature_importances_"):
                fi = self.model.feature_importances_
                vals = np.array(X_inst[0]) * fi
            else:
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
