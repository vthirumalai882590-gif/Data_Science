"""
FIREGUARD X - Model Evaluation Engine
Calculates comprehensive performance metrics for classification models:
Accuracy, Precision, Recall, F1-Score, ROC-AUC, Average Precision (PR-AUC),
Confusion Matrix, and generates visual diagnostic plots.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless figure generation
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    roc_curve,
    precision_recall_curve,
)
from ml.config import FIGURES_DIR

def evaluate_classifier(model, X_test, y_test, model_name: str = "Model") -> dict:
    """
    Evaluates a trained classifier on test set and computes standardized metrics.
    """
    y_pred = model.predict(X_test)
    
    # Predict probabilities if supported
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, "decision_function"):
        df_vals = model.decision_function(X_test)
        y_prob = 1.0 / (1.0 + np.exp(-df_vals))
    else:
        y_prob = y_pred.astype(float)

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    
    try:
        roc_auc = float(roc_auc_score(y_test, y_prob))
    except Exception:
        roc_auc = 0.5
        
    try:
        pr_auc = float(average_precision_score(y_test, y_prob))
    except Exception:
        pr_auc = 0.5

    cm = confusion_matrix(y_test, y_pred).tolist()
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()

    # False negative and false positive cost analysis for wildfire safety
    fn_rate = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0
    fp_rate = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0

    return {
        "model_name": model_name,
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "pr_auc": round(pr_auc, 4),
        "confusion_matrix": cm,
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp),
        "false_negative_rate": round(fn_rate, 4),
        "false_positive_rate": round(fp_rate, 4),
        "safety_notes": (
            "In wildfire monitoring, False Negatives (predicting no fire when fire occurs) "
            "carry severe catastrophic risk. Models with high Recall and minimal FN are prioritized."
        )
    }

def generate_evaluation_visualizations(models_dict: dict, X_test, y_test, feature_names: list[str]):
    """
    Generate and save high-resolution diagnostic plots to reports/figures/.
    """
    os.makedirs(FIGURES_DIR, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. ROC Curves Comparison
    plt.figure(figsize=(8, 6), dpi=150)
    plt.plot([0, 1], [0, 1], "k--", label="Random Chance (AUC = 0.50)", alpha=0.6)
    
    for name, model in models_dict.items():
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, probs)
            auc_val = roc_auc_score(y_test, probs)
            plt.plot(fpr, tpr, label=f"{name} (AUC = {auc_val:.3f})", lw=2)

    plt.title("ROC Curves - Wildfire Risk Model Benchmark", fontsize=13, fontweight="bold", pad=12)
    plt.xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
    plt.ylabel("True Positive Rate (Recall / Sensitivity)", fontsize=11)
    plt.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "roc_curves.png"))
    plt.close()

    # 2. Confusion Matrices Subplot
    num_models = len(models_dict)
    fig, axes = plt.subplots(1, num_models, figsize=(4 * num_models, 3.8), dpi=150)
    if num_models == 1:
        axes = [axes]

    for ax, (name, model) in zip(axes, models_dict.items()):
        preds = model.predict(X_test)
        cm = confusion_matrix(y_test, preds)
        sns.heatmap(
            cm, annot=True, fmt="d", cmap="YlOrRd", cbar=False, ax=ax,
            xticklabels=["No Fire", "Fire"], yticklabels=["No Fire", "Fire"]
        )
        ax.set_title(name, fontsize=11, fontweight="bold")
        ax.set_xlabel("Predicted Label")
        ax.set_ylabel("True Label")

    plt.suptitle("Confusion Matrices Across Models", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, "confusion_matrices.png"))
    plt.close()

    # 3. Feature Importance (Tree or Ensemble model)
    best_tree = None
    for name in ["Random Forest", "XGBoost", "Decision Tree"]:
        if name in models_dict and hasattr(models_dict[name], "feature_importances_"):
            best_tree = (name, models_dict[name])
            break

    if best_tree:
        name, model = best_tree
        importances = model.feature_importances_
        sorted_idx = np.argsort(importances)
        
        plt.figure(figsize=(9, 6), dpi=150)
        plt.barh(np.array(feature_names)[sorted_idx], importances[sorted_idx], color="#1b4332")
        plt.title(f"Feature Importance ({name})", fontsize=13, fontweight="bold", pad=12)
        plt.xlabel("Normalized Gini Importance", fontsize=11)
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, "feature_importance.png"))
        plt.close()
