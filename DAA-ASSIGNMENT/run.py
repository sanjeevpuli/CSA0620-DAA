#!/usr/bin/env python3
"""
Root entry point for CSA0620 DAA Assignment:
"Efficient Nearest-Neighbour Detection for Air-Traffic Collision Alerts (Divide-and-Conquer)"

Usage:
    python run.py                # Launches interactive menu
    python run.py --all          # Runs full automated pipeline
    python run.py --annexure-a   # Runs Annexure A analysis
    python run.py --table        # Displays 21-pair distance table
    python run.py --trace        # Displays D&C recursion trace
    python run.py --benchmark    # Runs empirical performance benchmark
    python run.py --test         # Executes test suite
    python run.py --visualize    # Generates high-resolution figures
"""

import sys
import os

# Ensure proper encoding on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    main()
