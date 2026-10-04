# `models/`: Model Registry & Serialized Pipelines

This directory stores trained model pipelines, encoders, and evaluation benchmarks.

## Expected Artifacts
- `best_model.joblib`: Complete end-to-end trained pipeline (preprocessor + estimator).
- `ridge_model.joblib`: Fitted Ridge L2 regression model.
- `rf_model.joblib`: Fitted Random Forest regressor/classifier.
- `xgb_model.joblib`: Fitted XGBoost regressor/classifier.
- `model_metrics.json`: Comparative performance metrics ($R^2$, RMSE, MAE, execution times).

## Subagent Responsibilities in `models/`
- All saved models must be complete pipelines that take raw unscaled inputs and handle preprocessing internally.
- Do not commit large multi-gigabyte models without user approval.
- Maintain `model_metrics.json` with up-to-date validation scores for each saved checkpoint.
