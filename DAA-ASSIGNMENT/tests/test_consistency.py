"""
Randomized Equivalence and Consistency Tests.

Course: CSA0620 - Design and Analysis of Algorithms
Module: test_consistency.py
"""

import math
import unittest
from src.generator import generate_random_aircraft_points
from src.brute_force import closest_pair_brute_force
from src.divide_conquer import closest_pair_divide_and_conquer


class TestConsistency(unittest.TestCase):
    """
    Validates that Divide-and-Conquer and Brute-Force produce identical results
    across diverse random distributions, scales, and seeds.
    """

    def test_random_datasets_equivalence(self):
        """Test equivalence across multiple seeds and sizes."""
        test_configs = [
            (4, 101),
            (7, 202),
            (15, 303),
            (30, 404),
            (50, 505),
            (100, 606),
            (200, 707),
            (350, 808),
        ]

        for n, seed in test_configs:
            with self.subTest(n=n, seed=seed):
                points = generate_random_aircraft_points(n, seed=seed)
                res_bf = closest_pair_brute_force(points)
                res_dc = closest_pair_divide_and_conquer(points)

                self.assertIsNotNone(res_bf, f"Brute force returned None for n={n}")
                self.assertIsNotNone(res_dc, f"Divide & conquer returned None for n={n}")

                # Assert that minimum distance computed matches within numerical tolerance
                self.assertTrue(
                    math.isclose(res_bf.distance, res_dc.distance, rel_tol=1e-8, abs_tol=1e-8),
                    f"Distance mismatch for n={n}, seed={seed}: "
                    f"BF={res_bf.distance:.8f} vs DC={res_dc.distance:.8f}"
                )

    def test_dense_clustering_equivalence(self):
        """Test equivalence in densely clustered airspace with high proximity."""
        seeds = [11, 22, 33, 44, 55]
        for seed in seeds:
            with self.subTest(seed=seed):
                # Small bounding box [0, 50] x [0, 50] forces high point density
                points = generate_random_aircraft_points(
                    n=80, seed=seed, x_min=0, x_max=50, y_min=0, y_max=50
                )
                res_bf = closest_pair_brute_force(points)
                res_dc = closest_pair_divide_and_conquer(points)

                self.assertIsNotNone(res_bf)
                self.assertIsNotNone(res_dc)
                self.assertAlmostEqual(res_bf.distance, res_dc.distance, places=6)


if __name__ == "__main__":
    unittest.main()
