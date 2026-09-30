# FIREGUARD X Data Repository

This directory contains the dataset assets used by FIREGUARD X for forest fire risk prediction and environmental intelligence.

## Structure

- `data/raw/`: Original, unmodified datasets.
  - Primary supported dataset: Algerian Forest Fires Dataset (UCI Machine Learning Repository) or Montesinho Forest Fire Dataset.
  - Default dataset: `data/raw/forest_fires.csv` (Algerian Forest Fires dataset containing real environmental measurements: Temperature, RH, Ws, Rain, FFMC, DMC, DC, ISI, BUI, FWI, and fire/not-fire classification).
- `data/interim/`: Intermediate cleaned data during exploratory analysis and processing.
- `data/processed/`: Scaled and feature-engineered datasets ready for model training and evaluation.
- `data/external/`: External spatial, regional, or reference boundary data.

## Dataset Provenance
- Source: UCI Machine Learning Repository (Algerian Forest Fires Dataset)
- Records: 244 instances from Bejaia and Sidi Bel-abbes regions
- Features: Real meteorological observations and Fire Weather Index (FWI) components.
