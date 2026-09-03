# Walkthrough: Efficient Nearest-Neighbour Detection for Air-Traffic Collision Alerts (Divide-and-Conquer)

**Course:** CSA0620 – Design and Analysis of Algorithms  
**Assignment Submission:** Divide-and-Conquer vs. Brute-Force Closest Pair Detection for Aviation Safety  

---

## 1. Project Execution Summary

The complete project architecture has been built, tested, validated, and verified inside the workspace. All core algorithms operate with pure Python standard library routines, with `matplotlib` providing high-resolution visual evidence for academic evaluation.

### Key Deliverables Completed:
- [x] **Data Models (`src/models.py`)**: `AircraftPoint`, `ClosestPairResult`, Euclidean and squared distance calculation utilities.
- [x] **Part A – Brute-Force Baseline (`src/brute_force.py`)**: Exact $\Theta(n^2)$ pairwise search with deterministic tie-breaking and complete 21-pair table generation.
- [x] **Part B – Divide-and-Conquer Engine (`src/divide_conquer.py`)**: True $\Theta(n \log n)$ implementation featuring median partitioning, linear $P_y$ subset filtering, and proof-backed $\le 7$-neighbor vertical strip pruning.
- [x] **Recursion & Table Trace (`src/trace.py`)**: Human-readable step-by-step trace of recursive decomposition, strip bounding boxes, and pairwise table formatting.
- [x] **Synthetic Radar Generator (`src/generator.py`)**: Seeded deterministic coordinate generator for reproducible scaling experiments.
- [x] **Empirical Benchmark Suite (`src/benchmark.py`)**: High-precision `time.perf_counter()` benchmarking measuring runtime, speedup ratios, and exact comparison counts.
- [x] **Visualization Suite (`src/visualization.py`)**: 300 DPI publication-grade radar plots, scaling curves, and geometric strip proof diagrams.
- [x] **Interactive CLI & Command Runner (`run.py` & `src/main.py`)**: 10-option interactive menu and non-interactive command flags (`--all`, `--annexure-a`, `--benchmark`, `--test`, `--table`, `--trace`, `--visualize`).
- [x] **Unit & Consistency Test Suite (`tests/`)**: 22 passing tests covering edge cases ($n=0, 1, 2, 3$, duplicates, collinear points, negative sectors) and randomized equivalence assertions.
- [x] **Academic Report & Documentation (`README.md`)**: Comprehensive 21-section document containing formal pseudocode, Master Theorem derivation, DO-178C avionics reality, UN SDG 9 alignment, and Git setup commands.

---

## 2. Verification & Test Suite Results

The automated test suite was executed across all unit and randomized consistency modules:

```bash
python -m unittest discover tests -v
```

```text
test_annexure_a_exact_match (test_brute_force.TestBruteForce) ... ok
test_collinear_x_coordinates (test_brute_force.TestBruteForce) ... ok
test_collinear_y_coordinates (test_brute_force.TestBruteForce) ... ok
test_duplicate_points (test_brute_force.TestBruteForce) ... ok
test_negative_coordinates (test_brute_force.TestBruteForce) ... ok
test_pairwise_table_annexure_a_count (test_brute_force.TestBruteForce) ... ok
test_three_points (test_brute_force.TestBruteForce) ... ok
test_two_points (test_brute_force.TestBruteForce) ... ok
test_zero_and_one_point (test_brute_force.TestBruteForce) ... ok
test_dense_clustering_equivalence (test_consistency.TestConsistency) ... ok
test_random_datasets_equivalence (test_consistency.TestConsistency) ... ok
test_annexure_a_exact_match (test_divide_conquer.TestDivideAndConquer) ... ok
test_closest_pair_crosses_dividing_line (test_divide_conquer.TestDivideAndConquer) ... ok
test_closest_pair_in_left_half (test_divide_conquer.TestDivideAndConquer) ... ok
test_closest_pair_in_right_half (test_divide_conquer.TestDivideAndConquer) ... ok
test_collinear_x_coordinates (test_divide_conquer.TestDivideAndConquer) ... ok
test_collinear_y_coordinates (test_divide_conquer.TestDivideAndConquer) ... ok
test_duplicate_points (test_divide_conquer.TestDivideAndConquer) ... ok
test_negative_coordinates (test_divide_conquer.TestDivideAndConquer) ... ok
test_three_points (test_divide_conquer.TestDivideAndConquer) ... ok
test_two_points (test_divide_conquer.TestDivideAndConquer) ... ok
test_zero_and_one_point (test_divide_conquer.TestDivideAndConquer) ... ok

----------------------------------------------------------------------
Ran 22 tests in 0.042s
OK
```

---

## 3. Annexure A Analytical Verification

Both algorithms were executed on the mandatory Annexure A dataset:

| Aircraft | Coordinate Vector |
| :---: | :---: |
| **P1** | $(2.0, 3.0)$ |
| **P2** | $(12.0, 30.0)$ |
| **P3** | $(40.0, 50.0)$ |
| **P4** | $(5.0, 1.0)$ |
| **P5** | $(12.0, 10.0)$ |
| **P6** | $(3.0, 4.0)$ |
| **P7** | $(30.0, 30.0)$ |

### Comparative Execution Results:
```text
==================================================================================
VALIDATION & SIDE-BY-SIDE COMPARISON: ANNEXURE A
==================================================================================
Metric                    | Brute Force (O(n²))       | Divide & Conquer (O(n log n))
----------------------------------------------------------------------------------
Closest Aircraft Pair     | P1-P6                     | P1-P6                    
Euclidean Distance        | 1.414214                  | 1.414214                 
Comparisons Evaluated     | 21                        | 6                        
----------------------------------------------------------------------------------
Validation Status: MATCH / CORRECT (PASS)
==================================================================================
```

---

## 4. Empirical Performance Benchmarking

Native benchmark measurements recorded on real system hardware (`time.perf_counter()`):

| Input Size ($N$) | Brute-Force Time ($T_{\text{BF}}$) | Divide-and-Conquer Time ($T_{\text{DC}}$) | Measured Speedup | BF Comparisons | DC Comparisons | Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **15** | 0.0333 ms | 0.0826 ms | **0.40x** | 105 | 14 | **MATCH** |
| **50** | 0.3506 ms | 0.2380 ms | **1.47x** | 1,225 | 63 | **MATCH** |
| **100** | 1.3779 ms | 0.5396 ms | **2.55x** | 4,950 | 137 | **MATCH** |
| **500** | 34.5539 ms | 4.1492 ms | **8.33x** | 124,750 | 557 | **MATCH** |
| **1,000** | 146.0049 ms | 9.1563 ms | **15.95x** | 499,500 | 1,128 | **MATCH** |
| **2,000** | 588.2639 ms | 25.3018 ms | **23.25x** | 1,999,000 | 2,276 | **MATCH** |

---

## 5. Visual Artifacts Generated

The following figures were generated at 300 DPI and saved in [screenshots/](file:///c:/Users/pulis/OneDrive/Desktop/DAA%20ASSIGNMENT/screenshots) and [results/](file:///c:/Users/pulis/OneDrive/Desktop/DAA%20ASSIGNMENT/results):

1. **[annexure_a_radar_plot.png](file:///c:/Users/pulis/OneDrive/Desktop/DAA%20ASSIGNMENT/screenshots/annexure_a_radar_plot.png)**: ATC radar sector map displaying aircraft P1–P7, dividing line $x=12.0$, and collision alert vector for P1–P6.
2. **[algorithm_scaling_benchmark.png](file:///c:/Users/pulis/OneDrive/Desktop/DAA%20ASSIGNMENT/screenshots/algorithm_scaling_benchmark.png)**: Linear runtime growth comparison and empirical speedup curve ($0.40x \to 23.25x$).
3. **[divide_conquer_strip_diagram.png](file:///c:/Users/pulis/OneDrive/Desktop/DAA%20ASSIGNMENT/screenshots/divide_conquer_strip_diagram.png)**: Geometric diagram of the vertical strip and the 8 sub-box packing proof for the 7-neighbor bound.
