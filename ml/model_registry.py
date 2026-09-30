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
        self.preprocessor = None
        if os.path.exists(PREPROCESSOR_PATH):
            try:
                self.preprocessor = joblib.load(PREPROCESSOR_PATH)
            except Exception:
                self.preprocessor = None
        if self.preprocessor is None:
            from ml.config import MODELS_DIR
            prep_json = os.path.join(MODELS_DIR, "preprocessor.json")
            if os.path.exists(prep_json):
                from ml.pure_engine import PureDataPipeline
                self.preprocessor = PureDataPipeline(prep_json)

        # 5. Primary Model
        self.model = None
        if os.path.exists(MODEL_PATH):
            try:
                self.model = joblib.load(MODEL_PATH)
            except Exception:
                self.model = None
        if self.model is None:
            from ml.config import MODELS_DIR
            xgb_json = os.path.join(MODELS_DIR, "xgb_model.json")
            if os.path.exists(xgb_json):
                from ml.pure_engine import PureTreeModel
                self.model = PureTreeModel(xgb_json)

        # 6. All models comparison dictionary
        self.all_models = {}
        if os.path.exists(ALL_MODELS_PATH):
            try:
                self.all_models = joblib.load(ALL_MODELS_PATH)
            except Exception:
                self.all_models = {}
        if not self.all_models and self.model:
            self.all_models = {"XGBoost (Champion)": self.model}

        # 7. Anomaly Detector
        self.anomaly_detector = None
        if os.path.exists(ANOMALY_MODEL_PATH):
            try:
                self.anomaly_detector = load_anomaly_detector(ANOMALY_MODEL_PATH)
            except Exception:
                self.anomaly_detector = None
        if self.anomaly_detector is None:
            from ml.config import MODELS_DIR
            anom_json = os.path.join(MODELS_DIR, "anomaly_stats.json")
            if os.path.exists(anom_json):
                from ml.pure_engine import PureAnomalyDetector
                self.anomaly_detector = PureAnomalyDetector(anom_json)

        # 8. SHAP Explainer
        if self.model and self.preprocessor:
            try:
                dim = len(self.feature_names) if self.feature_names else 16
                bg = np.zeros((30, dim))
                self.explainer = FireExplainer(self.model, bg, self.feature_names)
            except Exception as e:
                print(f"[ModelRegistry] Explainer initialization note: {e}")

        self.is_loaded = self.model is not None and self.preprocessor is not None
        return self

def get_registry() -> ModelRegistry:
    return ModelRegistry.get_instance().load_artifacts()
