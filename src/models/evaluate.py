"""Model evaluation, benchmarking, and metric reporting suite for Forest Fire Predictor.

Provides specialized evaluation functions for:
1. Binary Hazard / Ignition Risk Classification (Quebec Wildfire dataset):
   - Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrix.
2. Continuous Severity / Fire Weather Index Regression (Algerian Forest Fires dataset):
   - R² Score, Root Mean Squared Error (RMSE), and Mean Absolute Error (MAE).
3. Benchmark table formatting and diagnostic reporting for comparing Ridge (L2),
   Random Forest, and XGBoost models.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
    roc_auc_score,
)

logger = logging.getLogger(__name__)


def evaluate_regression(
    y_true: Union[np.ndarray, pd.Series, List[float]],
    y_pred: Union[np.ndarray, pd.Series, List[float]],
    prefix: str = "",
) -> Dict[str, float]:
    """Calculate standard regression metrics: R² Score, RMSE, and MAE.

    Args:
        y_true: Ground-truth target values.
        y_pred: Predicted target values from model pipeline.
        prefix: Optional prefix for metric dictionary keys.

    Returns:
        Dictionary containing rounded 'r2', 'rmse', and 'mae' metrics.
    """
    y_true_arr = np.asarray(y_true, dtype=np.float64)
    y_pred_arr = np.asarray(y_pred, dtype=np.float64)

    r2 = float(r2_score(y_true_arr, y_pred_arr))
    mse = float(mean_squared_error(y_true_arr, y_pred_arr))
    rmse = float(np.sqrt(mse))
    mae = float(mean_absolute_error(y_true_arr, y_pred_arr))

    p = f"{prefix}_" if prefix else ""
    return {
        f"{p}r2": round(r2, 4),
        f"{p}r2_score": round(r2, 4),
        f"{p}rmse": round(rmse, 4),
        f"{p}mae": round(mae, 4),
    }


def evaluate_classification(
    y_true: Union[np.ndarray, pd.Series, List[int]],
    y_pred: Union[np.ndarray, pd.Series, List[int]],
    y_prob: Optional[Union[np.ndarray, pd.Series, List[float]]] = None,
    prefix: str = "",
) -> Dict[str, float]:
    """Calculate standard binary classification metrics: Accuracy, Precision, Recall, F1, and ROC-AUC.

    Args:
        y_true: Ground-truth binary labels (0 or 1).
        y_pred: Predicted class labels (0 or 1).
        y_prob: Optional predicted positive class probabilities P(Y=1) for ROC-AUC.
        prefix: Optional prefix for metric dictionary keys.

    Returns:
        Dictionary containing rounded classification performance metrics.
    """
    y_true_arr = np.asarray(y_true, dtype=np.int32)
    y_pred_arr = np.asarray(y_pred, dtype=np.int32)

    acc = float(accuracy_score(y_true_arr, y_pred_arr))
    prec = float(precision_score(y_true_arr, y_pred_arr, zero_division=0))
    rec = float(recall_score(y_true_arr, y_pred_arr, zero_division=0))
    f1 = float(f1_score(y_true_arr, y_pred_arr, zero_division=0))

    roc_auc: Optional[float] = None
    if y_prob is not None:
        try:
            y_prob_arr = np.asarray(y_prob, dtype=np.float64)
            # If 2D probability matrix was passed (n_samples, 2), extract positive column
            if y_prob_arr.ndim == 2 and y_prob_arr.shape[1] == 2:
                y_prob_arr = y_prob_arr[:, 1]
            roc_auc = float(roc_auc_score(y_true_arr, y_prob_arr))
        except Exception as exc:
            logger.warning("Could not calculate ROC-AUC score: %s", exc)
            roc_auc = None

    p = f"{prefix}_" if prefix else ""
    metrics: Dict[str, float] = {
        f"{p}accuracy": round(acc, 4),
        f"{p}precision": round(prec, 4),
        f"{p}recall": round(rec, 4),
        f"{p}f1": round(f1, 4),
        f"{p}f1_score": round(f1, 4),
    }
    if roc_auc is not None:
        metrics[f"{p}roc_auc"] = round(roc_auc, 4)

    return metrics


def get_confusion_matrix_summary(
    y_true: Union[np.ndarray, pd.Series, List[int]],
    y_pred: Union[np.ndarray, pd.Series, List[int]],
) -> Dict[str, int]:
    """Extract True Negatives, False Positives, False Negatives, and True Positives."""
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = [int(v) for v in cm.ravel()]
    return {
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "true_positives": tp,
    }


def format_benchmark_table(
    headers: List[str],
    rows: List[List[Any]],
    title: str = "",
) -> str:
    """Format a clean markdown/ASCII comparison table for CLI output and logging."""
    str_rows = [[str(cell) for cell in row] for row in rows]
    col_widths = [len(h) for h in headers]
    for row in str_rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(cell))

    sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    header_str = "|" + "|".join(f" {h:<{col_widths[i]}} " for i, h in enumerate(headers)) + "|"

    body_lines = []
    for row in str_rows:
        line = "|" + "|".join(f" {cell:<{col_widths[i]}} " for i, cell in enumerate(row)) + "|"
        body_lines.append(line)

    output = []
    if title:
        banner_len = max(len(sep), len(title) + 4)
        output.append("=" * banner_len)
        output.append(f"  {title}")
        output.append("=" * banner_len)

    output.append(sep)
    output.append(header_str)
    output.append(sep)
    output.extend(body_lines)
    output.append(sep)

    return "\n".join(output)


def print_classification_benchmark(
    results: Dict[str, Dict[str, float]],
    title: Optional[str] = None,
    dataset_name: Optional[str] = None,
) -> str:
    """Format and print comparative benchmark table for classification models."""
    header_title = title or dataset_name or "Quebec Wildfire Ignition Risk (Binary Classification)"
    headers = ["Model", "Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    rows = []
    for model_name, m in results.items():
        rows.append([
            model_name,
            f"{m.get('accuracy', 0.0):.4f}",
            f"{m.get('precision', 0.0):.4f}",
            f"{m.get('recall', 0.0):.4f}",
            f"{m.get('f1_score', m.get('f1', 0.0)):.4f}",
            f"{m.get('roc_auc', 0.0):.4f}",
        ])
    table = format_benchmark_table(headers, rows, title=header_title)
    print("\n" + table)
    return table


def print_regression_benchmark(
    results: Dict[str, Dict[str, float]],
    title: Optional[str] = None,
    dataset_name: Optional[str] = None,
) -> str:
    """Format and print comparative benchmark table for regression models."""
    header_title = title or dataset_name or "Algerian Forest Fires Severity / FWI (Regression)"
    headers = ["Model", "R² Score", "RMSE", "MAE"]
    rows = []
    for model_name, m in results.items():
        rows.append([
            model_name,
            f"{m.get('r2_score', m.get('r2', 0.0)):.4f}",
            f"{m.get('rmse', 0.0):.4f}",
            f"{m.get('mae', 0.0):.4f}",
        ])
    table = format_benchmark_table(headers, rows, title=header_title)
    print("\n" + table)
    return table


def compare_and_select_best_model(
    metrics_dict: Dict[str, Dict[str, float]],
    criterion: str = "roc_auc",
    higher_is_better: bool = True,
) -> Tuple[str, Dict[str, float]]:
    """Identify the top performing model based on a chosen evaluation metric."""
    if not metrics_dict:
        raise ValueError("metrics_dict cannot be empty")

    best_name = ""
    best_score = -float("inf") if higher_is_better else float("inf")

    for name, m in metrics_dict.items():
        score = m.get(criterion)
        if score is None:
            # Fallback criteria
            if criterion == "roc_auc":
                score = m.get("f1_score", m.get("accuracy", 0.0))
            elif criterion == "r2":
                score = m.get("r2_score", 0.0)

        if score is not None:
            if higher_is_better and score > best_score:
                best_score = score
                best_name = name
            elif not higher_is_better and score < best_score:
                best_score = score
                best_name = name

    if not best_name:
        best_name = next(iter(metrics_dict.keys()))

    return best_name, metrics_dict[best_name]
