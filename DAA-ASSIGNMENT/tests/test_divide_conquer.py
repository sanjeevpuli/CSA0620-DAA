"""
Unit Tests for Divide-and-Conquer Closest Pair Algorithm.

Course: CSA0620 - Design and Analysis of Algorithms
Module: test_divide_conquer.py
"""

import math
import unittest
from src.models import AircraftPoint, get_annexure_a_points
from src.divide_conquer import closest_pair_divide_and_conquer, RecursionTraceLogger


class TestDivideAndConquer(unittest.TestCase):
    """Test suite verifying correctness and recursion dynamics of Divide and Conquer algorithm."""

    def test_annexure_a_exact_match(self):
        """Verify that Annexure A produces closest pair P1-P6 with distance sqrt(2) approx 1.414214."""
        points = get_annexure_a_points()
        tracer = RecursionTraceLogger()
        result = closest_pair_divide_and_conquer(points, tracer)

        self.assertIsNotNone(result)
        self.assertEqual(result.pair_names, "P1-P6")
        self.assertAlmostEqual(result.distance, math.sqrt(2.0), places=6)
        self.assertAlmostEqual(result.distance, 1.41421356, places=6)
        # Verify that tracer recorded events
        self.assertGreater(len(tracer.events), 0)

    def test_zero_and_one_point(self):
        """0 or 1 point cannot form a pair and must safely return None."""
        self.assertIsNone(closest_pair_divide_and_conquer([]))
        self.assertIsNone(closest_pair_divide_and_conquer([AircraftPoint("P1", 10.0, 20.0)]))

    def test_two_points(self):
        """2 points base case."""
        pts = [
            AircraftPoint("A1", 0.0, 0.0),
            AircraftPoint("A2", 3.0, 4.0),
        ]
        res = closest_pair_divide_and_conquer(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "A1-A2")
        self.assertAlmostEqual(res.distance, 5.0, places=6)

    def test_three_points(self):
        """3 points base case."""
        pts = [
            AircraftPoint("A", 0.0, 0.0),
            AircraftPoint("B", 10.0, 0.0),
            AircraftPoint("C", 1.0, 0.0),
        ]
        res = closest_pair_divide_and_conquer(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "A-C")
        self.assertAlmostEqual(res.distance, 1.0, places=6)

    def test_closest_pair_crosses_dividing_line(self):
        """
        Crucial test: closest pair straddles the dividing line and MUST be found
        by the vertical strip combination step.
        """
        # Left half points: x in [0, 4]
        # Right half points: x in [6, 10]
        # Dividing line at x ≈ 5
        # The closest pair is L2(4.9, 10.0) and R1(5.1, 10.0), distance = 0.2
        pts = [
            AircraftPoint("L1", 1.0, 20.0),
            AircraftPoint("L2", 4.9, 10.0),
            AircraftPoint("L3", 2.0, 30.0),
            AircraftPoint("R1", 5.1, 10.0),
            AircraftPoint("R2", 8.0, 50.0),
            AircraftPoint("R3", 9.0, 70.0),
        ]
        res = closest_pair_divide_and_conquer(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "L2-R1")
        self.assertAlmostEqual(res.distance, 0.2, places=6)

    def test_closest_pair_in_left_half(self):
        """Closest pair is located entirely within the left partition."""
        pts = [
            AircraftPoint("L1", 1.0, 1.0),
            AircraftPoint("L2", 1.1, 1.0),  # dist = 0.1
            AircraftPoint("L3", 2.0, 5.0),
            AircraftPoint("R1", 20.0, 10.0),
            AircraftPoint("R2", 30.0, 20.0),
            AircraftPoint("R3", 40.0, 30.0),
        ]
        res = closest_pair_divide_and_conquer(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "L1-L2")
        self.assertAlmostEqual(res.distance, 0.1, places=6)

    def test_closest_pair_in_right_half(self):
        """Closest pair is located entirely within the right partition."""
        pts = [
            AircraftPoint("L1", 1.0, 1.0),
            AircraftPoint("L2", 5.0, 10.0),
            AircraftPoint("L3", 8.0, 15.0),
            AircraftPoint("R1", 20.0, 10.0),
            AircraftPoint("R2", 20.15, 10.0),  # dist = 0.15
            AircraftPoint("R3", 40.0, 30.0),
        ]
        res = closest_pair_divide_and_conquer(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "R1-R2")
        self.assertAlmostEqual(res.distance, 0.15, places=6)

    def test_duplicate_points(self):
        """Duplicate coordinates must yield distance 0.0."""
        pts = [
            AircraftPoint("P1", 5.0, 5.0),
            AircraftPoint("P2", 20.0, 20.0),
            AircraftPoint("P3", 5.0, 5.0),
            AircraftPoint("P4", 50.0, 80.0),
        ]
        res = closest_pair_divide_and_conquer(pts)
        self.assertIsNotNone(res)
        self.assertAlmostEqual(res.distance, 0.0, places=6)

    def test_collinear_x_coordinates(self):
        """All points on vertical line."""
        pts = [
            AircraftPoint("P1", 10.0, 1.0),
            AircraftPoint("P2", 10.0, 15.0),
            AircraftPoint("P3", 10.0, 4.0),
            AircraftPoint("P4", 10.0, 2.5),
        ]
        res = closest_pair_divide_and_conquer(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "P1-P4")
        self.assertAlmostEqual(res.distance, 1.5, places=6)

    def test_collinear_y_coordinates(self):
        """All points on horizontal line."""
        pts = [
            AircraftPoint("P1", 2.0, 100.0),
            AircraftPoint("P2", 10.0, 100.0),
            AircraftPoint("P3", 5.0, 100.0),
            AircraftPoint("P4", 2.2, 100.0),
        ]
        res = closest_pair_divide_and_conquer(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "P1-P4")
        self.assertAlmostEqual(res.distance, 0.2, places=6)

    def test_negative_coordinates(self):
        """Negative quadrants."""
        pts = [
            AircraftPoint("N1", -50.0, -30.0),
            AircraftPoint("N2", -50.5, -30.0),
            AircraftPoint("N3", 100.0, 200.0),
            AircraftPoint("N4", -10.0, 40.0),
        ]
        res = closest_pair_divide_and_conquer(pts)
        self.assertIsNotNone(res)
        self.assertEqual(res.pair_names, "N1-N2")
        self.assertAlmostEqual(res.distance, 0.5, places=6)


if __name__ == "__main__":
    unittest.main()
