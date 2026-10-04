# `tests/`: Automated Verification & QA

This directory houses unit and integration tests executed with `pytest`.

## Test Suites
- `test_data.py`:
  - Verifies raw dataset loading, checks for missing values, and ensures negative non-fire samples are present.
- `test_models.py`:
  - Validates that Ridge, Random Forest, and XGBoost models produce bounded predictions given valid inputs.
- `test_api.py`:
  - Tests Open-Meteo API response schema, lat/long inputs, and error-handling on connection dropouts.

## Subagent Responsibilities in `tests/`
- Run `pytest` before marking any milestone as complete.
- Keep tests fast and deterministic (use mocks for network calls if testing offline).
