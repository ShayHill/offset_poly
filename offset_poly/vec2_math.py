"""Simple operations on vectors. All return 2tuples.

:author: Shay Hill
:created: 2023-08-19
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Union

_Vec2 = Union[tuple[float, float], Sequence[float]]


def det(vec_a: _Vec2, vec_b: _Vec2) -> float:
    """Return determinant of a 2x2 matrix.

    :param vec_a: 2d vector
    :param vec_b: 2d vector
    :return: determinant of the 2x2 matrix where
        vec_a is the first row and vec_b is the second
    """
    return vec_a[0] * vec_b[1] - vec_a[1] * vec_b[0]


def dot(vec_a: _Vec2, vec_b: _Vec2) -> float:
    """Return dot product of two 2d vectors.

    :param vec_a: 2d vector
    :param vec_b: 2d vector
    :return: dot product of the vectors
    """
    return vec_a[0] * vec_b[0] + vec_a[1] * vec_b[1]


def get_signed_angle(vec_a: _Vec2, vec_b: _Vec2) -> float:
    """Calculate the signed angle at a corner defined by two vectors.

    :param vec_a: 2d vector
    :param vec_b: 2d vector
    :return: signed angle between the vectors

    Counterclockwise angles will be positive
    Clockwise angles will be negative
    """
    return math.atan2(det(vec_a, vec_b), dot(vec_a, vec_b))


def get_norm(vec: _Vec2) -> float:
    """Return Euclidean norm of a 2d vector.

    :param vec: 2d vector
    :return: Euclidean norm of the vector
    """
    return math.sqrt(vec[0] ** 2 + vec[1] ** 2)


def set_norm(vec: _Vec2, norm: float = 1) -> tuple[float, float]:
    """Scale a 2d vector to a given magnitude.

    :param vec: 2d vector
    :param norm: desired magnitude of the output vector, default is 1
    :return: normalized (then optionally scaled) 2d vector
    :raise ValueError: if trying to scale a zero-length vector to a nonzero length
    """
    input_norm = get_norm(vec)
    if input_norm == 0 and norm != 0:
        except_msg = "cannot scale a zero-length vector to a nonzero length"
        raise ValueError(except_msg)
    if norm == 0:
        return 0, 0
    scale = norm / input_norm
    return vscale(vec, scale)


def vscale(vec: _Vec2, scale: float) -> tuple[float, float]:
    """Multiply a 2d vector by a scalar.

    :param vec: 2d vector
    :param scale: scalar for vec
    :return: vec * scale
    """
    return vec[0] * scale, vec[1] * scale


def vadd(vec_a: _Vec2, vec_b: _Vec2) -> tuple[float, float]:
    """Add two 2d vectors.

    :param vec_a: 2d vector
    :param vec_b: 2d vector
    :return: sum of the vectors
    """
    return vec_a[0] + vec_b[0], vec_a[1] + vec_b[1]


def vsub(vec_a: _Vec2, vec_b: _Vec2) -> tuple[float, float]:
    """Subtract two 2d vectors.

    :param vec_a: 2d vector
    :param vec_b: 2d vector
    :return: difference of the vectors
    """
    return vadd(vec_a, vscale(vec_b, -1))


def move_along(pnt: _Vec2, vec: _Vec2, distance: float) -> tuple[float, float]:
    """Move a point along a vector.

    :param pnt: 2d vector
    :param vec: 2d vector
    :param distance: distance to move v1 along v2
    :return: new point
    """
    vec12 = set_norm(vec, distance)
    return vadd(pnt, vec12)


def qrotate(vec: _Vec2, quadrants: int) -> tuple[float, float]:
    """Rotate a 2d vector 90 degrees counterclockwise.

    :param vec: 2d vector
    :param quadrants: number of 90 degree clockwise rotations
    :return: rotated vector
    """
    quadrants = quadrants % 4
    if quadrants == 0:
        return vec[0], vec[1]
    return qrotate((-vec[1], vec[0]), quadrants - 1)
