"""
Performance Benchmarking Module for Closest-Pair Algorithms.

Course: CSA0620 - Design and Analysis of Algorithms
Module: benchmark.py
"""

from __future__ import annotations
import time
import math
import csv
import os
from typing import List, Dict, Any, Tuple
from src.models import AircraftPoint
from src.brute_force import closest_pair_brute_force
from src.divide_conquer import closest_pair_divide_and_conquer
from src.generator import generate_random_aircraft_points


def benchmark_single_size(
    n: int,
    seed: int = 42,
    repetitions: int = 5
) -> Dict[str, Any]:
    """
    Executes a high-precision performance comparison between Brute-Force and Divide-and-Conquer
    for a specific dataset size n.

    Args:
        n: Number of aircraft points.
        seed: Random seed for deterministic data generation.
        repetitions: Number of iterations to average over.

    Returns:
        Dictionary containing measured metrics:
        - n: Input size
        - time_bf_ms: Brute Force execution time in milliseconds
        - time_dc_ms: Divide & Conquer execution time in milliseconds
        - speedup: Speedup ratio (T_bf / T_dc)
        - dist_bf: Distance found by Brute Force
        - dist_dc: Distance found by Divide & Conquer
        - same_result: True if |dist_bf - dist_dc| < 1e-9
        - comp_bf: Comparison count for Brute Force
        - comp_dc: Comparison count for Divide & Conquer
    """
    points = generate_random_aircraft_points(n, seed=seed)

    # Measure Brute Force execution time
    times_bf = []
    res_bf = None
    for _ in range(repetitions):
        start = time.perf_counter()
        res_bf = closest_pair_brute_force(points)
        end = time.perf_counter()
        times_bf.append((end - start) * 1000.0)  # ms

    # Measure Divide and Conquer execution time
    times_dc = []
    res_dc = None
    for _ in range(repetitions):
        start = time.perf_counter()
        res_dc = closest_pair_divide_and_conquer(points)
        end = time.perf_counter()
        times_dc.append((end - start) * 1000.0)  # ms

    avg_bf_ms = sum(times_bf) / len(times_bf)
    avg_dc_ms = sum(times_dc) / len(times_dc)
    speedup = avg_bf_ms / avg_dc_ms if avg_dc_ms > 0 else 1.0

    assert res_bf is not None
    assert res_dc is not None

    same_result = math.isclose(res_bf.distance, res_dc.distance, rel_tol=1e-8, abs_tol=1e-8)

    return {
        "n": n,
        "time_bf_ms": avg_bf_ms,
        "time_dc_ms": avg_dc_ms,
        "speedup": speedup,
        "dist_bf": res_bf.distance,
        "dist_dc": res_dc.distance,
        "same_result": same_result,
        "comp_bf": res_bf.comparisons_count,
        "comp_dc": res_dc.comparisons_count,
        "pair_bf": res_bf.pair_names,
        "pair_dc": res_dc.pair_names,
    }


def run_benchmark_suite(
    sizes: Optional[List[int]] = None,
    seed: int = 42,
    csv_output_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Runs the full benchmarking suite across multiple input sizes.

    Default sizes: [15, 50, 100, 500, 1000, 2000]

    Args:
        sizes: Custom list of dataset sizes.
        seed: Random seed.
        csv_output_path: Path to save CSV results.

    Returns:
        List of benchmark metric dictionaries.
    """
    if sizes is None:
        sizes = [15, 50, 100, 500, 1000, 2000]

    results = []
    for n in sizes:
        reps = 10 if n <= 100 else (5 if n <= 500 else 3)
        metrics = benchmark_single_size(n, seed=seed, repetitions=reps)
        results.append(metrics)

    # Save to CSV if path provided or default
    if csv_output_path:
        os.makedirs(os.path.dirname(os.path.abspath(csv_output_path)), exist_ok=True)
        with open(csv_output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Input Size (N)",
                "Brute Force Time (ms)",
                "Divide & Conquer Time (ms)",
                "Speedup (BF/DC)",
                "BF Comparisons",
                "DC Comparisons",
                "Result Match",
                "Distance"
            ])
            for r in results:
                writer.writerow([
                    r["n"],
                    f"{r['time_bf_ms']:.4f}",
                    f"{r['time_dc_ms']:.4f}",
                    f"{r['speedup']:.2f}x",
                    r["comp_bf"],
                    r["comp_dc"],
                    "MATCH" if r["same_result"] else "MISMATCH",
                    f"{r['dist_dc']:.6f}"
                ])

    return results


def format_benchmark_table(results: List[Dict[str, Any]]) -> str:
    """
    Formats the benchmark results into a clean terminal/report table.
    """
    lines = []
    lines.append("=" * 86)
    lines.append("EMPIRICAL PERFORMANCE BENCHMARK: BRUTE FORCE VS DIVIDE AND CONQUER")
    lines.append("=" * 86)
    lines.append(
        f"{'N (Aircraft)':<12} | {'Brute Force (ms)':<17} | {'Divide & Conquer (ms)':<22} | "
        f"{'Speedup':<9} | {'Verification'}"
    )
    lines.append("-" * 86)

    for r in results:
        status = "MATCH (Pass)" if r["same_result"] else "MISMATCH (Fail)"
        lines.append(
            f"{r['n']:<12} | {r['time_bf_ms']:<17.4f} | {r['time_dc_ms']:<22.4f} | "
            f"{r['speedup']:<8.2f}x | {status}"
        )

    lines.append("-" * 86)
    lines.append("Algorithmic Note on Measured Timings:")
    lines.append("* At small n (n <= 15), Brute Force is competitive due to low constant overhead.")
    lines.append("* As n increases (n >= 500), Divide-and-Conquer exhibits dramatic O(n log n) speedup")
    lines.append("  over O(n^2) Brute Force, proving essential for large-scale real-time radar sweeps.")
    lines.append("=" * 86)

    return "\n".join(lines)
