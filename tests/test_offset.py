"""Test functions in offset.py.

:author: Shay Hill
:created: 2023-08-19
"""


from offset_poly.offset import offset_polygon, offset_polyline


class TestOffsetPolyline:
    def test_three_sides(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        assert offset_polyline(polyline, 1) == [
            (0.0, 1.0),
            (4.0, 1.0),
            (4.0, 4.0),
            (0.0, 4.0),
        ]

    def test_three_sides_left(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        assert offset_polyline(polyline, -1) == [
            (0.0, -1.0),
            (6.0, -1.0),
            (6.0, 6.0),
            (0.0, 6.0),
        ]

    def test_beg_matches_end(self):
        """Treated as open even when begin matches end."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
        assert offset_polyline(polyline, 1) == [
            (0.0, 1.0),
            (4.0, 1.0),
            (4.0, 4.0),
            (1.0, 4.0),
            (1.0, 0.0),
        ]

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
        assert offset_polyline(polyline, 1) == [
            (0.0, 1.0),
            (0.0, 1.0),
            (4.0, 1.0),
            (4.0, 1.0),
            (4.0, 4.0),
            (4.0, 4.0),
            (1.0, 4.0),
            (1.0, 4.0),
            (1.0, 4.0),
            (1.0, 4.0),
            (1.0, 0.0),
            (1.0, 0.0),
        ]


class TestOffsetPolygon:
    def test_ccw(self):
        """When polygon in ccw, offset points are inside."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        assert offset_polygon(polyline, 1) == [
            (1, 1),
            (4, 1),
            (4, 4),
            (1, 4),
        ]

    def test_cw(self):
        """When polygon is cw, offset points are outside."""
        polyline = [(0, 5), (5, 5), (5, 0), (0, 0)]
        assert offset_polygon(polyline, 1) == [
            (-1, 6),
            (6, 6),
            (6, -1),
            (-1, -1),
        ]

    def test_three_sides_left(self):
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5)]
        assert offset_polygon(polyline, -1) == [
            (-1, -1),
            (6, -1),
            (6, 6),
            (-1, 6),
        ]

    def test_beg_matches_end(self):
        """Treated as open even when begin matches end. Duplicate end point retained."""
        polyline = [(0, 0), (5, 0), (5, 5), (0, 5), (0, 0)]
        assert offset_polygon(polyline, 1) == [
            (1, 1),
            (4, 1),
            (4, 4),
            (1, 4),
            (1, 1),
        ]

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
        assert offset_polygon(polyline, 1) == [
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
