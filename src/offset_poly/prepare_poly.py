"""Remove points that would give indeterminate results.

:author: Shay Hill
:created: 2023-08-17
"""

from __future__ import annotations

import itertools as it
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Sequence

_Vec2 = tuple[float, float]


def remove_coincident_adjacent_points(polyline: Sequence[_Vec2]) -> list[_Vec2]:
    """Remove zero-length segments from a polyline.

    :param polyline: polyline
    :return: polyline with zero-length segments removed
    """
    new_points: list[_Vec2] = []
    for i, point in enumerate(polyline):
        if i == 0 or point != polyline[i - 1]:
            new_points.append(point)
    return new_points


_T = TypeVar("_T")


def align_closing_points(polyline_a: Sequence[_Vec2], polyline_b: list[_T]) -> list[_T]:
    """Set b[0] to b[-1] if a[0] == a[-1].

    :param polyline_a: polyline
    :param polyline_b: polyline
    :return: polyline_b with first point set to last point if polyline_a is closed

    Match multiples of the same point.
    polyline_a -> [A, B, B, C]
    polyline_b -> [D, E, F]
    polyline_c -> [D, E, E, F]

    Wrap endpoints if polyline_a is closed.
    polyline_a -> [A, B, C, A]
    polyline_b -> [D, E, F]
    polyline_c -> [D, E, F, D]
    """
    polyline_c: list[_T] = []
    points_b = it.cycle(polyline_b)
    for i, point_a in enumerate(polyline_a):
        if i == 0:
            polyline_c.append(next(points_b))
        elif point_a == polyline_a[i - 1]:
            polyline_c.append(polyline_c[-1])
        else:
            polyline_c.append(next(points_b))
    return polyline_c
