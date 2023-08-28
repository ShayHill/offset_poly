# offset_poly

Move a polyline or polygon (left) by a given offset.

A counterclockwise polygon will be offset to the inside. I clockwise polygon will be offset to the outside.

## offset_polygon

~~~python
def offset_polygon(polyline: Sequence[_Vec2], offset: float) -> list[_Vec2]:
    """Offset polygon edges (to the left) by a constant amount.

    :param polyline: polyline
    :param offset: distance to offset from each edge
    :return: polygon offset by offset
    """
~~~

## offset_polyline

~~~python
def offset_polyline(polyline: Sequence[_Vec2], offset: float) -> list[_Vec2]:
    """Offset polygon edges (to the left) by a constant amount.

    :param polyline: polyline
    :param offset: distance to offset from each edge
    :return: polyline offset by offset
    """
~~~


The difference between the two is that `offset_polygon` will close the polygon if it is not already closed, whereas `offset_polyline` will leave the polyline open even if the first and last points are identical.

This package is the simplest version of polyline offsetting, it does not anticipate or account for self intersections that may come up when offsetting a polyline.

This is not nearly as sophisticated as curve offsetting, but you can use this for control polygon offsetting, which will be nearly as good in some instances.

* multiple points (knots in your control points) are preserved.
* if input[0] == input[-1], output[0] will equal output[-1]

## You may see (nan, nan) in the result.

If you pass two adjacent, opposite, parallel edges, you will get a (nan, nan) in the result. With points A -> B -> A, for instance, there is no point that would be any given distance (except 0) left of both A B and B A.

## More complex functions

There are a few more complex functions,`offset_poly_per_vert` and `offset_poly_per_edge`

~~~python
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
~~~

~~~python
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
~~~

~~~python
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
~~~

These allow a little more control, like putting in a different offset for each edge

## return value

The return value will be a GapCorner instance or a list of GapCorner instances. These have three attributes:

* .xsect -> a point at each corner where segment ab offset to the left by gap_1 intersects segment bc offset to the left by gap_2.
* .angle -> the signed ccw angle at corner abc
* .cpts -> quadratic Bezier control points for a rounded corner at abc. There is more than one way to handle this when gap_1 != gap_2, but these should give a good result in most situations.
