# `src/`: Modular Source Code Architecture

All production and pipeline code lives within this package. Scripts here are organized cleanly by responsibility to ensure modularity, maintainability, and testability.

## Subpackage Layout
- [`src/config/`](file:///Users/sreekanth/Desktop/DataScience/src/config/README.md): Central configurations, Indian forest coordinates, paths, model parameters.
- [`src/data/`](file:///Users/sreekanth/Desktop/DataScience/src/data/README.md): Automated data fetching, ingestion, cleaning, and train/test splits.
- [`src/features/`](file:///Users/sreekanth/Desktop/DataScience/src/features/README.md): Preprocessing transformers, scaling, and feature engineering.
- [`src/models/`](file:///Users/sreekanth/Desktop/DataScience/src/models/README.md): Model definition, training loops, evaluation metrics, and hyperparameter tuning.
- [`src/api/`](file:///Users/sreekanth/Desktop/DataScience/src/api/README.md): External integration with Open-Meteo for live Indian forest weather & 24h forecasts.
- [`src/utils/`](file:///Users/sreekanth/Desktop/DataScience/src/utils/README.md): General utilities (logging, artifact serialization, formatting).

## General Engineering Guidelines for Subagents
- Never hardcode file paths; import paths from `src.config.settings`.
- Ensure functions have explicit type annotations and docstrings.
- Code must run without circular dependencies.
