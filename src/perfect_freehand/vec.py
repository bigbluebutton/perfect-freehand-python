# SPDX-FileCopyrightText: 2021 Stephen Ruiz Ltd
# SPDX-FileCopyrightText: 2022 Calvin Walton
#
# SPDX-License-Identifier: MIT

from math import cos, hypot, sin
from typing import Sequence, Tuple

S = Sequence[float]
V = Tuple[float, float]


def neg(A: S) -> V:
    """Negate a vector."""
    return (-A[0], -A[1])


def add(A: S, B: S) -> V:
    """Add vectors."""
    return (A[0] + B[0], A[1] + B[1])


def sub(A: S, B: S) -> V:
    """Subtract vectors."""
    return (A[0] - B[0], A[1] - B[1])


def mul(A: S, n: float) -> V:
    """Vector multiplication by scalar."""
    return (A[0] * n, A[1] * n)


def div(A: S, n: float) -> V:
    """Vector division by scalar."""
    return (A[0] / n, A[1] / n)


def per(A: S) -> V:
    """Perpendicular rotation of a vector."""
    return (A[1], -A[0])


def dpr(A: S, B: S) -> float:
    """Dot product."""
    return A[0] * B[0] + A[1] * B[1]


def len(A: S) -> float:
    """Length of the vector."""
    return hypot(A[0], A[1])


def uni(A: S) -> V:
    """Get normalized / unit vector."""
    return div(A, len(A))


def dist(A: S, B: S) -> float:
    """Dist length from A to B."""
    return hypot(A[1] - B[1], A[0] - B[0])


def len2(A: S) -> float:
    """Length of the vector squared."""
    return A[0] * A[0] + A[1] * A[1]


def dist2(A: S, B: S) -> float:
    """Dist length from A to B squared."""
    return len2(sub(A, B))


def rotAround(A: S, C: S, r: float) -> V:
    """Rotate a vector around another vector by r (radians)

    Args:
        A: vector
        C: center
        r: rotation in radians
    """
    s = sin(r)
    c = cos(r)

    px = A[0] - C[0]
    py = A[1] - C[1]

    nx = px * c - py * s
    ny = px * s + py * c

    return (nx + C[0], ny + C[1])


def lrp(A: S, B: S, t: float) -> V:
    """Interpolate vector A to B with a scalar t"""
    return add(A, mul(sub(B, A), t))


def prj(A: S, B: S, c: float) -> V:
    """Project a point A in the direction B by a scaler c"""
    return add(A, mul(B, c))
