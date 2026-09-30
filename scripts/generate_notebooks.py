"""
FIREGUARD X - Jupyter Notebooks Generator
Generates reproducible academic notebooks for all 7 phases of the Data Science lifecycle:
  01_data_loading.ipynb
  02_data_cleaning.ipynb
  03_eda.ipynb
  04_feature_engineering.ipynb
  05_model_training.ipynb
  06_model_evaluation.ipynb
  07_explainable_ai.ipynb
"""

import os
import json

NOTEBOOKS_DIR = os.path.join(os.path.dirname(__file__), "..", "notebooks")
os.makedirs(NOTEBOOKS_DIR, exist_ok=True)

def create_notebook(cells):
    return {
        "cells": cells,
        "metadata": {
            "language_info": {"name": "python", "version": "3.11"},
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

def md_cell(source):
    return {"cell_type": "markdown", "metadata": {}, "source": [line + "\n" for line in source.strip().split("\n")]}

def code_cell(source):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": [line + "\n" for line in source.strip().split("\n")]}

def build_all_notebooks():
    # 01_data_loading.ipynb
    nb1 = create_notebook([
        md_cell("# FIREGUARD X - Phase 1: Data Acquisition & Inspection\n\nThis notebook demonstrates programmatic dataset acquisition, schema verification, data types, and initial data exploration from the UCI Algerian Forest Fires dataset."),
        code_cell("""import pandas as pd
import numpy as np

# Load raw dataset
df = pd.read_csv('../data/raw/forest_fires.csv')
print(f"Dataset Shape: {df.shape}")
df.head()"""),
        code_cell("""# Inspect attributes and non-null counts
df.info()"""),
        code_cell("""# Summary statistics of raw meteorological readings
df.describe()""")
    ])
    with open(os.path.join(NOTEBOOKS_DIR, "01_data_loading.ipynb"), "w") as f:
        json.dump(nb1, f, indent=2)

    # 02_data_cleaning.ipynb
    nb2 = create_notebook([
        md_cell("# FIREGUARD X - Phase 2: Data Cleaning & Preprocessing Pipeline\n\nHandles whitespace trimming, numeric type coercion, missing value checks, and target classification mapping ('fire'=1, 'not fire'=0)."),
        code_cell("""from ml.preprocessing import clean_raw_dataset
cleaned_df = clean_raw_dataset('../data/raw/forest_fires.csv')
print(f"Cleaned dataset shape: {cleaned_df.shape}")
print(cleaned_df['target'].value_counts())
cleaned_df.head()""")
    ])
    with open(os.path.join(NOTEBOOKS_DIR, "02_data_cleaning.ipynb"), "w") as f:
        json.dump(nb2, f, indent=2)

    # 03_eda.ipynb
    nb3 = create_notebook([
        md_cell("# FIREGUARD X - Phase 3: Exploratory Data Analysis (EDA)\n\nConducts univariate, bivariate, and correlation analyses examining temperature, relative humidity, wind speed, rainfall, and Fire Weather Index against fire occurrence."),
        code_cell("""import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/interim/cleaned_fires.csv')
sns.set_theme(style='whitegrid')

# Temperature vs Fire Occurrence
plt.figure(figsize=(8, 4))
sns.boxplot(x='target', y='Temperature', data=df, palette=['#16a34a', '#dc2626'])
plt.title('Temperature Distribution by Fire Occurrence (0: Safe, 1: Fire)')
plt.show()"""),
        code_cell("""# Correlation Matrix Heatmap
plt.figure(figsize=(10, 8))
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
sns.heatmap(df[numeric_cols].corr(), annot=False, cmap='coolwarm', center=0)
plt.title('Feature Correlation Matrix')
plt.show()""")
    ])
    with open(os.path.join(NOTEBOOKS_DIR, "03_eda.ipynb"), "w") as f:
        json.dump(nb3, f, indent=2)

    # 04_feature_engineering.ipynb
    nb4 = create_notebook([
        md_cell("# FIREGUARD X - Phase 4: Feature Engineering\n\nDerives domain-grounded fire-weather interactions: `temp_rh_ratio`, `dryness_index`, `wind_temp_interaction`, `rain_deficit`, and `ffmc_isi_ratio`."),
        code_cell("""from ml.feature_engineering import compute_engineered_features
import pandas as pd

df = pd.read_csv('../data/interim/cleaned_fires.csv')
featured_df = compute_engineered_features(df)
featured_df[['Temperature', 'RH', 'temp_rh_ratio', 'dryness_index', 'wind_temp_interaction', 'rain_deficit']].head()""")
    ])
    with open(os.path.join(NOTEBOOKS_DIR, "04_feature_engineering.ipynb"), "w") as f:
        json.dump(nb4, f, indent=2)

    # 05_model_training.ipynb
    nb5 = create_notebook([
        md_cell("# FIREGUARD X - Phase 5: Multi-Model Machine Learning Training\n\nTrains Logistic Regression, Decision Tree, Random Forest, and XGBoost on stratified partitions with hyperparameter control."),
        code_cell("""from ml.train import train_and_evaluate_all
results = train_and_evaluate_all()
print(f"Selected Champion Model: {results['selected_model']}")""")
    ])
    with open(os.path.join(NOTEBOOKS_DIR, "05_model_training.ipynb"), "w") as f:
        json.dump(nb5, f, indent=2)

    # 06_model_evaluation.ipynb
    nb6 = create_notebook([
        md_cell("# FIREGUARD X - Phase 6: Model Evaluation & Benchmark Comparison\n\nAnalyzes Accuracy, Precision, Recall, F1, ROC-AUC, Confusion Matrix, and safety trade-offs (False Negatives vs False Positives)."),
        code_cell("""import json
with open('../models/metrics.json') as f:
    metrics = json.load(f)

print(json.dumps(metrics['models'], indent=2))""")
    ])
    with open(os.path.join(NOTEBOOKS_DIR, "06_model_evaluation.ipynb"), "w") as f:
        json.dump(nb6, f, indent=2)

    # 07_explainable_ai.ipynb
    nb7 = create_notebook([
        md_cell("# FIREGUARD X - Phase 7: Explainable AI with SHAP\n\nComputes Shapley additive explanations (SHAP) for local and global feature attribution."),
        code_cell("""from ml.model_registry import get_registry
from ml.services import *
import pandas as pd

registry = get_registry()
print(f"Loaded Model: {registry.metadata.get('model_name')}")
sample_input = {'Temperature': 36.0, 'RH': 28.0, 'Ws': 18.0, 'Rain': 0.0, 'Region': 0}
# Preprocessing and SHAP inference test
df = pd.DataFrame([sample_input])
X_scaled = registry.preprocessor.transform(df)
expl = registry.explainer.explain_instance(X_scaled[0], sample_input)
print('Top Drivers:')
for d in expl['top_drivers']:
    print(f" - {d['label']}: {d['contribution']:+.4f} ({d['direction']})")
print('Narrative:', expl['narrative'])""")
    ])
    with open(os.path.join(NOTEBOOKS_DIR, "07_explainable_ai.ipynb"), "w") as f:
        json.dump(nb7, f, indent=2)

    print("[FIREGUARD X] Generated all 7 academic Jupyter notebooks.")

if __name__ == "__main__":
    build_all_notebooks()
