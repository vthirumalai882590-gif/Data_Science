# Data Directory: Architecture & Responsibilities

This directory contains all data assets for the **Forest Fire Predictor** project.

## Directory Layout
- `raw/`: Stores the original, immutable source datasets exactly as fetched from external repositories (e.g., UCI, NASA FIRMS, Forest Survey). Never modify files directly inside `raw/`.
- `processed/`: Stores cleaned, transformed, and feature-engineered datasets ready for model training.

---

## Subagent Responsibilities in `data/`

If you are a subagent working inside or interacting with this folder:

1. **Negative Controls / Normal Days Verification:**
   - You MUST ensure datasets contain both **fire incidents** and **normal/non-fire days** (negative samples).
   - Datasets with only fire occurrences introduce survivorship bias.
2. **Schema & Integrity Rules:**
   - Relative Humidity ($RH$) must be within $[0, 100]\%$.
   - Rain / Precipitation must be $\ge 0 \text{ mm}$.
   - Temperature must match realistic Celsius ranges (typically $10^\circ\text{C}$ to $55^\circ\text{C}$).
   - Any corrupt non-numeric tokens (e.g. `'14.6 9'`, whitespace padding) must be addressed during parsing.
3. **Data Versioning & Tracking:**
   - Raw data files must be preserved in their initial state.
   - When writing to `processed/`, save as clean CSVs (e.g., `forest_fires_cleaned.csv`) accompanied by a short `.meta.json` summary containing total rows, column datatypes, and class distributions.
