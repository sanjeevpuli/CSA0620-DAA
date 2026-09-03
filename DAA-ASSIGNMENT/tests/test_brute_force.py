"""
Unit Tests for Brute-Force Closest Pair Algorithm.

Course: CSA0620 - Design and Analysis of Algorithms
Module: test_brute_force.py
"""

import math
import unittest
from src.models import AircraftPoint, get_annexure_a_points
from src.brute_force import closest_pair_brute_force, compute_all_pairwise_distances


class TestBruteForce(unittest.TestCase):
    """Test suite verifying correctness and edge-case handling of Brute Force algorithm."""

    def test_annexure_a_exact_match(self):
        """Verify that Annexure A produces closest pair P1-P6 with distance sqrt(2) approx 1.414214."""
        points = get_annexure_a_points()
        result = closest_pair_brute_force(points)

        self.assertIsNotNone(result)
        self.assertEqual(result.pair_names, "P1-P6")
        self.assertAlmostEqual(result.distance, math.sqrt(2.0), places=6)
        self.assertAlmostEqual(result.distance, 1.41421356, places=6)
        # For n=7, comparisons should be 7*6/2 = 21
        self.assertEqual(result.comparisons_count, 21)

    def test_zero_and_one_point(self):
        """0 or 1 point cannot form a pair and must safely return None."""
        self.assertIsNone(closest_pair_brute_force([]))
        self.assertIsNone(closest_pair_brute_force([AircraftPoint("P1", 10.0, 20.0)]))

    def test_two_points(self):
        """2 points should return direct distance with 1 comparison."""
        pts = [
            AircraftPoint("A1", 0.0, 0.0),
            AircraftPoint("A2", 3.0, 4.0),
        ]
        res = closest_pair_brute_force(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "A1-A2")
        self.assertAlmostEqual(res.distance, 5.0, places=6)
        self.assertEqual(res.comparisons_count, 1)

    def test_three_points(self):
        """3 points should evaluate all 3 pairs and return minimum."""
        pts = [
            AircraftPoint("A", 0.0, 0.0),
            AircraftPoint("B", 10.0, 0.0),
            AircraftPoint("C", 1.0, 0.0),
        ]
        res = closest_pair_brute_force(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "A-C")
        self.assertAlmostEqual(res.distance, 1.0, places=6)
        self.assertEqual(res.comparisons_count, 3)

    def test_duplicate_points(self):
        """Duplicate coordinates must yield distance 0.0."""
        pts = [
            AircraftPoint("P1", 5.0, 5.0),
            AircraftPoint("P2", 20.0, 20.0),
            AircraftPoint("P3", 5.0, 5.0),
        ]
        res = closest_pair_brute_force(pts)
        self.assertIsNotNone(res)
        self.assertAlmostEqual(res.distance, 0.0, places=6)

    def test_collinear_x_coordinates(self):
        """Points sharing identical X coordinates (vertical line)."""
        pts = [
            AircraftPoint("P1", 10.0, 1.0),
            AircraftPoint("P2", 10.0, 15.0),
            AircraftPoint("P3", 10.0, 4.0),
            AircraftPoint("P4", 10.0, 2.5),
        ]
        # P1(10, 1.0) and P4(10, 2.5) have distance 1.5
        res = closest_pair_brute_force(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "P1-P4")
        self.assertAlmostEqual(res.distance, 1.5, places=6)

    def test_collinear_y_coordinates(self):
        """Points sharing identical Y coordinates (horizontal line)."""
        pts = [
            AircraftPoint("P1", 2.0, 100.0),
            AircraftPoint("P2", 10.0, 100.0),
            AircraftPoint("P3", 5.0, 100.0),
            AircraftPoint("P4", 2.2, 100.0),
        ]
        # P1(2.0, 100) and P4(2.2, 100) have distance 0.2
        res = closest_pair_brute_force(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "P1-P4")
        self.assertAlmostEqual(res.distance, 0.2, places=6)

    def test_negative_coordinates(self):
        """Points with negative quadrants."""
        pts = [
            AircraftPoint("N1", -50.0, -30.0),
            AircraftPoint("N2", -50.5, -30.0),
            AircraftPoint("N3", 100.0, 200.0),
        ]
        res = closest_pair_brute_force(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "N1-N2")
        self.assertAlmostEqual(res.distance, 0.5, places=6)

    def test_pairwise_table_annexure_a_count(self):
        """Verify that Annexure A produces exactly 21 pairwise records."""
        points = get_annexure_a_points()
        records = compute_all_pairwise_distances(points)
        self.assertEqual(len(records), 21)
        min_recs = [r for r in records if r["is_minimum"]]
        self.assertEqual(len(min_recs), 1)
        self.assertEqual(min_recs[0]["pair_name"], "P1-P6")


if __name__ == "__main__":
    unittest.main()
