"""Test functions in vec2_math module.

:author: Shay Hill
:created: 2023-08-19
"""
import math

from offset_poly.vec2_math import get_signed_angle, qrotate


class TestGetSignedAngle:
    def test_quadrant_1(self):
        v1 = (1, 0)
        v2 = (0, 1)
        assert get_signed_angle(v1, v2) == math.pi / 2

    def test_quadrant_12(self):
        v1 = (1, 1)
        v2 = (-1, 1)
        assert get_signed_angle(v1, v2) == math.pi / 2

    def test_x_axis(self):
        v1 = (1, 0)
        v2 = (-1, 0)
        assert get_signed_angle(v1, v2) == math.pi

    def test_y_axis(self):
        v1 = (0, 1)
        v2 = (0, -1)
        assert get_signed_angle(v1, v2) == math.pi

    def test_equal(self):
        v1 = (0, 1)
        v2 = (0, 1)
        assert get_signed_angle(v1, v2) == 0

    def test_parallel(self):
        v1 = (0, 1)
        v2 = (0, 2)
        assert get_signed_angle(v1, v2) == 0

    def test_quadrant_4(self):
        v1 = (1, 0)
        v2 = (0, -1)
        assert get_signed_angle(v1, v2) == -math.pi / 2

    def test_one_zero_vector(self):
        v1 = (1, 0)
        v2 = (0, 0)
        assert get_signed_angle(v1, v2) == 0

    def test_two_zero_vectors(self):
        v1 = (0, 0)
        v2 = (0, 0)
        assert get_signed_angle(v1, v2) == 0


class TestQrotate:
    def test_zero_quadrants(self):
        v = (2, 3)
        quadrants = 0
        assert qrotate(v, quadrants) == v

    def test_one_quadrant(self):
        v = (2, 3)
        quadrants = 1
        expected_result = (-3, 2)
        assert qrotate(v, quadrants) == expected_result

    def test_two_quadrants(self):
        v = (2, 3)
        quadrants = 2
        expected_result = (-2, -3)
        assert qrotate(v, quadrants) == expected_result

    def test_three_quadrants(self):
        v = (2, 3)
        quadrants = 3
        expected_result = (3, -2)
        assert qrotate(v, quadrants) == expected_result

    def test_negative_quadrants(self):
        vec = (1, 2)
        result = qrotate(vec, -1)
        assert result == (2, -1)

    def test_multiple_quadrants(self):
        vec = (1, 2)
        result = qrotate(vec, 3)
        assert result == (2, -1)
