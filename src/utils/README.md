# `src/utils/`: Common Utilities & Helpers

This package provides helper functions for structured logging, metrics reporting, serialization, and risk level binning.

## Subagent Responsibilities in `src/utils/`
- **Logger (`logger.py`):**
  - Standardized logging format with timestamps and clear progress indicators.
- **Risk Categorization (`risk_scorer.py`):**
  - Map continuous regression predictions or probability values into human-readable danger levels:
    - **Low** (Safe, green)
    - **Moderate** (Caution, yellow)
    - **High** (Warning, orange)
    - **Extreme** (Critical danger, red)
- **Serialization Helpers (`serializer.py`):**
  - Safe model dumping and loading with version checks via `joblib`.
