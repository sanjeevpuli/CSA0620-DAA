"""
Visualization Suite for Air-Traffic Nearest-Neighbour Detection.

Course: CSA0620 - Design and Analysis of Algorithms
Module: visualization.py
"""

from __future__ import annotations
import os
import math
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from src.models import get_annexure_a_points, AircraftPoint
from src.divide_conquer import closest_pair_divide_and_conquer


def plot_annexure_a_radar(
    save_paths: Optional[List[str]] = None,
    show_plot: bool = False
) -> str:
    """
    Renders a high-resolution, publication-grade radar plot of the Annexure A dataset.

    Highlights:
    - Aircraft points P1 through P7 with coordinates.
    - Vertical dividing line (x = 12.0) from Divide-and-Conquer.
    - Closest pair (P1, P6) with alert halo, connection line, and distance annotation.

    Args:
        save_paths: List of filepaths to save the rendered image.
        show_plot: Whether to display interactively (default: False).

    Returns:
        Primary saved image filepath.
    """
    if save_paths is None:
        save_paths = [
            "screenshots/annexure_a_radar_plot.png",
            "results/annexure_a_radar_plot.png"
        ]

    points = get_annexure_a_points()
    res = closest_pair_divide_and_conquer(points)
    assert res is not None

    fig, ax = plt.subplots(figsize=(10, 7.5), dpi=300)

    # Modern Aviation Radar Style Styling
    ax.set_facecolor("#0b132b")
    fig.patch.set_facecolor("#1c2541")

    # Grid
    ax.grid(True, linestyle="--", alpha=0.35, color="#48cae4")

    # Plot all aircraft
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    ax.scatter(xs, ys, color="#48cae4", s=110, zorder=4, edgecolor="#ffffff", linewidth=1.5, label="Aircraft (Radar Tracks)")

    # Specific label placement offsets to prevent overlapping in dense clusters (P1 and P6)
    label_offsets = {
        "P1": (-55, -20),  # Down and left of P1(2,3)
        "P6": (16, 12),    # Up and right of P6(3,4)
        "P4": (14, -14),   # Down and right of P4(5,1)
        "P5": (14, -4),    # Right of P5(12,10)
        "P2": (14, 4),     # Right of P2(12,30)
        "P7": (14, 4),     # Right of P7(30,30)
        "P3": (-55, 6),    # Left of P3(40,50)
    }

    # Label points
    for p in points:
        xytext = label_offsets.get(p.id, (8, 8))
        ax.annotate(
            f"{p.id} ({p.x:g}, {p.y:g})",
            (p.x, p.y),
            textcoords="offset points",
            xytext=xytext,
            fontsize=10.5,
            fontweight="bold",
            color="#e0e1dd",
            bbox=dict(boxstyle="round,pad=0.25", facecolor="#1c2541", edgecolor="#3a506b", alpha=0.9),
            zorder=6
        )

    # Median dividing line (x = 12)
    mid_x = 12.0
    ax.axvline(x=mid_x, color="#f77f00", linestyle=":", linewidth=2, label=f"D&C Dividing Line (x = {mid_x:g})", zorder=3)

    # Highlight closest pair (P1, P6)
    p1, p2 = res.point1, res.point2
    ax.scatter([p1.x, p2.x], [p1.y, p2.y], color="#d62828", s=220, zorder=5, edgecolor="#fcbf49", linewidth=2.5, label="Collision Alert Pair (P1-P6)")

    # Connect closest pair with dashed alert vector
    ax.plot([p1.x, p2.x], [p1.y, p2.y], color="#fcbf49", linestyle="-", linewidth=2.5, zorder=5)

    # Proximity alert circle around closest pair
    midpoint_x = (p1.x + p2.x) / 2
    midpoint_y = (p1.y + p2.y) / 2
    alert_circle = patches.Circle((midpoint_x, midpoint_y), 3.5, linewidth=1.5, edgecolor="#e63946", facecolor="none", linestyle="--", zorder=4)
    ax.add_patch(alert_circle)

    # Distance annotation banner
    ax.annotate(
        f"MINIMUM DISTANCE\n{p1.id}-{p2.id} : d = {res.distance:.6f}\n(sqrt(2) ≈ 1.414214)",
        xy=(midpoint_x, midpoint_y),
        xytext=(midpoint_x + 6.5, midpoint_y + 6.0),
        arrowprops=dict(arrowstyle="->", color="#fcbf49", lw=1.8),
        fontsize=10.5,
        fontweight="heavy",
        color="#fcbf49",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="#03071e", edgecolor="#d62828", linewidth=1.8),
        zorder=7
    )

    # Sector bounds and titles
    ax.set_xlim(-2, 45)
    ax.set_ylim(-3, 55)
    ax.set_xlabel("Radar Sector X-Coordinate (km / nmi)", fontsize=11, fontweight="bold", color="#e0e1dd")
    ax.set_ylabel("Radar Sector Y-Coordinate (km / nmi)", fontsize=11, fontweight="bold", color="#e0e1dd")
    ax.tick_params(colors="#e0e1dd", labelsize=9.5)

    plt.title(
        "Closest Aircraft Pair – Divide and Conquer Proximity Alert\n"
        "Annexure A Dataset | CSA0620 Design and Analysis of Algorithms",
        fontsize=13,
        fontweight="bold",
        color="#ffffff",
        pad=16
    )

    legend = ax.legend(loc="upper left", facecolor="#1c2541", edgecolor="#3a506b", labelcolor="#e0e1dd", fontsize=9.5)
    legend.get_frame().set_alpha(0.9)

    plt.tight_layout()

    primary_path = save_paths[0]
    for path in save_paths:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        fig.savefig(path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")

    if show_plot:
        plt.show()
    plt.close(fig)

    return primary_path


def plot_benchmark_scaling(
    benchmark_results: List[Dict[str, Any]],
    save_paths: Optional[List[str]] = None,
    show_plot: bool = False
) -> str:
    """
    Renders a comparative performance chart:
    1. Execution Time vs Input Size N (O(n^2) Brute Force vs O(n log n) Divide & Conquer).
    2. Speedup Factor (T_bf / T_dc) vs Input Size N.
    """
    if save_paths is None:
        save_paths = [
            "screenshots/algorithm_scaling_benchmark.png",
            "results/algorithm_scaling_benchmark.png"
        ]

    ns = [r["n"] for r in benchmark_results]
    t_bf = [r["time_bf_ms"] for r in benchmark_results]
    t_dc = [r["time_dc_ms"] for r in benchmark_results]
    speedups = [r["speedup"] for r in benchmark_results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)
    fig.patch.set_facecolor("#f8f9fa")

    # Plot 1: Execution Time Comparison
    ax1.set_facecolor("#ffffff")
    ax1.plot(ns, t_bf, marker="o", linewidth=2.4, color="#d90429", label="Brute Force O(n²)")
    ax1.plot(ns, t_dc, marker="s", linewidth=2.4, color="#0077b6", label="Divide & Conquer O(n log n)")
    ax1.set_title("Runtime Comparison (Linear Scale)", fontsize=12, fontweight="bold", color="#1d3557")
    ax1.set_xlabel("Number of Aircraft Points (N)", fontsize=10.5, fontweight="bold")
    ax1.set_ylabel("Execution Time (milliseconds)", fontsize=10.5, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(fontsize=10)

    # Plot 2: Speedup Factor Curve
    ax2.set_facecolor("#ffffff")
    ax2.plot(ns, speedups, marker="^", linewidth=2.4, color="#2b9348", label="Empirical Speedup (T_BF / T_DC)")
    ax2.axhline(y=1.0, color="#6c757d", linestyle="--", linewidth=1.2, label="Parity Baseline (1.0x)")
    ax2.set_title("Empirical Speedup of Divide & Conquer", fontsize=12, fontweight="bold", color="#1d3557")
    ax2.set_xlabel("Number of Aircraft Points (N)", fontsize=10.5, fontweight="bold")
    ax2.set_ylabel("Speedup Ratio (x times faster)", fontsize=10.5, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(fontsize=10)

    # Add data annotations on speedup plot
    for n, s in zip(ns, speedups):
        if n >= 50:
            ax2.annotate(
                f"{s:.1f}x",
                (n, s),
                textcoords="offset points",
                xytext=(0, 8),
                ha="center",
                fontsize=9,
                fontweight="bold",
                color="#1b4332"
            )

    fig.suptitle(
        "Empirical Scalability Analysis: Brute Force vs. Divide-and-Conquer\n"
        "Air-Traffic Collision Detection Benchmark (CSA0620 DAA)",
        fontsize=13.5,
        fontweight="bold",
        color="#0b132b",
        y=0.98
    )
    plt.tight_layout()

    primary_path = save_paths[0]
    for path in save_paths:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        fig.savefig(path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")

    if show_plot:
        plt.show()
    plt.close(fig)

    return primary_path


def plot_divide_conquer_strip_concept(
    save_paths: Optional[List[str]] = None,
    show_plot: bool = False
) -> str:
    """
    Renders an academic diagram illustrating the Divide-and-Conquer vertical strip
    and geometric packing proof (why at most 7 candidate comparisons are needed).
    """
    if save_paths is None:
        save_paths = [
            "screenshots/divide_conquer_strip_diagram.png",
            "results/divide_conquer_strip_diagram.png"
        ]

    fig, ax = plt.subplots(figsize=(9, 7), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f8f9fa")

    # Center dividing line at x = 0
    ax.axvline(x=0, color="#d90429", linestyle="--", linewidth=2, label="Dividing Line (x_mid)")

    # Strip boundaries [-delta, +delta]
    delta = 4.0
    ax.axvspan(-delta, delta, color="#e0f2fe", alpha=0.6, label="Vertical Strip: [x_mid - δ, x_mid + δ]")
    ax.axvline(x=-delta, color="#0284c7", linestyle=":", linewidth=1.5)
    ax.axvline(x=delta, color="#0284c7", linestyle=":", linewidth=1.5)

    # Candidate bounding box: width 2*delta, height delta
    box_y_base = 2.0
    rect = patches.Rectangle(
        (-delta, box_y_base),
        2 * delta,
        delta,
        linewidth=2,
        edgecolor="#023e8a",
        facecolor="#90e0ef",
        alpha=0.35,
        label="δ × 2δ Bounding Box (Max 8 points total, ≤ 7 neighbors)"
    )
    ax.add_patch(rect)

    # Sub-boxes (delta/2 x delta/2) illustrating packing limit
    # Left half: 4 squares
    for i in range(2):
        for j in range(2):
            sub_sq_left = patches.Rectangle(
                (-delta + i * (delta / 2), box_y_base + j * (delta / 2)),
                delta / 2,
                delta / 2,
                linewidth=1,
                edgecolor="#0077b6",
                facecolor="none",
                linestyle="--"
            )
            ax.add_patch(sub_sq_left)

            sub_sq_right = patches.Rectangle(
                (i * (delta / 2), box_y_base + j * (delta / 2)),
                delta / 2,
                delta / 2,
                linewidth=1,
                edgecolor="#0077b6",
                facecolor="none",
                linestyle="--"
            )
            ax.add_patch(sub_sq_right)

    # Reference point p_i at bottom of box
    ax.scatter([0], [box_y_base], color="#d90429", s=130, zorder=5)
    ax.annotate("Reference Point p_i", (0, box_y_base), xytext=(8, -12), textcoords="offset points", fontweight="bold", color="#d90429")

    # Annotations
    ax.annotate("Left Half Q (min dist ≥ δ)", xy=(-6, 8), fontsize=11, fontweight="bold", color="#1e3a8a", ha="center")
    ax.annotate("Right Half R (min dist ≥ δ)", xy=(6, 8), fontsize=11, fontweight="bold", color="#1e3a8a", ha="center")
    ax.annotate("Width = 2δ", xy=(0, box_y_base + delta + 0.3), fontsize=10, fontweight="bold", color="#023e8a", ha="center")
    ax.annotate("Height = δ", xy=(delta + 0.3, box_y_base + delta / 2), fontsize=10, fontweight="bold", color="#023e8a", va="center")

    ax.set_xlim(-9, 9)
    ax.set_ylim(0, 10)
    ax.set_xlabel("X Coordinate Distance relative to Dividing Line", fontsize=10.5, fontweight="bold")
    ax.set_ylabel("Y Coordinate Dimension", fontsize=10.5, fontweight="bold")
    ax.grid(True, linestyle=":", alpha=0.5)

    plt.title(
        "Geometric Packing Proof: Maximum 7 Comparisons in Vertical Strip\n"
        "Each (δ/2 × δ/2) cell has diameter δ/√2 < δ, so contains at most 1 point.",
        fontsize=11.5,
        fontweight="bold",
        color="#0f172a",
        pad=14
    )
    ax.legend(loc="upper right", fontsize=9)
    plt.tight_layout()

    primary_path = save_paths[0]
    for path in save_paths:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        fig.savefig(path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")

    if show_plot:
        plt.show()
    plt.close(fig)

    return primary_path
