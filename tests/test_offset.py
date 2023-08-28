"""Test functions in offset.py.

:author: Shay Hill
:created: 2023-08-19
"""
import math

from offset_poly.offset import offset_polygon, offset_polyline


def _is_vec_close(vec_a: tuple[float, float], vec_b: tuple[float, float]) -> bool:
    """Return True if vec_a and vec_b are close enough to be equal."""
    return math.isclose(vec_a[0], vec_b[0]) and math.isclose(vec_a[1], vec_b[1])


def _is_cpts_close(
    cpts_a: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
    cpts_b: tuple[tuple[float, float], tuple[float, float], tuple[float, float]],
) -> bool:
    """Return True if cpts_a and cpts_b are close enough to be equal."""
    return (
        _is_vec_close(cpts_a[0], cpts_b[0])
        and _is_vec_close(cpts_a[1], cpts_b[1])
        and _is_vec_close(cpts_a[2], cpts_b[2])
    )


class TestOffsetPolyline:
    def test_three_sides_xsects(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polyline(polyline, 1)
        expect_xsects = [(0, 1), (4, 1), (4, 4), (0, 4)]
        assert all([_is_vec_close(r.xsect, e) for r, e in zip(result, expect_xsects)])

    def test_three_sides_angles(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polyline(polyline, 1)
        expect_angles = [0, math.pi / 2, math.pi / 2, 0]
        assert all([math.isclose(r.angle, e) for r, e in zip(result, expect_angles)])

    def test_three_sides_cpts(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polyline(polyline, 1)
        expect_cpts = [
            ((0, 0), (0, 0), (0, 0)),
            ((4, 0), (5, 0), (5, 1)),
            ((5, 4), (5, 5), (4, 5)),
            ((0, 5), (0, 5), (0, 5)),
        ]
        assert all([_is_cpts_close(r.cpts, e) for r, e in zip(result, expect_cpts)])

    def test_three_sides_left_xsects(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polyline(polyline, -1)
        expect_xsects = [(0, -1), (6, -1), (6, 6), (0, 6)]
        assert all([_is_vec_close(r.xsect, e) for r, e in zip(result, expect_xsects)])

    def test_three_sides_left_angles(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polyline(polyline, -1)
        expect_angles = [0, math.pi / 2, math.pi / 2, 0]
        assert all([math.isclose(r.angle, e) for r, e in zip(result, expect_angles)])

    def test_three_sides_left_cpts(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polyline(polyline, -1)
        expect_cpts = [
            ((0, 0), (0, 0), (0, 0)),
            ((5, 0), (5, 0), (5, 0)),
            ((5, 5), (5, 5), (5, 5)),
            ((0, 5), (0, 5), (0, 5)),
        ]
        assert all([_is_cpts_close(r.cpts, e) for r, e in zip(result, expect_cpts)])

    def test_beg_matches_end_xsects(self):
        """Treated as open even when begin matches end."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
        result = offset_polygon(polyline, 1)
        expect_xsects = [(1, 1), (4, 1), (4, 4), (1, 4), (1, 1)]
        assert all([_is_vec_close(r.xsect, e) for r, e in zip(result, expect_xsects)])

    def test_beg_matches_end_angles(self):
        """Treated as open even when begin matches end."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
        result = offset_polygon(polyline, 1)
        expect_angles = [
            math.pi / 2,
            math.pi / 2,
            math.pi / 2,
            math.pi / 2,
            math.pi / 2,
        ]
        assert all([math.isclose(r.angle, e) for r, e in zip(result, expect_angles)])

    def test_beg_matches_end_cpts(self):
        """Treated as open even when begin matches end."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
        result = offset_polygon(polyline, 1)
        expect_cpts = [
            ((0, 1), (0, 0), (1, 0)),
            ((4, 0), (5, 0), (5, 1)),
            ((5, 4), (5, 5), (4, 5)),
            ((1, 5), (0, 5), (0, 4)),
            ((0, 1), (0, 0), (1, 0)),
        ]
        assert all([_is_cpts_close(r.cpts, e) for r, e in zip(result, expect_cpts)])

    def test_multiples_retained(self):
        """Keep multiple points."""
        polyline = [
            (0, 0),
            (0, 0),
            (5, 0),
            (5, 0),
            (5, 5),
            (5, 5),
            (0, 5),
            (0, 5),
            (0, 5),
            (0, 5),
            (0, 0),
            (0, 0),
        ]
        assert [x.xsect for x in offset_polyline(polyline, 1)] == [
            (0, 1),
            (0, 1),
            (4, 1),
            (4, 1),
            (4, 4),
            (4, 4),
            (1, 4),
            (1, 4),
            (1, 4),
            (1, 4),
            (1, 0),
            (1, 0),
        ]


class TestOffsetPolygon:
    def test_ccw_xsects(self):
        """When polygon in ccw, offset points are inside."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polygon(polyline, 1)
        expect_xsects = [(1, 1), (4, 1), (4, 4), (1, 4)]
        assert all([_is_vec_close(r.xsect, e) for r, e in zip(result, expect_xsects)])

    def test_ccw_angles(self):
        """When polygon in ccw, offset points are inside."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polygon(polyline, 1)
        expect_angles = [
            math.pi / 2,
            math.pi / 2,
            math.pi / 2,
            math.pi / 2,
        ]
        assert all([math.isclose(r.angle, e) for r, e in zip(result, expect_angles)])

    def test_ccw_cpts(self):
        """When polygon in ccw, offset points are inside."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polygon(polyline, 1)
        expect_cpts = [
            ((0, 1), (0, 0), (1, 0)),
            ((4, 0), (5, 0), (5, 1)),
            ((5, 4), (5, 5), (4, 5)),
            ((1, 5), (0, 5), (0, 4)),
        ]
        assert all([_is_cpts_close(r.cpts, e) for r, e in zip(result, expect_cpts)])

    def test_cw_xsects(self):
        """When polygon is cw, offset points are outside."""
        polyline = [(0, 5), (5, 5), (5, 0), (0, 0)]
        result = offset_polygon(polyline, 1)
        expect_xsects = [(-1, 6), (6, 6), (6, -1), (-1, -1)]
        assert all([_is_vec_close(r.xsect, e) for r, e in zip(result, expect_xsects)])

    def test_cw_angles(self):
        """When polygon is cw, offset points are outside."""
        polyline = [(0, 5), (5, 5), (5, 0), (0, 0)]
        result = offset_polygon(polyline, 1)
        expect_angles = [
            -math.pi / 2,
            -math.pi / 2,
            -math.pi / 2,
            -math.pi / 2,
        ]
        assert all([math.isclose(r.angle, e) for r, e in zip(result, expect_angles)])

    def test_cw_cpts(self):
        """When polygon is cw, offset points are outside."""
        polyline = [(0, 5), (5, 5), (5, 0), (0, 0)]
        result = offset_polygon(polyline, 1)
        expect_cpts = [
            ((0, 4), (0, 5), (1, 5)),
            ((4, 5), (5, 5), (5, 4)),
            ((5, 1), (5, 0), (4, 0)),
            ((1, 0), (0, 0), (0, 1)),
        ]
        assert all([_is_cpts_close(r.cpts, e) for r, e in zip(result, expect_cpts)])

    def test_three_sides_left_xsects(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polygon(polyline, -1)
        expect_xsects = [(-1, -1), (6, -1), (6, 6), (-1, 6)]
        assert all([_is_vec_close(r.xsect, e) for r, e in zip(result, expect_xsects)])

    def test_three_sides_left_angles(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polygon(polyline, -1)
        expect_angles = [
            math.pi / 2,
            math.pi / 2,
            math.pi / 2,
            math.pi / 2,
        ]
        assert all([math.isclose(r.angle, e) for r, e in zip(result, expect_angles)])

    def test_three_sides_left_cpts(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        result = offset_polygon(polyline, -1)
        expect_cpts = [
            ((0, 0), (0, 0), (0, 0)),
            ((5, 0), (5, 0), (5, 0)),
            ((5, 5), (5, 5), (5, 5)),
            ((0, 5), (0, 5), (0, 5)),
        ]
        assert all([_is_cpts_close(r.cpts, e) for r, e in zip(result, expect_cpts)])

    def test_beg_matches_end_xsects(self):
        """Treated as open even when begin matches end. Duplicate end point retained."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
        result = offset_polygon(polyline, 1)
        expect_xsects = [(1, 1), (4, 1), (4, 4), (1, 4), (1, 1)]
        assert all([_is_vec_close(r.xsect, e) for r, e in zip(result, expect_xsects)])

    def test_beg_matches_end_angles(self):
        """Treated as open even when begin matches end. Duplicate end point retained."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
        result = offset_polygon(polyline, 1)
        expect_angles = [
            math.pi / 2,
            math.pi / 2,
            math.pi / 2,
            math.pi / 2,
            math.pi / 2,
        ]
        assert all([math.isclose(r.angle, e) for r, e in zip(result, expect_angles)])

    def test_beg_matches_end_cpts(self):
        """Treated as open even when begin matches end. Duplicate end point retained."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
        result = offset_polygon(polyline, 1)
        expect_cpts = [
            ((0, 1), (0, 0), (1, 0)),
            ((4, 0), (5, 0), (5, 1)),
            ((5, 4), (5, 5), (4, 5)),
            ((1, 5), (0, 5), (0, 4)),
            ((0, 1), (0, 0), (1, 0)),
        ]
        assert all([_is_cpts_close(r.cpts, e) for r, e in zip(result, expect_cpts)])

    def test_multiples_retained(self):
        """Keep multiple points."""
        polyline = [
            (0, 0),
            (0, 0),
            (5, 0),
            (5, 0),
            (5, 5),
            (5, 5),
            (0, 5),
            (0, 5),
            (0, 5),
            (0, 5),
            (0, 0),
            (0, 0),
        ]
        assert [x.xsect for x in offset_polygon(polyline, 1)] == [
            (1, 1),
            (1, 1),
            (4, 1),
            (4, 1),
            (4, 4),
            (4, 4),
            (1, 4),
            (1, 4),
            (1, 4),
            (1, 4),
            (1, 1),
            (1, 1),
        ]
