"""
Divide-and-Conquer Closest-Pair Implementation with Recursion Tracing.

Course: CSA0620 - Design and Analysis of Algorithms
Module: divide_conquer.py

Complexity Analysis:
- Preprocessing: Sorting points by X and Y coordinates takes O(n log n).
- Divide Step: Finding mid-point and partitioning into left/right takes O(n) or O(1).
- Conquer Step: Two recursive calls on n/2 subproblems: 2 * T(n/2).
- Combine Step (Strip Processing):
  * Filtering points within distance delta of x_mid takes O(n) because points are already Y-sorted.
  * For each point in the strip, geometric packing proofs establish that at most 7 subsequent
    points can lie within the delta x 2*delta bounding box.
  * Hence, strip comparison takes at most 7 * n = O(n) comparisons.
- Recurrence Relation:
  T(n) = 2 * T(n/2) + O(n)
  By Master Theorem (Case 2: a=2, b=2, d=1, log_b(a) = 1 == d):
  T(n) in Theta(n log n).
- Space Complexity: O(n) for recursive slicing and strip buffers.
"""

from __future__ import annotations
import math
from typing import List, Optional, Tuple, Dict, Any
from src.models import AircraftPoint, ClosestPairResult, squared_distance, euclidean_distance


class RecursionTraceLogger:
    """
    Structured logger to capture the execution trace of the Divide-and-Conquer algorithm.
    Used for academic demonstration, debugging, and report generation.
    """

    def __init__(self):
        self.events: List[Dict[str, Any]] = []
        self.comparison_count: int = 0

    def log_call(self, depth: int, points: List[AircraftPoint]):
        self.events.append({
            "type": "CALL",
            "depth": depth,
            "points": [p.id for p in points],
            "n": len(points),
        })

    def log_base_case(self, depth: int, points: List[AircraftPoint], best_pair: Optional[Tuple[AircraftPoint, AircraftPoint]], dist: float):
        self.events.append({
            "type": "BASE_CASE",
            "depth": depth,
            "points": [p.id for p in points],
            "best_pair": (best_pair[0].id, best_pair[1].id) if best_pair else None,
            "distance": dist,
        })

    def log_split(self, depth: int, mid_x: float, left_points: List[AircraftPoint], right_points: List[AircraftPoint]):
        self.events.append({
            "type": "SPLIT",
            "depth": depth,
            "mid_x": mid_x,
            "left": [p.id for p in left_points],
            "right": [p.id for p in right_points],
        })

    def log_merge(
        self,
        depth: int,
        mid_x: float,
        delta_left: float,
        left_pair: Optional[Tuple[AircraftPoint, AircraftPoint]],
        delta_right: float,
        right_pair: Optional[Tuple[AircraftPoint, AircraftPoint]],
        delta_min: float,
        strip_points: List[AircraftPoint],
        strip_comparisons: List[Tuple[str, str, float]],
        final_pair: Tuple[AircraftPoint, AircraftPoint],
        final_dist: float,
    ):
        self.events.append({
            "type": "MERGE",
            "depth": depth,
            "mid_x": mid_x,
            "delta_left": delta_left,
            "left_pair": (left_pair[0].id, left_pair[1].id) if left_pair else None,
            "delta_right": delta_right,
            "right_pair": (right_pair[0].id, right_pair[1].id) if right_pair else None,
            "delta_min": delta_min,
            "strip_points": [p.id for p in strip_points],
            "strip_comparisons": strip_comparisons,
            "final_pair": (final_pair[0].id, final_pair[1].id),
            "final_dist": final_dist,
        })


def _base_case_solve(
    points: List[AircraftPoint],
    tracer: Optional[RecursionTraceLogger] = None
) -> Tuple[AircraftPoint, AircraftPoint, float, float]:
    """
    Solves base cases (n = 2 or n = 3) using direct pairwise comparison.

    Returns:
        Tuple of (best_p1, best_p2, min_sq_dist, min_euclidean_dist).
    """
    n = len(points)
    min_sq = float("inf")
    best_p1 = points[0]
    best_p2 = points[1]

    for i in range(n):
        for j in range(i + 1, n):
            if tracer is not None:
                tracer.comparison_count += 1
            sq_d = squared_distance(points[i], points[j])
            if sq_d < min_sq:
                min_sq = sq_d
                best_p1, best_p2 = points[i], points[j]
            elif math.isclose(sq_d, min_sq, rel_tol=1e-12, abs_tol=1e-12):
                # Deterministic tie-breaking
                cand = (points[i], points[j]) if points[i].id < points[j].id else (points[j], points[i])
                curr = (best_p1, best_p2) if best_p1.id < best_p2.id else (best_p2, best_p1)
                if (cand[0].id, cand[1].id) < (curr[0].id, curr[1].id):
                    best_p1, best_p2 = cand[0], cand[1]

    return best_p1, best_p2, min_sq, math.sqrt(min_sq)


def _closest_in_strip(
    strip: List[AircraftPoint],
    delta: float,
    current_best_pair: Tuple[AircraftPoint, AircraftPoint],
    tracer: Optional[RecursionTraceLogger] = None
) -> Tuple[Tuple[AircraftPoint, AircraftPoint], float, List[Tuple[str, str, float]]]:
    """
    Finds the closest pair of aircraft in the vertical strip centered at x_mid.

    Geometric Invariant (Proof of 7-Point Bound):
    The strip contains points whose x-distance to the dividing line is < delta.
    Any two points in the same half (left or right) are at distance >= delta.
    In the d x 2d rectangle, at most 8 points can exist (4 on each side of the dividing line).
    Thus, for each point strip[i], we only need to inspect up to the next 7 points in strip
    whose y-coordinate difference is strictly less than delta.

    Args:
        strip: List of AircraftPoint objects sorted in ascending order of Y-coordinate.
        delta: Minimum distance found from left and right recursive subproblems.
        current_best_pair: Best aircraft pair found from left/right halves.
        tracer: Optional RecursionTraceLogger.

    Returns:
        Tuple of (best_pair, min_distance, comparison_records).
    """
    min_dist = delta
    best_pair = current_best_pair
    min_sq = delta * delta
    m = len(strip)
    comparisons: List[Tuple[str, str, float]] = []

    for i in range(m):
        p1 = strip[i]
        # Inspect up to next 7 points in the y-sorted strip
        max_lookahead = min(i + 8, m)
        for j in range(i + 1, max_lookahead):
            p2 = strip[j]

            # If y-difference exceeds current best delta, no subsequent points can be closer
            dy = p2.y - p1.y
            if dy >= min_dist:
                break

            if tracer is not None:
                tracer.comparison_count += 1

            sq_d = squared_distance(p1, p2)
            d = math.sqrt(sq_d)
            comparisons.append((p1.id, p2.id, d))

            if sq_d < min_sq:
                min_sq = sq_d
                min_dist = d
                best_pair = (p1, p2)
            elif math.isclose(sq_d, min_sq, rel_tol=1e-12, abs_tol=1e-12):
                cand = (p1, p2) if p1.id < p2.id else (p2, p1)
                curr = (best_pair[0], best_pair[1]) if best_pair[0].id < best_pair[1].id else (best_pair[1], best_pair[0])
                if (cand[0].id, cand[1].id) < (curr[0].id, curr[1].id):
                    best_pair = cand

    return best_pair, min_dist, comparisons


def _closest_pair_recursive(
    px: List[AircraftPoint],
    py: List[AircraftPoint],
    tracer: Optional[RecursionTraceLogger] = None,
    depth: int = 0
) -> Tuple[AircraftPoint, AircraftPoint, float]:
    """
    Recursive core of the O(n log n) divide-and-conquer closest-pair algorithm.

    Args:
        px: Aircraft points sorted by X-coordinate (tie-break by Y, ID).
        py: Aircraft points sorted by Y-coordinate (tie-break by X, ID).
        tracer: Optional tracer for logging execution.
        depth: Recursion call depth.

    Returns:
        Tuple of (best_p1, best_p2, min_euclidean_distance).
    """
    n = len(px)
    if tracer:
        tracer.log_call(depth, px)

    # Base Case: n <= 3 solved directly in O(1)
    if n <= 3:
        p1, p2, _, d = _base_case_solve(px, tracer)
        if tracer:
            tracer.log_base_case(depth, px, (p1, p2), d)
        return p1, p2, d

    # Divide: Bisect at median point
    mid_idx = n // 2
    mid_point = px[mid_idx]
    mid_x = mid_point.x

    qx = px[:mid_idx]
    rx = px[mid_idx:]

    # Partition py into left (qy) and right (ry) subsets in linear O(n) time
    left_ids = {p.id for p in qx}
    qy = [p for p in py if p.id in left_ids]
    ry = [p for p in py if p.id not in left_ids]

    if tracer:
        tracer.log_split(depth, mid_x, qx, rx)

    # Conquer: Solve left and right subproblems recursively
    left_p1, left_p2, delta_left = _closest_pair_recursive(qx, qy, tracer, depth + 1)
    right_p1, right_p2, delta_right = _closest_pair_recursive(rx, ry, tracer, depth + 1)

    # Determine delta = min(delta_left, delta_right)
    if delta_left < delta_right:
        delta = delta_left
        best_pair = (left_p1, left_p2)
    elif math.isclose(delta_left, delta_right, rel_tol=1e-12, abs_tol=1e-12):
        cand_l = (left_p1, left_p2) if left_p1.id < left_p2.id else (left_p2, left_p1)
        cand_r = (right_p1, right_p2) if right_p1.id < right_p2.id else (right_p2, right_p1)
        if (cand_l[0].id, cand_l[1].id) <= (cand_r[0].id, cand_r[1].id):
            delta = delta_left
            best_pair = cand_l
        else:
            delta = delta_right
            best_pair = cand_r
    else:
        delta = delta_right
        best_pair = (right_p1, right_p2)

    # Combine: Construct vertical strip around x_mid with width 2*delta
    # Since py is already sorted by Y, filtering preserves Y-order in O(n) time!
    strip = [p for p in py if abs(p.x - mid_x) < delta]

    # Find closest pair across the vertical dividing strip
    strip_best_pair, final_delta, strip_comparisons = _closest_in_strip(strip, delta, best_pair, tracer)

    if tracer:
        tracer.log_merge(
            depth=depth,
            mid_x=mid_x,
            delta_left=delta_left,
            left_pair=(left_p1, left_p2),
            delta_right=delta_right,
            right_pair=(right_p1, right_p2),
            delta_min=delta,
            strip_points=strip,
            strip_comparisons=strip_comparisons,
            final_pair=strip_best_pair,
            final_dist=final_delta,
        )

    return strip_best_pair[0], strip_best_pair[1], final_delta


def closest_pair_divide_and_conquer(
    points: List[AircraftPoint],
    tracer: Optional[RecursionTraceLogger] = None
) -> Optional[ClosestPairResult]:
    """
    Finds the closest pair of aircraft in O(n log n) time using Divide and Conquer.

    Args:
        points: List of AircraftPoint objects.
        tracer: Optional RecursionTraceLogger to capture the recursion tree.

    Returns:
        ClosestPairResult containing the closest pair and minimum distance,
        or None if len(points) < 2.
    """
    n = len(points)
    if n < 2:
        return None

    if n == 2:
        d = euclidean_distance(points[0], points[1])
        if tracer:
            tracer.comparison_count = 1
        return ClosestPairResult(
            point1=points[0],
            point2=points[1],
            distance=d,
            comparisons_count=1,
            algorithm="Divide and Conquer"
        )

    # Pre-sorting step: O(n log n)
    # Sort deterministically by (x, y, id) and (y, x, id)
    px = sorted(points, key=lambda p: (p.x, p.y, p.id))
    py = sorted(points, key=lambda p: (p.y, p.x, p.id))

    comp_counter = 0
    if tracer is None:
        internal_tracer = RecursionTraceLogger()
        p1, p2, dist = _closest_pair_recursive(px, py, internal_tracer, depth=0)
        comp_counter = internal_tracer.comparison_count
    else:
        p1, p2, dist = _closest_pair_recursive(px, py, tracer, depth=0)
        comp_counter = tracer.comparison_count

    return ClosestPairResult(
        point1=p1,
        point2=p2,
        distance=dist,
        comparisons_count=comp_counter,
        algorithm="Divide and Conquer"
    )
