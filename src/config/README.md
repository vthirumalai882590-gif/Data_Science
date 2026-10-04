# `src/config/`: Configuration & Presets

This directory manages global variables, project filesystem paths, API endpoints, model hyperparameter bounds, and geographical coordinates for Indian forests.

## Subagent Responsibilities in `src/config/`
- **Single Source of Truth:** All file paths, random seeds (`RANDOM_STATE = 42`), and thresholds must be defined here.
- **Indian Forest Preset Catalog:** Maintain accurate latitude, longitude, region, and state for key forest reserves across India:
  - Jim Corbett National Park (Uttarakhand)
  - Bandipur National Park (Karnataka)
  - Simlipal National Park (Odisha)
  - Kaziranga National Park (Assam)
  - Gir National Park (Gujarat)
  - Kanha National Park (Madhya Pradesh)
  - Wayanad Wildlife Sanctuary (Kerala)
  - Sariska / Ranthambore (Rajasthan)
  - Sundarbans Mangrove Forest (West Bengal)
- **API Configuration:** Base URL and parameters for Open-Meteo (`https://api.open-meteo.com/v1/forecast`).
