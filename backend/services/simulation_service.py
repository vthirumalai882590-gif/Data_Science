"""
FIREGUARD X - Educational Fire Spread Simulation Service
Implements a 2D cellular automaton model simulating wildfire propagation
governed by wind vectors, ambient dryness, and localized fuel state transitions.
"""

import numpy as np

# Wind direction vector map (row_delta, col_delta)
WIND_VECTORS = {
    "N": (-1, 0),
    "NE": (-1, 1),
    "E": (0, 1),
    "SE": (1, 1),
    "S": (1, 0),
    "SW": (1, -1),
    "W": (0, -1),
    "NW": (-1, -1),
}

# State definitions
STATE_SAFE = "SAFE"
STATE_AT_RISK = "AT_RISK"
STATE_SIMULATED_FIRE = "SIMULATED_FIRE"
STATE_AFFECTED = "AFFECTED"

def run_fire_spread_simulation(
    start_zone: str = "zone-bej-01",
    wind_speed: float = 20.0,
    wind_direction: str = "NE",
    dryness: float = 75.0,
    duration_hours: int = 24,
    grid_size: int = 9,
) -> dict:
    """
    Simulates discrete time-step wildfire progression across a cellular landscape.
    Time steps: T+0, T+6, T+12, T+18, T+24 (up to duration_hours).
    """
    wind_dir = wind_direction.upper()
    if wind_dir not in WIND_VECTORS:
        wind_dir = "NE"

    w_row, w_col = WIND_VECTORS[wind_dir]

    # Initialize grid: SAFE = 0, AT_RISK = 1, SIMULATED_FIRE = 2, AFFECTED = 3
    # Start ignition near center
    center_row = grid_size // 2
    center_col = grid_size // 2

    grid = np.zeros((grid_size, grid_size), dtype=int)
    grid[center_row, center_col] = 2  # Ignition point: SIMULATED_FIRE

    # Base propagation probability influenced by wind and dryness
    base_spread_prob = float(np.clip((dryness / 100.0) * 0.45 + (wind_speed / 100.0) * 0.35, 0.15, 0.90))

    # Time steps to simulate
    steps_hours = [0, 6, 12, 18, 24]
    if duration_hours > 24:
        steps_hours = [0, 6, 12, 24, 48, 72][:6]

    recorded_steps = []

    def format_step_cells(current_grid, hours_elapsed):
        cells = []
        active_fire = 0
        affected = 0
        at_risk = 0

        for r in range(grid_size):
            for c in range(grid_size):
                val = current_grid[r, c]
                if val == 0:
                    state = STATE_SAFE
                    intensity = 0.0
                elif val == 1:
                    state = STATE_AT_RISK
                    intensity = 0.4
                    at_risk += 1
                elif val == 2:
                    state = STATE_SIMULATED_FIRE
                    intensity = 1.0
                    active_fire += 1
                else:
                    state = STATE_AFFECTED
                    intensity = 0.7
                    affected += 1

                cells.append({
                    "row": r,
                    "col": c,
                    "state": state,
                    "intensity": intensity
                })

        return {
            "time_label": f"T+{hours_elapsed}h",
            "hours": hours_elapsed,
            "cells": cells,
            "active_fire_count": active_fire,
            "affected_count": affected,
            "at_risk_count": at_risk
        }

    # Record T+0
    # Mark downwind neighbors as AT_RISK
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = center_row + dr, center_col + dc
            if 0 <= nr < grid_size and 0 <= nc < grid_size and grid[nr, nc] == 0:
                grid[nr, nc] = 1

    recorded_steps.append(format_step_cells(grid, 0))

    # Simulate subsequent time steps
    rng = np.random.RandomState(42)  # Deterministic seed for reproducible simulation

    current_grid = grid.copy()

    for idx, hrs in enumerate(steps_hours[1:], start=1):
        next_grid = current_grid.copy()
        
        # 1. Existing fires transition to AFFECTED (burned) after some steps
        for r in range(grid_size):
            for c in range(grid_size):
                if current_grid[r, c] == 2:
                    # Fire has burned fuel in this cell
                    next_grid[r, c] = 3

        # 2. Spread from previously active fire cells to neighbors
        for r in range(grid_size):
            for c in range(grid_size):
                if current_grid[r, c] == 2:
                    # Check 8-neighborhood
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < grid_size and 0 <= nc < grid_size:
                                if current_grid[nr, nc] in (0, 1):
                                    # Calculate wind alignment
                                    # Dot product of spread direction and wind vector
                                    alignment = (dr * w_row + dc * w_col)
                                    spread_chance = base_spread_prob
                                    if alignment > 0:
                                        spread_chance = min(0.95, spread_chance * 1.5)
                                    elif alignment < 0:
                                        spread_chance = max(0.05, spread_chance * 0.4)

                                    if rng.rand() < spread_chance:
                                        next_grid[nr, nc] = 2  # Becomes SIMULATED_FIRE
                                    else:
                                        next_grid[nr, nc] = 1  # Remains/Becomes AT_RISK

        current_grid = next_grid
        recorded_steps.append(format_step_cells(current_grid, hrs))

    return {
        "start_zone": start_zone,
        "wind_speed": wind_speed,
        "wind_direction": wind_dir,
        "dryness": dryness,
        "duration_hours": duration_hours,
        "grid_dimension": grid_size,
        "steps": recorded_steps,
        "disclaimer": "This is a simplified educational simulation and should not be used for real-world emergency response."
    }
