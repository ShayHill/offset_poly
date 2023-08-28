"""Simple math helpers and offsetting one corner defined by three points.

:author: Shay Hill
:created: 2023-08-17
"""

from __future__ import annotations

import dataclasses
import math

import vec2_math as v2

_Vec = tuple[float, float]
_Seg = tuple[_Vec, _Vec]


def _get_closest_point_on_seg(seg: _Seg, point: _Vec) -> _Vec:
    """Find the closest point on a line segment to a point.

    :param seg: line segment define by two points
    :param point: point
    :return: closest point on the line segment to the point
    """
    seg_vec = v2.vsub(seg[1], seg[0])
    point_vec = v2.vsub(point, seg[0])
    seg_norm = v2.get_norm(seg_vec)
    seg_unit = v2.vscale(seg_vec, 1 / seg_norm)
    proj_norm = v2.dot(point_vec, seg_unit)
    proj_norm = max(0, min(seg_norm, proj_norm))
    return v2.vadd(seg[0], v2.vscale(seg_unit, proj_norm))


def _offset_seg(seg: _Seg, gap: float) -> _Seg:
    """Offset a line segment by a gap.

    :param seg: line segment
    :param gap: gap to offset by
    :return: line segment moved gap distance to the left
    """
    vec_left = v2.set_norm(v2.qrotate(v2.vsub(seg[1], seg[0]), 1), gap)
    return v2.vadd(seg[0], vec_left), v2.vadd(seg[1], vec_left)


@dataclasses.dataclass
class GapCorner:
    """Offset a corner defined by three points.

    :param pnt_a: first point
    :param pnt_b: second point
    :param pnt_c: third point
    :param gap_1: gap to offset pnt_a and pnt_b by
    :param gap_2: gap to offset pnt_b and pnt_c by

    Calculate intersection point of a line offset gap_1 from ab and a line offset
    gap_2 from bc.

    Calculate quadratic Bezier control points for a rounded corner at abc
    """

    pnt_a: _Vec
    pnt_b: _Vec
    pnt_c: _Vec
    gap_1: float
    gap_2: float
    angle: float = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        """Calculate the angle at b."""
        vec_ab = v2.vsub(self.pnt_b, self.pnt_a)
        vec_bc = v2.vsub(self.pnt_c, self.pnt_b)
        self.angle = v2.get_signed_angle(vec_ab, vec_bc)

    @property
    def _ab_left(self) -> _Seg:
        """Return segment ab offset to the left."""
        return _offset_seg((self.pnt_a, self.pnt_b), self.gap_1)

    @property
    def _ab_right(self) -> _Seg:
        """Return segment ab offset to the right."""
        return _offset_seg((self.pnt_a, self.pnt_b), -self.gap_1)

    @property
    def _bc_left(self) -> _Seg:
        """Return segment bc offset to the left."""
        return _offset_seg((self.pnt_b, self.pnt_c), self.gap_2 or 0)

    @property
    def _bc_right(self) -> _Seg:
        """Return segment bc offset to the right."""
        return _offset_seg((self.pnt_b, self.pnt_c), -self.gap_2 or 0)

    @property
    def _is_straight(self) -> bool:
        """Return True if b (almost) lies on ac."""
        return math.isclose(self.angle, 0, abs_tol=1e-6)

    @property
    def _is_degenerate(self) -> bool:
        """Return True if corner forms a zero-degree angle."""
        return math.isclose(self.angle % (math.pi * 2), math.pi, abs_tol=1e-6)

    def _get_xsect(self, seg_1: _Seg, seg_2: _Seg) -> _Vec:
        """Return the intersection of two offset segments.

        :raise ValueError: if segments do not intersect (straight line with two
            different gaps)
        :raise RuntimeError: if segments not parallel but we've failed to find an
            intersection.
        """
        if self._is_degenerate:
            return (math.nan, math.nan)
        if self._is_straight:
            if self.gap_1 != self.gap_2:
                msg = "gaps must be equal for straight corners"
                raise ValueError(msg)
            return seg_1[1]
        xsect_ = v2.get_line_xsect(seg_1, seg_2)
        if xsect_ is None:
            msg = "segments are not parallel but no intersection found"
            raise RuntimeError(msg)
        return xsect_

    @property
    def xsect(self) -> _Vec:
        """The intersection of left-offset segments ab and bc."""
        return self._get_xsect(self._ab_left, self._bc_left)

    @property
    def _xsect_right(self) -> _Vec:
        """The intersection of right-offset segments ab and bc."""
        return self._get_xsect(self._ab_right, self._bc_right)

    def _get_cp(self, seg: _Seg) -> _Vec:
        """Return closest point on seg to xsect."""
        if self._is_straight or self._is_degenerate:
            return self.pnt_b
        if self.angle > 0:
            return _get_closest_point_on_seg(seg, self.xsect)
        return _get_closest_point_on_seg(seg, self._xsect_right)

    @property
    def _cp_a(self) -> _Vec:
        """Return closest point on ab to xsect."""
        return self._get_cp((self.pnt_a, self.pnt_b))

    @property
    def _cp_c(self) -> _Vec:
        """Return closest point on bc to xsect."""
        return self._get_cp((self.pnt_b, self.pnt_c))

    @property
    def cpts(self) -> tuple[_Vec, _Vec, _Vec]:
        """Return control points for a Bezier curve at the corner."""
        return self._cp_a, self.pnt_b, self._cp_c


def gap_corner(
    pnt_a: _Vec, pnt_b: _Vec, pnt_c: _Vec, gap_1: float, gap_2: float | None = None
) -> GapCorner:
    """Offset a corner (to the left) defined by three points.

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
    return GapCorner(pnt_a, pnt_b, pnt_c, gap_1, gap_2)
