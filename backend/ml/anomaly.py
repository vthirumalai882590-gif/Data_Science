"""
FIREGUARD X - Environmental Anomaly Detection Engine
Uses an Isolation Forest model combined with multivariate Z-score verification
against authentic historical baseline distributions to detect anomalous climatic conditions.
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from ml.config import ANOMALY_MODEL_PATH, RANDOM_STATE

class EnvironmentalAnomalyDetector:
    """
    Detects extreme or unprecedented combinations of weather conditions
    (e.g., compound heatwaves + severe humidity deficits + high winds)
    relative to the empirical historical distribution.
    """
    def __init__(self, contamination: float = 0.08):
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=RANDOM_STATE,
            n_estimators=100
        )
        self.feature_stats = {}
        self.fitted = False

    def fit(self, X: pd.DataFrame, feature_cols: list[str]):
        self.feature_cols = feature_cols
        X_sub = X[self.feature_cols].copy()
        
        # Calculate empirical baseline stats
        for col in self.feature_cols:
            vals = pd.to_numeric(X_sub[col], errors="coerce").dropna()
            self.feature_stats[col] = {
                "mean": float(vals.mean()),
                "std": float(vals.std()) if vals.std() > 0 else 1.0,
                "median": float(vals.median()),
                "q25": float(vals.quantile(0.25)),
                "q75": float(vals.quantile(0.75)),
                "min": float(vals.min()),
                "max": float(vals.max())
            }
            
        self.model.fit(X_sub)
        self.fitted = True
        return self

    def analyze(self, inputs: dict) -> dict:
        """
        Evaluate single or multiple environmental conditions for anomalies.
        Returns:
            - status: 'NORMAL', 'UNUSUAL', or 'HIGHLY UNUSUAL'
            - anomaly_score: float in [0.0, 1.0] (higher = more anomalous)
            - deviations: list of attributes deviating noticeably from historical normals
            - summary: plain-language narrative of the environmental condition
        """
        if not self.fitted:
            raise RuntimeError("Anomaly detector must be fitted before running analysis.")

        # Build feature vector for the model
        row = []
        deviations = []
        severe_count = 0

        for col in self.feature_cols:
            val = float(inputs.get(col, self.feature_stats[col]["median"]))
            row.append(val)
            
            stats = self.feature_stats[col]
            z_score = (val - stats["mean"]) / stats["std"]
            
            # Check for significant deviations (|z| >= 1.75)
            if abs(z_score) >= 1.75:
                direction = "higher" if z_score > 0 else "lower"
                deviations.append({
                    "feature": col,
                    "current_value": round(val, 2),
                    "historical_normal": round(stats["median"], 2),
                    "z_score": round(z_score, 2),
                    "direction": direction,
                    "severity": "severe" if abs(z_score) >= 2.5 else "moderate"
                })
                if abs(z_score) >= 2.5:
                    severe_count += 1

        # Isolation forest raw decision function (negative = outlier, positive = inlier)
        iso_score = float(self.model.decision_function([row])[0])
        # Normalize to 0 (normal) to 1 (highly anomalous)
        normalized_score = float(np.clip(0.5 - (iso_score * 2.0), 0.0, 1.0))

        # Categorize status
        if normalized_score >= 0.75 or severe_count >= 2:
            status = "HIGHLY UNUSUAL"
            badge = "⚠️ HIGHLY UNUSUAL"
        elif normalized_score >= 0.50 or len(deviations) >= 2:
            status = "UNUSUAL"
            badge = "⚠️ UNUSUAL"
        else:
            status = "NORMAL"
            badge = "✓ NORMAL"

        # Generate descriptive narrative
        if status != "NORMAL" and deviations:
            top_dev = deviations[0]
            narrative = (
                f"{status.capitalize()} atmospheric pattern detected. "
                f"{top_dev['feature']} ({top_dev['current_value']}) deviates substantially "
                f"from historical baseline ({top_dev['historical_normal']})."
            )
        else:
            narrative = "Observed environmental parameters align with historical baseline distributions."

        return {
            "status": status,
            "badge": badge,
            "anomaly_score": round(normalized_score, 3),
            "is_anomaly": status != "NORMAL",
            "deviations": deviations,
            "narrative": narrative
        }

def save_anomaly_detector(detector: EnvironmentalAnomalyDetector, path: str = ANOMALY_MODEL_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(detector, path)

def load_anomaly_detector(path: str = ANOMALY_MODEL_PATH) -> EnvironmentalAnomalyDetector:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Anomaly model artifact not found at {path}")
    return joblib.load(path)
