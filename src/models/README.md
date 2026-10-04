# `src/models/`: Machine Learning Training, Evaluation & Tuning

This package contains the core ML modeling implementations, comparing regularized linear regression (Ridge L2), Random Forest, and XGBoost.

## Subagent Responsibilities in `src/models/`
- **Model Implementations (`train.py`):**
  - **Ridge Regression (L2 Regularization):** Baseline regularized linear model. Analyze coefficients ($\beta_j$) to explain directional impact.
  - **Random Forest Regressor/Classifier:** Tree ensemble with bagging; compute Gini / MDI feature importances.
  - **XGBoost Regressor/Classifier:** Gradient boosted decision trees; tune `n_estimators`, `max_depth`, `learning_rate`.
- **Evaluation & Benchmarking (`evaluate.py`):**
  - Compute $R^2$ Score, Mean Absolute Error (MAE), and Root Mean Squared Error (RMSE) for regression tasks.
  - Compute Accuracy, Precision, Recall, F1-Score, and ROC-AUC for classification/probability tasks.
  - Produce benchmark comparison tables across Ridge, Random Forest, and XGBoost.
- **Model Persistence:**
  - Export best-performing pipeline(s) to `models/` using `joblib`.
  - Save evaluation summary metrics as JSON for frontend visualization.
