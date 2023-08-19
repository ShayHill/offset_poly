"""Test the miter corner function.

:author: Shay Hill
:created: 2023-08-17
"""
import math
import pytest

from offset_poly.offset_corner import (
    miter_corner,
)


class TestMiterCorner:
    def test_right_turn(self):
        """point is on the outside for a right turn"""
        assert miter_corner((0, 0), (0, 2), (2, 2), 1, 1) == (-1, 3)

    def test_gap2_not_given(self):
        """If gap_2 is not given, it defaults to gap_1."""
        assert miter_corner((0, 0), (0, 2), (2, 2), 1, None) == (-1, 3)

    def test_gap2_ne_gap1(self):
        """Gaps can be different."""
        assert miter_corner((0, 0), (0, 2), (2, 2), 1, 2) == (-1, 4)

    def test_gap1_zero(self):
        """If gap_1 is zero, result lies on vec12."""
        assert miter_corner((0, 0), (0, 2), (2, 2), 0, 1) == (0, 3)

    def test_gap2_zero(self):
        """If gap_2 is zero, result lies on vec23."""
        assert miter_corner((0, 0), (0, 2), (2, 2), 1, 0) == (-1, 2)

    def test_both_gaps_zero(self):
        """If both gaps are zero, result is v2."""
        assert miter_corner((0, 0), (0, 2), (2, 2), 0, 0) == (0, 2)

    def test_left_turn(self):
        """point is on the inside of a left turn"""
        assert miter_corner((0, 0), (0, 2), (-2, 2), 1, 1) == (-1, 1)

    def test_straight(self):
        assert miter_corner((0, 0), (0, 2), (0, 4), 1, 1) == (-1, 2)

    def test_straight_zero_gap(self):
        """If gap is zero, result is v2."""
        assert miter_corner((0, 0), (0, 2), (0, 4), 0, 0) == (0, 2)

    def test_zero_angle_with_different_gaps(self):
        """Raise a ValueError if the angle is zero and the gaps are different."""
        with pytest.raises(ValueError) as excinfo:
            miter_corner((0, 0), (0, 2), (0, 4), 1, 2)
        assert "gap_1 and gap_2 must be equal when angle is zero" in str(excinfo.value)

    def test_pi_angle(self):
        """Return (nan, nan) if miter level would be infinite"""
        nan_nan = miter_corner((0, 0), (0, 2), (0, 1), 1)
        assert math.isnan(nan_nan[0])
        assert math.isnan(nan_nan[1])
