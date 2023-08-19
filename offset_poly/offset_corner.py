"""Simple math helpers and offsetting one corner defined by three points.

:author: Shay Hill
:created: 2023-08-17
"""

from __future__ import annotations

import math

from offset_poly.vec2_math import _Vec2, get_signed_angle, move_along, qrotate, vsub


def miter_corner(
    pnt_a: _Vec2, pnt_b: _Vec2, pnt_c: _Vec2, gap_1: float, gap_2: float | None = None
) -> tuple[float, float]:
    """Offset a corner (to the right) defined by three points.

    :param pnt_a: previous  point
    :param pnt_b: corner point
    :param pnt_c: next point
    :param gap_1: distance to offset from vec12
    :param gap_2: optional distance to offset from vec23. If not given, gap_1 is used
    :return: the unique point gap_1 distance from ab and gap_2 distance from bc
    :raise ValueError: if angle abc is zero and gap_1 != gap_2
    """
    if gap_2 is None:
        gap_2 = gap_1

    if gap_1 is 0 and gap_2 is 0:
        return pnt_b

    vec12 = vsub(pnt_b, pnt_a)
    vec23 = vsub(pnt_c, pnt_b)
    angle = get_signed_angle(vec12, vec23)

    if math.isclose(angle, 0, abs_tol=1e-6):
        if gap_1 != gap_2:
            except_msg = "gap_1 and gap_2 must be equal when angle is zero"
            raise ValueError(except_msg)
        return move_along(pnt_b, qrotate(vec12, 1), gap_1)

    sin_angle = math.sin(angle)
    if math.isclose(sin_angle, 0, abs_tol=1e-6):
        return math.nan, math.nan

    intermediate = move_along(pnt_b, vec23, gap_1 / sin_angle)
    return move_along(intermediate, vec12, -(gap_2 or 0) / sin_angle)
