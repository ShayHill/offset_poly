"""Offset a polyline to the right.

:author: Shay Hill
:created: 2023-08-17
"""

from __future__ import annotations

import enum
import itertools as it
from typing import TYPE_CHECKING

from vec2_math import vadd, vsub

from offset_poly.offset_corner import GapCorner, gap_corner
from offset_poly.prepare_poly import (
    align_closing_points,
    remove_coincident_adjacent_points,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

_Vec2 = tuple[float, float]

_MIN_PTS_FOR_POLYGON = 3
_MIN_PTS_FOR_POLYLINE = 2


class PolyType(enum.Enum):
    """Polyline types."""

    POLYLINE = enum.auto()
    POLYGON = enum.auto()


def _wrap_polygon(polyline: Sequence[_Vec2]) -> list[_Vec2]:
    """Wrap a polyline around to the beginning if it is closed.

    :param polyline: polyline
    :return: polyline with last point repeated if it is closed

    From A, B, C, A to C, A, B, C, A
    """
    points = list(polyline)
    if points[0] == points[-1]:
        points = points[:-1]
    return points[-1:] + points + points[:1]


def _anchor_polyline(polyline: Sequence[_Vec2]) -> list[_Vec2]:
    """Add edges to endpoints of an open polyline.

    :param polyline: polyline
    :return: polyline with extended edges at the beginning and end

        A ΓÇö B
            |
            C

    becomes

    A`ΓÇö A ΓÇö B
            |
            C
            |
            C`

    From A, B, C to (A + (A - B)), A, B, C, (C - (B - C))
    """
    pnt_beg = vadd(polyline[0], vsub(*polyline[:2]))
    pnt_end = vsub(polyline[-1], vsub(*polyline[-2:]))
    return [pnt_beg, *list(polyline), pnt_end]


def offset_poly_per_vert(
    polyline: Sequence[_Vec2],
    vert_offsets: Iterable[tuple[float, float]],
    poly_type: PolyType,
) -> list[GapCorner]:
    """Offset each corner of a polyline or polygon.

    :param polyline: polyline
    :param vert_offsets: iterable of (gap_1, gap_2) tuples. One pair per corner.
    :param poly_type: PolyType.POLYGON or PolyType.POLYLINE
    :return: polyline offset by vert_offsets
    :raise ValueError: if fewer than three points are given for a polygon
    :raise ValueError: if fewer than two points are given for a polyline

    This is the engine of the offset_polyline and offset_polygon
    functions. You can use it directly, but it's going to be tricky if
    you have zero-length segments or closed points. These points will
    be removed before the gaps are applied, so you'll have to pass
    exactly enough for gap pairs for the segments that are retained.
    """
    points = remove_coincident_adjacent_points(polyline)

    if poly_type == PolyType.POLYGON:
        if len(points) < _MIN_PTS_FOR_POLYGON:
            msg = "at least three unique points required for a polygon"
            raise ValueError(msg)
        points = _wrap_polygon(points)
    elif poly_type == PolyType.POLYLINE:
        if len(points) < _MIN_PTS_FOR_POLYLINE:
            msg = "at least two unique points required for a polyline"
            raise ValueError(msg)
        points = _anchor_polyline(points)
    else:
        msg = "poly_type must be PolyType.POLYGON or PolyType.POLYLINE"
        raise ValueError(msg)

    offset_points: list[GapCorner] = []
    abcs = list(zip(points, points[1:], points[2:]))
    gaps = it.cycle(vert_offsets or [(0, 0)])

    for i, (pnt_a, pnt_b, pnt_c) in enumerate(abcs):
        gap_1, gap_2 = next(gaps)
        if poly_type == PolyType.POLYLINE and i == 0:
            offset_points.append(gap_corner(pnt_a, pnt_b, pnt_c, gap_2))
            continue
        if poly_type == PolyType.POLYLINE and i == len(abcs) - 1:
            offset_points.append(gap_corner(pnt_a, pnt_b, pnt_c, gap_1))
            continue
        offset_points.append(gap_corner(pnt_a, pnt_b, pnt_c, gap_1, gap_2))

    return align_closing_points(polyline, offset_points)


def offset_poly_per_edge(
    polyline: Sequence[_Vec2], edge_offsets: Iterable[float], poly_type: PolyType
) -> list[GapCorner]:
    """Offset each edge of a polyline or polygon.

    :param polyline: polyline
    :param edge_offsets: iterable of offsets. One per edge.
    :param poly_type: PolyType.POLYGON or PolyType.POLYLINE
    :return: polyline offset by edge_offsets

    This function allows each edge of a polygon or polyline to be offset by
    a different amount. You will end up with a ValueError in gap_corner
    if you try to offset consecutive, parallel edges by different amounts.
    """
    next_edges = [x for x, _ in zip(edge_offsets, polyline)]
    prev_edges = [next_edges[-1], *next_edges[:-1]]
    return offset_poly_per_vert(polyline, zip(prev_edges, next_edges), poly_type)


def offset_polyline(polyline: Sequence[_Vec2], offset: float) -> list[GapCorner]:
    """Offset polygon edges (to the left) by a constant amount.

    :param polyline: polyline
    :param offset: distance to offset from each edge
    :return: polyline offset by offset
    """
    return offset_poly_per_edge(polyline, it.cycle([offset]), PolyType.POLYLINE)


def offset_polygon(polyline: Sequence[_Vec2], offset: float) -> list[GapCorner]:
    """Offset polygon edges (to the left) by a constant amount.

    :param polyline: polyline
    :param offset: distance to offset from each edge
    :return: polygon offset by offset
    """
    return offset_poly_per_edge(polyline, it.cycle([offset]), PolyType.POLYGON)
