"""
FIREGUARD X - Feature Engineering Pipeline
Constructs domain-grounded environmental and fire-weather features
from raw meteorological and fuel moisture indicators.
"""

import pandas as pd
import numpy as np

def compute_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate derived environmental intelligence features from base meteorological inputs.
    
    Features engineered:
    1. temp_rh_ratio: Ratio of Temperature to Relative Humidity.
       High values indicate critical atmospheric drying conditions.
    2. dryness_index: (100 - RH) * Temperature / 100.0
       Quantifies evapotranspiration pressure on forest canopy and dead fine fuels.
    3. wind_temp_interaction: Ws * Temperature
       Advective convective heat transport and wind-driven oxygen supply.
    4. rain_deficit: 1.0 / (Rain + 0.1)
       Inverse moisture suppression indicator; spikes under prolonged dry spells.
    5. ffmc_isi_ratio: ISI / (FFMC + 1e-4)
       Initial spread index normalized by fuel moisture code.
    """
    df = df.copy()
    
    # Ensure numeric types
    temp = pd.to_numeric(df["Temperature"], errors="coerce")
    rh = pd.to_numeric(df["RH"], errors="coerce")
    ws = pd.to_numeric(df["Ws"], errors="coerce")
    rain = pd.to_numeric(df["Rain"], errors="coerce")
    
    # 1. Temperature-to-Humidity Ratio
    df["temp_rh_ratio"] = np.round(temp / (rh + 1e-4), 4)
    
    # 2. Atmospheric Dryness Index
    df["dryness_index"] = np.round((100.0 - rh) * temp / 100.0, 4)
    
    # 3. Wind-Temperature Interaction
    df["wind_temp_interaction"] = np.round(ws * temp, 4)
    
    # 4. Rain Deficit Indicator
    df["rain_deficit"] = np.round(1.0 / (rain + 0.1), 4)
    
    # 5. FFMC to ISI Spread Dynamic (if FWI components present)
    if "FFMC" in df.columns and "ISI" in df.columns:
        ffmc = pd.to_numeric(df["FFMC"], errors="coerce")
        isi = pd.to_numeric(df["ISI"], errors="coerce")
        df["ffmc_isi_ratio"] = np.round(isi / (ffmc + 1e-4), 4)
    else:
        df["ffmc_isi_ratio"] = 0.0

    return df

FEATURE_DESCRIPTIONS = {
    "Temperature": "Ambient temperature in degrees Celsius (°C). Primary driver of fuel drying and ignition readiness.",
    "RH": "Relative humidity percentage (%). Key moisture buffer suppressing ignition.",
    "Ws": "Wind speed in km/h. Accelerates flame propagation and oxygen delivery.",
    "Rain": "Precipitation in mm. Wetting agent that raises moisture content of living and dead biomass.",
    "FFMC": "Fine Fuel Moisture Code (standard FWI system). Moisture content of surface litter and needles.",
    "DMC": "Duff Moisture Code. Moisture of shallow decomposing organic soil layers.",
    "DC": "Drought Code. Moisture content of deep organic layers and heavy woody fuels.",
    "ISI": "Initial Spread Index. Fire rate-of-spread rating combining wind and surface moisture.",
    "BUI": "Buildup Index. Total fuel quantity available for combustion combining DMC and DC.",
    "FWI": "Fire Weather Index. Overall fire intensity rating combining ISI and BUI.",
    "Region": "Geographic zone identifier (0: Bejaia, 1: Sidi Bel-abbes).",
    "temp_rh_ratio": "Derived: Temperature / Relative Humidity ratio. High values signal rapid fuel desiccation.",
    "dryness_index": "Derived: Atmospheric dryness potential quantifying evapotranspiration pressure.",
    "wind_temp_interaction": "Derived: Convective heat transfer interaction between ambient wind and temperature.",
    "rain_deficit": "Derived: Inverse rainfall metric reflecting cumulative moisture deficit.",
    "ffmc_isi_ratio": "Derived: Flame propagation potential relative to fine fuel moisture."
}
