"""
Main CLI Application and Interactive Menu for DAA Closest-Pair Assignment.

Course: CSA0620 - Design and Analysis of Algorithms
Module: main.py
"""

from __future__ import annotations
import sys
import os
import argparse
import unittest
import math

# Ensure proper encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from src.models import get_annexure_a_points
from src.brute_force import closest_pair_brute_force, compute_all_pairwise_distances
from src.divide_conquer import closest_pair_divide_and_conquer
from src.trace import format_annexure_a_trace, format_pairwise_distance_table
from src.generator import generate_random_aircraft_points
from src.benchmark import run_benchmark_suite, format_benchmark_table
from src.visualization import (
    plot_annexure_a_radar,
    plot_benchmark_scaling,
    plot_divide_conquer_strip_concept
)


def print_banner():
    print("=" * 82)
    print("  CSA0620 -- DESIGN AND ANALYSIS OF ALGORITHMS ASSIGNMENT")
    print("  Efficient Nearest-Neighbour Detection for Air-Traffic Collision Alerts")
    print("  Paradigm: Divide-and-Conquer vs. Brute-Force Baseline")
    print("=" * 82)


def run_annexure_a_brute_force():
    print("\n" + "=" * 82)
    print("ANNEXURE A -- BRUTE FORCE RESULT")
    print("=" * 82)
    points = get_annexure_a_points()
    print(f"Dataset: Annexure A (n = {len(points)} aircraft)")
    for p in points:
        print(f"  * {p.id}: ({p.x:g}, {p.y:g})")
    print("-" * 82)

    result = closest_pair_brute_force(points)
    assert result is not None
    print(f"Algorithm            : {result.algorithm}")
    print(f"Closest Pair Found   : {result.point1.id} {result.point1.as_tuple()} and {result.point2.id} {result.point2.as_tuple()}")
    print(f"Pair Identifier      : {result.pair_names}")
    print(f"Euclidean Distance   : {result.distance:.6f}  (Exact: sqrt(2) approx 1.414214)")
    print(f"Pairwise Comparisons : {result.comparisons_count} (Exhaustive: 7C2 = 21)")
    print("=" * 82)
    return result


def run_annexure_a_divide_conquer():
    print("\n" + "=" * 82)
    print("ANNEXURE A -- DIVIDE AND CONQUER RESULT")
    print("=" * 82)
    points = get_annexure_a_points()
    print(f"Dataset: Annexure A (n = {len(points)} aircraft)")
    print("-" * 82)

    result = closest_pair_divide_and_conquer(points)
    assert result is not None
    print(f"Algorithm            : {result.algorithm}")
    print(f"Closest Pair Found   : {result.point1.id} {result.point1.as_tuple()} and {result.point2.id} {result.point2.as_tuple()}")
    print(f"Pair Identifier      : {result.pair_names}")
    print(f"Euclidean Distance   : {result.distance:.6f}  (Exact: sqrt(2) approx 1.414214)")
    print(f"Pairwise Comparisons : {result.comparisons_count} (Efficient O(n log n) strip comparisons)")
    print("=" * 82)
    return result


def compare_both_algorithms():
    print("\n" + "=" * 82)
    print("VALIDATION & SIDE-BY-SIDE COMPARISON: ANNEXURE A")
    print("=" * 82)
    points = get_annexure_a_points()
    res_bf = closest_pair_brute_force(points)
    res_dc = closest_pair_divide_and_conquer(points)
    assert res_bf is not None and res_dc is not None

    match = math.isclose(res_bf.distance, res_dc.distance, rel_tol=1e-9)
    pair_match = res_bf.pair_names == res_dc.pair_names

    print(f"{'Metric':<25} | {'Brute Force (O(n²))':<25} | {'Divide & Conquer (O(n log n))':<25}")
    print("-" * 82)
    print(f"{'Closest Aircraft Pair':<25} | {res_bf.pair_names:<25} | {res_dc.pair_names:<25}")
    print(f"{'Euclidean Distance':<25} | {res_bf.distance:<25.6f} | {res_dc.distance:<25.6f}")
    print(f"{'Comparisons Evaluated':<25} | {res_bf.comparisons_count:<25} | {res_dc.comparisons_count:<25}")
    print("-" * 82)
    print(f"Validation Status: {'MATCH / CORRECT (PASS)' if (match and pair_match) else 'MISMATCH (FAIL)'}")
    print("=" * 82)


def show_pairwise_distance_table():
    print("\n" + format_pairwise_distance_table())
    # Save output to text file in results/
    os.makedirs("results", exist_ok=True)
    with open("results/pairwise_distances_annexure_a.txt", "w", encoding="utf-8") as f:
        f.write(format_pairwise_distance_table())
    print("\n[INFO] Saved complete 21-pair table to results/pairwise_distances_annexure_a.txt")


def show_divide_conquer_trace():
    print("\n" + format_annexure_a_trace())


def generate_and_inspect_random(n: int = 15, seed: int = 42):
    print("\n" + "=" * 82)
    print(f"RANDOM RADAR DATASET GENERATION (N = {n}, Seed = {seed})")
    print("=" * 82)
    points = generate_random_aircraft_points(n=n, seed=seed)
    print(f"Generated {len(points)} synthetic aircraft tracks in sector [0, 1000] x [0, 1000]:")
    for idx, p in enumerate(points[:10], start=1):
        print(f"  {idx:2d}. {p.id}: ({p.x:6.2f}, {p.y:6.2f})")
    if len(points) > 10:
        print(f"  ... and {len(points) - 10} more aircraft.")
    print("-" * 82)

    res_bf = closest_pair_brute_force(points)
    res_dc = closest_pair_divide_and_conquer(points)
    assert res_bf is not None and res_dc is not None

    print(f"Brute Force Result       : {res_bf.pair_names} | Distance: {res_bf.distance:.6f} | Comp: {res_bf.comparisons_count}")
    print(f"Divide & Conquer Result  : {res_dc.pair_names} | Distance: {res_dc.distance:.6f} | Comp: {res_dc.comparisons_count}")
    match = math.isclose(res_bf.distance, res_dc.distance, rel_tol=1e-8)
    print(f"Equivalence Verification : {'MATCH (PASS)' if match else 'MISMATCH (FAIL)'}")
    print("=" * 82)


def run_benchmark():
    print("\n" + "=" * 82)
    print("RUNNING EMPIRICAL BENCHMARK SUITE (Sizes N = 15, 50, 100, 500, 1000, 2000)...")
    print("=" * 82)
    results = run_benchmark_suite(csv_output_path="results/benchmark_results.csv")
    print("\n" + format_benchmark_table(results))
    print("\n[INFO] Benchmark CSV saved to results/benchmark_results.csv")
    return results


def run_all_tests():
    print("\n" + "=" * 82)
    print("EXECUTING UNIT AND INTEGRATION TEST SUITE")
    print("=" * 82)
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    test_result = runner.run(suite)
    print("-" * 82)
    if test_result.wasSuccessful():
        print(f"ALL TESTS PASSED! Total Tests Run: {test_result.testsRun}")
    else:
        print(f"TEST FAILURES DETECTED! Errors: {len(test_result.errors)}, Failures: {len(test_result.failures)}")
    print("=" * 82)
    return test_result.wasSuccessful()


def generate_visualizations(benchmark_data=None):
    print("\n" + "=" * 82)
    print("GENERATING PUBLICATION-GRADE VISUALIZATIONS (300 DPI)")
    print("=" * 82)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    # 1. Annexure A Radar Plot
    p1 = plot_annexure_a_radar()
    print(f"[1/3] Generated Radar Plot       : {p1}")

    # 2. Benchmark Scaling Plot
    if benchmark_data is None:
        benchmark_data = run_benchmark_suite(csv_output_path="results/benchmark_results.csv")
    p2 = plot_benchmark_scaling(benchmark_data)
    print(f"[2/3] Generated Scaling Benchmark: {p2}")

    # 3. Divide & Conquer Strip Concept Diagram
    p3 = plot_divide_conquer_strip_concept()
    print(f"[3/3] Generated Strip Diagram    : {p3}")

    print("-" * 82)
    print("All figures successfully saved to screenshots/ and results/ directories.")
    print("=" * 82)


def run_full_suite():
    """Executes every assignment requirement in one automated pipeline."""
    print_banner()
    run_annexure_a_brute_force()
    run_annexure_a_divide_conquer()
    compare_both_algorithms()
    show_pairwise_distance_table()
    show_divide_conquer_trace()
    generate_and_inspect_random(n=50, seed=42)
    benchmark_res = run_benchmark()
    run_all_tests()
    generate_visualizations(benchmark_res)
    print("\n" + "=" * 82)
    print("FULL PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 82)


def interactive_menu():
    while True:
        print("\n" + "=" * 82)
        print("  CSA0620 DAA ASSIGNMENT – INTERACTIVE CLI MENU")
        print("=" * 82)
        print("  1. Run Annexure A Brute Force (O(n²))")
        print("  2. Run Annexure A Divide and Conquer (O(n log n))")
        print("  3. Compare Both Algorithms (Side-by-side validation)")
        print("  4. Show Pairwise Distance Table (All 21 Pairs for Annexure A)")
        print("  5. Show Divide-and-Conquer Recursion Trace (Annexure A)")
        print("  6. Generate & Test Random Radar Dataset")
        print("  7. Run Performance Benchmark Suite (N = 15 to 2000)")
        print("  8. Run Unit & Consistency Tests")
        print("  9. Generate High-Resolution Visualizations (Plots)")
        print(" 10. Run Full End-to-End Suite (--all)")
        print("  0. Exit")
        print("=" * 82)

        try:
            choice = input("Enter option [0-10]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if choice == "1":
            run_annexure_a_brute_force()
        elif choice == "2":
            run_annexure_a_divide_conquer()
        elif choice == "3":
            compare_both_algorithms()
        elif choice == "4":
            show_pairwise_distance_table()
        elif choice == "5":
            show_divide_conquer_trace()
        elif choice == "6":
            try:
                n_str = input("Enter dataset size n [default 50]: ").strip()
                n = int(n_str) if n_str else 50
            except ValueError:
                n = 50
            generate_and_inspect_random(n=n, seed=42)
        elif choice == "7":
            run_benchmark()
        elif choice == "8":
            run_all_tests()
        elif choice == "9":
            generate_visualizations()
        elif choice == "10":
            run_full_suite()
        elif choice in ("0", "exit", "quit", "q"):
            print("Exiting. Have a great day!")
            break
        else:
            print("[ERROR] Invalid choice. Please select an option between 0 and 10.")


def main():
    parser = argparse.ArgumentParser(
        description="Air-Traffic Nearest-Neighbour Detection (Divide-and-Conquer vs. Brute-Force)"
    )
    parser.add_argument("--all", action="store_true", help="Run full pipeline including tests, benchmarks, and plots")
    parser.add_argument("--annexure-a", action="store_true", help="Run Annexure A comparison")
    parser.add_argument("--table", action="store_true", help="Display 21-pair distance table for Annexure A")
    parser.add_argument("--trace", action="store_true", help="Display step-by-step Divide and Conquer trace")
    parser.add_argument("--benchmark", action="store_true", help="Run empirical performance benchmarks")
    parser.add_argument("--test", action="store_true", help="Run automated test suite")
    parser.add_argument("--visualize", action="store_true", help="Generate publication-grade visualization plots")
    parser.add_argument("--interactive", "-i", action="store_true", help="Launch interactive menu")

    args = parser.parse_args()

    if args.all:
        run_full_suite()
    elif args.annexure_a:
        print_banner()
        run_annexure_a_brute_force()
        run_annexure_a_divide_conquer()
        compare_both_algorithms()
    elif args.table:
        show_pairwise_distance_table()
    elif args.trace:
        show_divide_conquer_trace()
    elif args.benchmark:
        print_banner()
        run_benchmark()
    elif args.test:
        run_all_tests()
    elif args.visualize:
        generate_visualizations()
    else:
        # Default to interactive menu if no flags passed
        print_banner()
        interactive_menu()


if __name__ == "__main__":
    main()
