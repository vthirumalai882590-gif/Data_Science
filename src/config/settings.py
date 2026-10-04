"""Global configuration, directory paths, and Indian forest geographical coordinates."""
from pathlib import Path
from typing import Dict, Any

# Root Paths
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
DATA_DIR: Path = BASE_DIR / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
MODELS_DIR: Path = BASE_DIR / "models"
REPORTS_DIR: Path = BASE_DIR / "reports"

# Project Constants
RANDOM_STATE: int = 42
TEST_SIZE: float = 0.20

# Weather API Configuration
OPEN_METEO_API_URL: str = "https://api.open-meteo.com/v1/forecast"
WEATHER_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "wind_speed_10m",
    "precipitation",
]

# Preset Indian Forests with Precise Coordinates
INDIAN_FORESTS: Dict[str, Dict[str, Any]] = {
    "Bandipur National Park": {
        "state": "Karnataka",
        "region": "Western Ghats / Deccan",
        "latitude": 11.6667,
        "longitude": 76.6333,
        "forest_type": "Dry Deciduous / Teak",
        "vulnerability": "High in summer (Feb-May)",
    },
    "Jim Corbett National Park": {
        "state": "Uttarakhand",
        "region": "Himalayan Foothills / Terai",
        "latitude": 29.5300,
        "longitude": 78.7747,
        "forest_type": "Moist Deciduous / Sal",
        "vulnerability": "Moderate to High in dry spring",
    },
    "Simlipal National Park": {
        "state": "Odisha",
        "region": "Eastern Highlands",
        "latitude": 21.6833,
        "longitude": 86.3500,
        "forest_type": "Dense Sal / Moist Deciduous",
        "vulnerability": "High (frequent March wildfires)",
    },
    "Kanha Tiger Reserve": {
        "state": "Madhya Pradesh",
        "region": "Central Highlands",
        "latitude": 22.3345,
        "longitude": 80.6115,
        "forest_type": "Sal and Bamboo",
        "vulnerability": "Moderate to High in summer",
    },
    "Gir National Park": {
        "state": "Gujarat",
        "region": "Kathiawar Peninsula",
        "latitude": 21.1243,
        "longitude": 70.8242,
        "forest_type": "Dry Deciduous Scrub & Teak",
        "vulnerability": "High in arid months",
    },
    "Wayanad Wildlife Sanctuary": {
        "state": "Kerala",
        "region": "Western Ghats",
        "latitude": 11.6854,
        "longitude": 76.3693,
        "forest_type": "Semi-Evergreen / Moist Deciduous",
        "vulnerability": "Moderate (summer dry spells)",
    },
    "Kaziranga National Park": {
        "state": "Assam",
        "region": "Brahmaputra Floodplains",
        "latitude": 26.5775,
        "longitude": 93.1711,
        "forest_type": "Tropical Moist / Grasslands",
        "vulnerability": "Low to Moderate",
    },
    "Ranthambore National Park": {
        "state": "Rajasthan",
        "region": "Aravalli & Vindhya Junction",
        "latitude": 26.0173,
        "longitude": 76.5026,
        "forest_type": "Tropical Dry Deciduous / Dhok",
        "vulnerability": "High in summer",
    },
}
