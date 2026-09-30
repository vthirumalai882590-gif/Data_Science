"""
FIREGUARD X - Dataset Acquisition and Preparation Script
Source: UCI Machine Learning Repository (Algerian Forest Fires Dataset)
URL: https://archive.ics.uci.edu/ml/machine-learning-databases/00547/Algerian_forest_fires_dataset_UPDATE.csv

Downloads the authentic historical forest fires dataset, parses the two distinct regions
(Bejaia Region and Sidi Bel-abbes Region), cleans whitespace anomalies and subheader markers,
and persists the raw and normalized data in data/raw/forest_fires.csv.
"""

import os
import sys
import urllib.request
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
RAW_FILE = os.path.join(RAW_DIR, "forest_fires.csv")
UCI_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00547/Algerian_forest_fires_dataset_UPDATE.csv"

def acquire_dataset():
    os.makedirs(RAW_DIR, exist_ok=True)
    raw_content = None

    print("[FIREGUARD X] Downloading authentic Algerian Forest Fires dataset from UCI ML Repository...")
    try:
        req = urllib.request.Request(UCI_URL, headers={"User-Agent": "FIREGUARD-X-Platform/1.0"})
        with urllib.request.urlopen(req, timeout=10) as response:
            raw_content = response.read().decode("latin1")
        print(f"[FIREGUARD X] Successfully retrieved {len(raw_content)} bytes from UCI.")
    except Exception as exc:
        print(f"[FIREGUARD X] UCI download encountered: {exc}. Checking local cache...")
        if os.path.exists(RAW_FILE):
            print(f"[FIREGUARD X] Existing raw dataset found at {RAW_FILE}")
            return

    if not raw_content:
        raise RuntimeError("Failed to acquire dataset from UCI and no local file found.")

    lines = [line.strip() for line in raw_content.splitlines() if line.strip()]
    
    records = []
    current_region = 0  # 0: Bejaia Region, 1: Sidi Bel-abbes Region
    header = None

    for line in lines:
        if "Bejaia" in line:
            current_region = 0
            continue
        elif "Sidi Bel-abbes" in line:
            current_region = 1
            continue
        
        parts = [p.strip() for p in line.split(",")]
        
        if parts[0] == "day":
            if header is None:
                header = [p.replace(" ", "") for p in parts]
            continue
        
        if len(parts) >= 14:
            row_dict = {}
            for col_idx, col_name in enumerate(header[:len(parts)]):
                row_dict[col_name] = parts[col_idx]
            row_dict["Region"] = current_region
            records.append(row_dict)

    df = pd.DataFrame(records)
    print(f"[FIREGUARD X] Parsed {len(df)} records across 2 regions.")

    # Save initial raw parsed file
    df.to_csv(RAW_FILE, index=False)
    print(f"[FIREGUARD X] Saved authentic dataset to {RAW_FILE}")
    print(f"[FIREGUARD X] Columns: {list(df.columns)}")
    print(f"[FIREGUARD X] Sample row:\n{df.iloc[0].to_dict()}")

if __name__ == "__main__":
    acquire_dataset()
