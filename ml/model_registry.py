"""
FIREGUARD X - Model Registry & Artifact Manager
Loads, caches, and provides thread-safe access to serialized model artifacts,
preprocessors, anomaly detectors, and SHAP explainers.
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from ml.config import (
    MODEL_PATH,
    ALL_MODELS_PATH,
    PREPROCESSOR_PATH,
    ANOMALY_MODEL_PATH,
    METRICS_PATH,
    FEATURE_NAMES_PATH,
    METADATA_PATH,
)
from ml.explain import FireExplainer
from ml.anomaly import EnvironmentalAnomalyDetector, load_anomaly_detector

class ModelRegistry:
    _instance = None

    def __init__(self):
        self.model = None
        self.all_models = {}
        self.preprocessor = None
        self.anomaly_detector = None
        self.explainer = None
        self.feature_names = []
        self.metrics = {}
        self.metadata = {}
        self.is_loaded = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load_artifacts(self, force_reload: bool = False):
        if self.is_loaded and not force_reload:
            return self

        # 1. Feature names
        if os.path.exists(FEATURE_NAMES_PATH):
            with open(FEATURE_NAMES_PATH, "r") as f:
                self.feature_names = json.load(f)

        # 2. Metrics
        if os.path.exists(METRICS_PATH):
            with open(METRICS_PATH, "r") as f:
                self.metrics = json.load(f)

        # 3. Metadata
        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, "r") as f:
                self.metadata = json.load(f)

        # 4. Preprocessor
        if os.path.exists(PREPROCESSOR_PATH):
            self.preprocessor = joblib.load(PREPROCESSOR_PATH)

        # 5. Primary Model
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)

        # 6. All models comparison dictionary
        if os.path.exists(ALL_MODELS_PATH):
            self.all_models = joblib.load(ALL_MODELS_PATH)
        elif self.model:
            self.all_models = {"Selected Model": self.model}

        # 7. Anomaly Detector
        if os.path.exists(ANOMALY_MODEL_PATH):
            self.anomaly_detector = load_anomaly_detector(ANOMALY_MODEL_PATH)

        # 8. SHAP Explainer
        if self.model and self.preprocessor and hasattr(self.preprocessor, "scaler"):
            try:
                # Synthetic background representation from preprocessor mean/std
                dim = len(self.feature_names) if self.feature_names else 16
                bg = np.zeros((30, dim))
                self.explainer = FireExplainer(self.model, bg, self.feature_names)
            except Exception as e:
                print(f"[ModelRegistry] Explainer initialization note: {e}")

        self.is_loaded = self.model is not None and self.preprocessor is not None
        return self

def get_registry() -> ModelRegistry:
    return ModelRegistry.get_instance().load_artifacts()
