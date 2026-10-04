"""Scikit-learn compatible bounded pipeline wrapper and in-pipeline feature transformers."""

from __future__ import annotations

from typing import List, Optional, Union
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

BASE_FEATURE_NAMES: List[str] = [
    "temperature",
    "relative_humidity",
    "wind_speed",
    "rain",
]

INTERACTION_FEATURE_NAMES: List[str] = [
    "vapor_pressure_deficit",
    "heat_aridity_index",
    "wind_spread_factor",
    "rain_suppression",
]

ALL_FEATURE_NAMES: List[str] = BASE_FEATURE_NAMES + INTERACTION_FEATURE_NAMES


def compute_fire_weather_features(X: Union[pd.DataFrame, np.ndarray]) -> np.ndarray:
    """Compute 4 physical fire weather interaction features and concatenate with 4 base features.

    Calculates:
      1. vapor_pressure_deficit: temperature * (1.0 - relative_humidity / 100.0)
      2. heat_aridity_index: temperature / (relative_humidity + 1.0)
      3. wind_spread_factor: wind_speed * (temperature / (relative_humidity + 1.0))
      4. rain_suppression: exp(-1.5 * rain)

    Returns:
      np.ndarray of shape (N, 8) with all 8 features.
    """
    if isinstance(X, pd.DataFrame):
        if all(col in X.columns for col in BASE_FEATURE_NAMES):
            t = X["temperature"].to_numpy(dtype=np.float64)
            rh = X["relative_humidity"].to_numpy(dtype=np.float64)
            w = X["wind_speed"].to_numpy(dtype=np.float64)
            r = X["rain"].to_numpy(dtype=np.float64)
            base = X[BASE_FEATURE_NAMES].to_numpy(dtype=np.float64)
        elif X.shape[1] == 8:
            return X.to_numpy(dtype=np.float64)
        else:
            arr = X.to_numpy(dtype=np.float64)
            t = arr[:, 0]
            rh = arr[:, 1]
            w = arr[:, 2]
            r = arr[:, 3]
            base = arr[:, :4]
    else:
        arr = np.asarray(X, dtype=np.float64)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        if arr.shape[1] == 8:
            return arr
        t = arr[:, 0]
        rh = arr[:, 1]
        w = arr[:, 2]
        r = arr[:, 3]
        base = arr[:, :4]

    vpd = t * (1.0 - rh / 100.0)
    hai = t / (rh + 1.0)
    wsf = w * (t / (rh + 1.0))
    rs = np.exp(-1.5 * r)

    return np.column_stack([base, vpd, hai, wsf, rs])


class WeatherFeatureEngineer(BaseEstimator, TransformerMixin):
    """Scikit-learn compatible transformer that computes interaction features inside pipelines.

    Computes:
      - vapor_pressure_deficit
      - heat_aridity_index
      - wind_spread_factor
      - rain_suppression
    Expands 4 raw meteorological inputs into an 8-dimensional feature representation.
    """

    def fit(self, X, y=None):
        """Fit transformer (stateless)."""
        return self

    def transform(self, X):
        """Transform raw weather features into 8-dimensional feature matrix."""
        return compute_fire_weather_features(X)

    def get_feature_names_out(self, input_features=None) -> np.ndarray:
        """Return 8-dimensional feature names array."""
        return np.array(ALL_FEATURE_NAMES)


class BoundedRiskPipeline(Pipeline):
    """Scikit-learn compatible Pipeline that strictly bounds .predict() outputs.

    Ensures predictions never violate physical constraints (e.g. [0.0, 100.0] for risk
    scores, or [0.0, inf) for burned area). Preserves full scikit-learn Pipeline
    attributes, named_steps, and seamless joblib serialization across modules.
    """

    def __init__(
        self,
        steps,
        *,
        min_val: Optional[float] = 0.0,
        max_val: Optional[float] = 100.0,
        memory=None,
        verbose: bool = False,
    ):
        super().__init__(steps, memory=memory, verbose=verbose)
        self.min_val = min_val
        self.max_val = max_val

    def predict(self, X, **predict_params):
        """Transform features through pipeline steps, predict raw values, and clamp bounds."""
        raw_pred = super().predict(X, **predict_params)
        lower = self.min_val if self.min_val is not None else -float("inf")
        upper = self.max_val if self.max_val is not None else float("inf")
        return np.clip(raw_pred, lower, upper)
