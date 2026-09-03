"""
Academic Execution Trace and Pairwise Distance Table Formatter.

Course: CSA0620 - Design and Analysis of Algorithms
Module: trace.py
"""

from __future__ import annotations
from typing import List, Dict, Any
from src.models import AircraftPoint, get_annexure_a_points
from src.brute_force import compute_all_pairwise_distances, closest_pair_brute_force
from src.divide_conquer import closest_pair_divide_and_conquer, RecursionTraceLogger


def format_annexure_a_trace() -> str:
    """
    Generates a detailed, student-readable academic trace of the Divide-and-Conquer
    closest-pair algorithm executing on the Annexure A dataset.
    """
    points = get_annexure_a_points()
    px = sorted(points, key=lambda p: (p.x, p.y, p.id))
    py = sorted(points, key=lambda p: (p.y, p.x, p.id))

    tracer = RecursionTraceLogger()
    result = closest_pair_divide_and_conquer(points, tracer)

    lines = []
    lines.append("=" * 78)
    lines.append("DIVIDE-AND-CONQUER RECURSION TRACE: ANNEXURE A DATASET")
    lines.append("=" * 78)
    lines.append(f"Input Aircraft Points (n = {len(points)}):")
    for p in points:
        lines.append(f"  * {p.id}: (x={p.x:4.1f}, y={p.y:4.1f})")
    lines.append("")

    lines.append("STEP 1: INITIAL PRE-SORTING (O(n log n))")
    lines.append("-" * 78)
    lines.append(f"  Points sorted by X-coordinate (Px):")
    lines.append("    " + " -> ".join([f"{p.id}({p.x:g},{p.y:g})" for p in px]))
    lines.append(f"  Points sorted by Y-coordinate (Py):")
    lines.append("    " + " -> ".join([f"{p.id}({p.x:g},{p.y:g})" for p in py]))
    lines.append("")

    lines.append("STEP 2: RECURSIVE DECOMPOSITION & STRIP COMBINATION")
    lines.append("-" * 78)

    # Walk through logged events to present a clean hierarchical breakdown
    for ev in tracer.events:
        indent = "  " * (ev["depth"] + 1)
        if ev["type"] == "CALL":
            lines.append(f"{indent}[Call Depth {ev['depth']}] Subproblem with {ev['n']} points: {ev['points']}")
        elif ev["type"] == "SPLIT":
            lines.append(f"{indent}  |-- Bisect at Median X = {ev['mid_x']:.1f}")
            lines.append(f"{indent}  |-- Left Subproblem (Qx) : {ev['left']}")
            lines.append(f"{indent}  +-- Right Subproblem (Rx): {ev['right']}")
        elif ev["type"] == "BASE_CASE":
            lines.append(f"{indent}  +-- [Base Case (n<={len(ev['points'])})] Direct solve: Pair {ev['best_pair']}, dist = {ev['distance']:.6f}")
        elif ev["type"] == "MERGE":
            lines.append(f"{indent}  +-- [Merge at Depth {ev['depth']}] Median X = {ev['mid_x']:.1f}")
            lines.append(f"{indent}      |-- Left Result : Pair {ev['left_pair']}, delta_L = {ev['delta_left']:.6f}")
            lines.append(f"{indent}      |-- Right Result: Pair {ev['right_pair']}, delta_R = {ev['delta_right']:.6f}")
            lines.append(f"{indent}      |-- Minimum Delta (delta_min) = {ev['delta_min']:.6f}")
            lines.append(f"{indent}      |-- Vertical Strip Region: [{ev['mid_x'] - ev['delta_min']:.2f}, {ev['mid_x'] + ev['delta_min']:.2f}]")
            lines.append(f"{indent}      |-- Aircraft Points in Strip (Y-ordered): {ev['strip_points']}")
            if ev["strip_comparisons"]:
                lines.append(f"{indent}      |-- Strip Comparisons Checked (<=7 neighbours):")
                for c in ev["strip_comparisons"]:
                    lines.append(f"{indent}      |   * Pair ({c[0]}, {c[1]}): dist = {c[2]:.6f}")
            else:
                lines.append(f"{indent}      |-- Strip Comparisons: None needed (strip contains <2 points or no cross-pairs within delta)")
            lines.append(f"{indent}      +-- Best Pair after Merge: {ev['final_pair']}, distance = {ev['final_dist']:.6f}")
            lines.append("")

    lines.append("=" * 78)
    lines.append("STEP 3: FINAL GLOBAL RESULT")
    lines.append("=" * 78)
    assert result is not None
    lines.append(f"Globally Closest Pair : {result.point1.id} {result.point1.as_tuple()} and {result.point2.id} {result.point2.as_tuple()}")
    lines.append(f"Euclidean Distance    : {result.distance:.6f}  (sqrt(2) approx 1.414214)")
    lines.append(f"Total Comparisons Made: {result.comparisons_count}")
    lines.append("=" * 78)

    return "\n".join(lines)


def format_pairwise_distance_table() -> str:
    """
    Formats the complete 21-pair distance calculation table for Annexure A (n=7).
    7C2 = 7 * 6 / 2 = 21 unique pairs.
    """
    points = get_annexure_a_points()
    records = compute_all_pairwise_distances(points)

    lines = []
    lines.append("=" * 82)
    lines.append("HAND-COMPUTED / EXHAUSTIVE PAIRWISE DISTANCE TABLE (ANNEXURE A)")
    lines.append("Total Aircraft: n = 7  |  Total Unique Pairs: 7C2 = 21 pairs")
    lines.append("Formula: Euclidean Distance d = sqrt((x2 - x1)^2 + (y2 - y1)^2)")
    lines.append("=" * 82)
    lines.append(
        f"{'#':<3} | {'Pair':<7} | {'Point 1 (x1, y1)':<18} | {'Point 2 (x2, y2)':<18} | "
        f"{'dx':<5} | {'dy':<5} | {'dx^2+dy^2':<9} | {'Distance':<10} | {'Status'}"
    )
    lines.append("-" * 82)

    for idx, r in enumerate(records, start=1):
        status = "** MINIMUM **" if r["is_minimum"] else ""
        lines.append(
            f"{idx:<3} | {r['pair_name']:<7} | {r['p1_str']:<18} | {r['p2_str']:<18} | "
            f"{r['dx']:<5.1f} | {r['dy']:<5.1f} | {r['sq_dist']:<9.1f} | {r['distance']:<10.6f} | {status}"
        )

    lines.append("-" * 82)
    min_rec = [r for r in records if r["is_minimum"]][0]
    lines.append(
        f"CONCLUSION: The minimum pairwise distance across all 21 pairs is {min_rec['pair_name']}\n"
        f"with exact distance sqrt({min_rec['sq_dist']:.0f}) = {min_rec['distance']:.6f}."
    )
    lines.append("=" * 82)

    return "\n".join(lines)
