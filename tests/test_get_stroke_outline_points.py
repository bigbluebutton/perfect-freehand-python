# SPDX-FileCopyrightText: 2021 Stephen Ruiz Ltd
# SPDX-FileCopyrightText: 2022 Calvin Walton
#
# SPDX-License-Identifier: MIT

import json
from math import isfinite
from typing import Sequence

import pytest
from pytest import approx

from perfect_freehand import get_stroke_outline_points, get_stroke_points


def compare_stroke_outline_points(
    points: Sequence[Sequence[float]], ref_points: Sequence[Sequence[float]]
) -> None:
    assert len(points) == len(ref_points)
    for A, B in zip(points, ref_points):
        assert A[0] == approx(B[0])
        assert A[1] == approx(B[1])


@pytest.mark.parametrize(
    ("input_json"),
    [
        "onePoint",
        "twoPoints",
        "twoEqualPoints",
        "numberPairs",
        "objectPairs",
        "withDuplicates",
        "manyPoints",
        "hey",
        "he2",
        "waves",
        "corners",
        "scribble",
    ],
    indirect=True,
)
def test_no_nan_values(input_json: Sequence[Sequence[float]]) -> None:
    """Run over many example input files without generating NaN values."""
    for point in get_stroke_outline_points(get_stroke_points(input_json)):
        assert isfinite(point[0])
        assert isfinite(point[1])


@pytest.mark.input_json("onePoint")
def test_one_point(
    input_json: Sequence[Sequence[float]], output_json: Sequence[Sequence[float]]
) -> None:
    """Get stroke outline points with a single point."""
    points = get_stroke_outline_points(get_stroke_points(input_json))
    compare_stroke_outline_points(points, output_json)


@pytest.mark.input_json("twoPoints")
def test_two_points(
    input_json: Sequence[Sequence[float]], output_json: Sequence[Sequence[float]]
) -> None:
    """Get stroke outline points with two points."""
    points = get_stroke_outline_points(get_stroke_points(input_json))
    compare_stroke_outline_points(points, output_json)


@pytest.mark.input_json("twoEqualPoints")
def test_two_equal_points(
    input_json: Sequence[Sequence[float]], output_json: Sequence[Sequence[float]]
) -> None:
    """Get stroke outline points from a line with two equal points."""
    points = get_stroke_outline_points(get_stroke_points(input_json))
    compare_stroke_outline_points(points, output_json)


@pytest.mark.input_json("manyPoints")
def test_many_points(
    input_json: Sequence[Sequence[float]], output_json: Sequence[Sequence[float]]
) -> None:
    """Get stroke outline points on a line with many points."""
    points = get_stroke_outline_points(get_stroke_points(input_json))
    compare_stroke_outline_points(points, output_json)


@pytest.mark.input_json("withDuplicates")
def test_with_duplicates(
    input_json: Sequence[Sequence[float]], output_json: Sequence[Sequence[float]]
) -> None:
    """Get stroke points from a line with duplicates."""
    points = get_stroke_outline_points(get_stroke_points(input_json))
    compare_stroke_outline_points(points, output_json)
