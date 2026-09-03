"""
Brute-Force Closest-Pair Implementation and Pairwise Distance Table Generator.

Course: CSA0620 - Design and Analysis of Algorithms
Module: brute_force.py

Complexity Analysis:
- Time Complexity: O(n^2)
  The algorithm iterates through every distinct pair of points (P_i, P_j) where 0 <= i < j < n.
  Total comparisons = n * (n - 1) / 2 = (n^2 - n) / 2, which is Theta(n^2).
- Space Complexity: O(1) auxiliary space (beyond storage for the input list).
"""

from __future__ import annotations
import math
from typing import List, Optional, Tuple, Dict, Any
from src.models import AircraftPoint, ClosestPairResult, squared_distance, euclidean_distance


def closest_pair_brute_force(points: List[AircraftPoint]) -> Optional[ClosestPairResult]:
    """
    Finds the closest pair of aircraft in a given 2D sector using exhaustive search.

    Algorithmic Steps:
    1. Validate input size: return None if fewer than 2 aircraft are provided.
    2. Initialize minimum squared distance to infinity.
    3. Evaluate each unique pair (p1, p2) with nested loops (i from 0 to n-1, j from i+1 to n-1).
    4. Compute squared Euclidean distance (avoiding sqrt in loop).
    5. Update best pair deterministically when a strictly smaller distance (or tie-break) is found.
    6. Compute exact Euclidean distance sqrt(d_sq) once for the winning pair.

    Args:
        points: List of AircraftPoint objects.

    Returns:
        ClosestPairResult containing the two closest aircraft, their distance,
        and total comparison count; or None if len(points) < 2.
    """
    n = len(points)
    if n < 2:
        return None

    if n == 2:
        d = euclidean_distance(points[0], points[1])
        return ClosestPairResult(
            point1=points[0],
            point2=points[1],
            distance=d,
            comparisons_count=1,
            algorithm="Brute Force"
        )

    min_sq_dist = float("inf")
    best_pair: Optional[Tuple[AircraftPoint, AircraftPoint]] = None
    comparison_count = 0

    for i in range(n):
        p1 = points[i]
        for j in range(i + 1, n):
            p2 = points[j]
            comparison_count += 1
            sq_d = squared_distance(p1, p2)

            # Deterministic comparison: strictly smaller distance, or deterministic tie-breaker
            if sq_d < min_sq_dist:
                min_sq_dist = sq_d
                best_pair = (p1, p2)
            elif math.isclose(sq_d, min_sq_dist, rel_tol=1e-12, abs_tol=1e-12):
                # Tie-breaking logic: pick lexicographically smallest pair identifier
                candidate_pair = (p1, p2) if (p1.id, p2.id) < (p2.id, p1.id) else (p2, p1)
                assert best_pair is not None
                current_canonical = (best_pair[0], best_pair[1]) if (best_pair[0].id, best_pair[1].id) < (best_pair[1].id, best_pair[0].id) else (best_pair[1], best_pair[0])
                if (candidate_pair[0].id, candidate_pair[1].id) < (current_canonical[0].id, current_canonical[1].id):
                    best_pair = candidate_pair

    assert best_pair is not None
    return ClosestPairResult(
        point1=best_pair[0],
        point2=best_pair[1],
        distance=math.sqrt(min_sq_dist),
        comparisons_count=comparison_count,
        algorithm="Brute Force"
    )


def compute_all_pairwise_distances(points: List[AircraftPoint]) -> List[Dict[str, Any]]:
    """
    Exhaustively computes and tabulates all n*(n-1)/2 pairwise distances.
    For Annexure A (n=7), computes exactly 7C2 = 21 unique pairs.

    Args:
        points: List of AircraftPoint objects.

    Returns:
        List of dictionaries containing detailed step-by-step arithmetic for each pair:
        - pair_name: e.g. 'P1-P2'
        - p1: First aircraft point
        - p2: Second aircraft point
        - dx: (x2 - x1)
        - dy: (y2 - y1)
        - dx2_plus_dy2: squared Euclidean distance
        - distance: actual Euclidean distance
        - is_minimum: boolean flag indicating if this pair is the global minimum
    """
    n = len(points)
    records = []
    min_dist = float("inf")

    for i in range(n):
        for j in range(i + 1, n):
            p1 = points[i]
            p2 = points[j]
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            sq_d = dx * dx + dy * dy
            dist = math.sqrt(sq_d)

            if dist < min_dist:
                min_dist = dist

            records.append({
                "pair_name": f"{p1.id}-{p2.id}",
                "p1": p1,
                "p2": p2,
                "p1_str": f"{p1.id}({p1.x:g}, {p1.y:g})",
                "p2_str": f"{p2.id}({p2.x:g}, {p2.y:g})",
                "dx": dx,
                "dy": dy,
                "sq_dist": sq_d,
                "distance": dist,
                "is_minimum": False  # set in second pass
            })

    # Mark minimum pair(s)
    for rec in records:
        if math.isclose(rec["distance"], min_dist, rel_tol=1e-9, abs_tol=1e-9):
            rec["is_minimum"] = True

    return records
