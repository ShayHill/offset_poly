"""Import fuctions into the package namespace.

:author: Shay Hill
:created: 2023-08-19
"""

from offset_poly.offset import (
    offset_poly_per_edge,
    offset_poly_per_vert,
    offset_polygon,
    offset_polyline,
)
from offset_poly.offset_corner import miter_corner

__all__ = [
    "miter_corner",
    "offset_polyline",
    "offset_polygon",
    "offset_poly_per_vert",
    "offset_poly_per_edge",
]
