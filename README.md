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