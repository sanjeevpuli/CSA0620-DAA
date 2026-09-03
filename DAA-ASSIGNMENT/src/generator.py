"""
Deterministic Synthetic Aircraft Dataset Generator.

Course: CSA0620 - Design and Analysis of Algorithms
Module: generator.py
"""

from __future__ import annotations
import random
from typing import List
from src.models import AircraftPoint


def generate_random_aircraft_points(
    n: int,
    seed: int = 42,
    x_min: float = 0.0,
    x_max: float = 1000.0,
    y_min: float = 0.0,
    y_max: float = 1000.0,
    prefix: str = "AC"
) -> List[AircraftPoint]:
    """
    Generates a deterministic synthetic dataset of n aircraft positions.

    Uses a fixed random seed to guarantee reproducibility across benchmark runs
    and automated test suites.

    Args:
        n: Number of aircraft points to generate.
        seed: Random seed for deterministic reproducibility (default: 42).
        x_min: Minimum X coordinate boundary (e.g., km from radar origin).
        x_max: Maximum X coordinate boundary.
        y_min: Minimum Y coordinate boundary.
        y_max: Maximum Y coordinate boundary.
        prefix: Aircraft ID prefix string.

    Returns:
        List of n AircraftPoint objects with unique coordinates and identifiers.
    """
    rng = random.Random(seed)
    points: List[AircraftPoint] = []
    used_coords = set()

    for i in range(1, n + 1):
        while True:
            # Round to 2 decimal places to simulate radar resolution
            x = round(rng.uniform(x_min, x_max), 2)
            y = round(rng.uniform(y_min, y_max), 2)
            if (x, y) not in used_coords:
                used_coords.add((x, y))
                break
        aircraft_id = f"{prefix}-{i:04d}" if n >= 100 else f"{prefix}{i}"
        points.append(AircraftPoint(aircraft_id, x, y))

    return points
