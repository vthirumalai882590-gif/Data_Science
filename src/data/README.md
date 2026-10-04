# `src/data/`: Data Ingestion & Preprocessing Pipelines

This package handles the acquisition, reading, schema sanitization, and train/test splitting of raw data.

## Subagent Responsibilities in `src/data/`
- **Data Ingestion Script (`loader.py`):**
  - Download or load target datasets from local/remote sources.
  - Cache downloaded files into `data/raw/` to prevent redundant network requests.
- **Cleaning & Validation (`cleaner.py`):**
  - Standardize column names (lowercase, strip whitespace, replace spaces with underscores).
  - Convert numeric columns with dirty strings (e.g. `'14.6 9'` or missing values) to proper float types.
  - Verify negative controls: Confirm that non-fire records (`Classes == 'not fire'` or `area == 0`) are present and not stripped away.
- **Train/Test Splitting (`splitter.py`):**
  - Perform stratified or temporal train-test splits using `RANDOM_STATE = 42`.
  - Save processed splits to `data/processed/`.
