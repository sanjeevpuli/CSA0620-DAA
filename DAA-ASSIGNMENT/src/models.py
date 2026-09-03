"""
Data Models and Distance Utilities for Air-Traffic Nearest-Neighbour Detection.

Course: CSA0620 - Design and Analysis of Algorithms
Module: models.py
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass(frozen=True)
class AircraftPoint:
    """
    Represents an aircraft's 2D position in a monitored airspace sector.

    Attributes:
        id: Unique identifier for the aircraft (e.g., 'P1', 'FL-104').
        x: Radar X-coordinate (e.g., kilometers / nautical miles from radar center).
        y: Radar Y-coordinate (e.g., kilometers / nautical miles from radar center).
    """
    id: str
    x: float
    y: float

    def __post_init__(self):
        # Enforce float type for numerical precision
        object.__setattr__(self, "x", float(self.x))
        object.__setattr__(self, "y", float(self.y))

    def as_tuple(self) -> Tuple[float, float]:
        """Returns coordinate pair as (x, y)."""
        return (self.x, self.y)

    def __str__(self) -> str:
        return f"{self.id}({self.x:g}, {self.y:g})"

    def __repr__(self) -> str:
        return f"AircraftPoint(id='{self.id}', x={self.x}, y={self.y})"


def squared_distance(p1: AircraftPoint, p2: AircraftPoint) -> float:
    """
    Computes the squared Euclidean distance between two aircraft points:
        d^2 = (x2 - x1)^2 + (y2 - y1)^2

    Used internally in algorithms to avoid computationally expensive
    square-root operations during distance comparisons.

    Args:
        p1: First aircraft point.
        p2: Second aircraft point.

    Returns:
        Squared distance as a float.
    """
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return dx * dx + dy * dy


def euclidean_distance(p1: AircraftPoint, p2: AircraftPoint) -> float:
    """
    Computes the exact Euclidean distance between two aircraft points:
        d = sqrt((x2 - x1)^2 + (y2 - y1)^2)

    Args:
        p1: First aircraft point.
        p2: Second aircraft point.

    Returns:
        Euclidean distance as a float.
    """
    return math.sqrt(squared_distance(p1, p2))


@dataclass
class ClosestPairResult:
    """
    Standardized result structure representing the closest pair of aircraft found.

    Attributes:
        point1: First aircraft in the closest pair.
        point2: Second aircraft in the closest pair.
        distance: Minimum Euclidean distance between them.
        comparisons_count: Total number of pairwise distance checks evaluated.
        algorithm: Name of the algorithm used ('Brute Force' or 'Divide and Conquer').
    """
    point1: AircraftPoint
    point2: AircraftPoint
    distance: float
    comparisons_count: int = 0
    algorithm: str = "Unknown"

    def __post_init__(self):
        # Guarantee deterministic canonical ordering (point1 precedes point2)
        if self.point1.id > self.point2.id or (
            self.point1.id == self.point2.id
            and (self.point1.x, self.point1.y) > (self.point2.x, self.point2.y)
        ):
            self.point1, self.point2 = self.point2, self.point1

    @property
    def pair_names(self) -> str:
        """Returns standard pair representation, e.g., 'P1-P6'."""
        return f"{self.point1.id}-{self.point2.id}"

    def summary(self) -> str:
        """Returns formatted human-readable summary."""
        return (
            f"Algorithm: {self.algorithm}\n"
            f"Closest Pair: {self.point1.id} {self.point1.as_tuple()} and "
            f"{self.point2.id} {self.point2.as_tuple()}\n"
            f"Euclidean Distance: {self.distance:.6f}\n"
            f"Pairwise Comparisons: {self.comparisons_count}"
        )


def get_annexure_a_points() -> List[AircraftPoint]:
    """
    Returns the exact 7-point Annexure A dataset specified in the assignment.

    P1 = (2, 3)
    P2 = (12, 30)
    P3 = (40, 50)
    P4 = (5, 1)
    P5 = (12, 10)
    P6 = (3, 4)
    P7 = (30, 30)

    Expected Closest Pair: P1 and P6
    Expected Distance: sqrt((3-2)^2 + (4-3)^2) = sqrt(1 + 1) = sqrt(2) ≈ 1.414214
    """
    return [
        AircraftPoint("P1", 2.0, 3.0),
        AircraftPoint("P2", 12.0, 30.0),
        AircraftPoint("P3", 40.0, 50.0),
        AircraftPoint("P4", 5.0, 1.0),
        AircraftPoint("P5", 12.0, 10.0),
        AircraftPoint("P6", 3.0, 4.0),
        AircraftPoint("P7", 30.0, 30.0),
    ]
