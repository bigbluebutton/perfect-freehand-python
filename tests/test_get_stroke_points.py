# SPDX-FileCopyrightText: 2021 Stephen Ruiz Ltd
# SPDX-FileCopyrightText: 2022 Calvin Walton
#
# SPDX-License-Identifier: MIT

from math import isfinite
from typing import Sequence

import pytest
from pytest import approx

from perfect_freehand import get_stroke_points
from perfect_freehand.types import StrokePoint


def compare_stroke_point(A: StrokePoint, B: StrokePoint) -> None:
    assert A["point"] == approx(B["point"])
    assert A["pressure"] == approx(B["pressure"])
    assert A["distance"] == approx(B["distance"])
    assert A["vector"] == approx(B["vector"])
    assert A["running_length"] == approx(B["running_length"])


def compare_stroke_points(
    points: Sequence[StrokePoint], ref_points: Sequence[StrokePoint]
) -> None:
    assert len(points) == len(ref_points)
    for A, B in zip(points, ref_points):
        compare_stroke_point(A, B)


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
    for point in get_stroke_points(input_json):
        assert isfinite(point["point"][0]) and isfinite(point["point"][1])
        assert isfinite(point["pressure"])
        assert isfinite(point["distance"])
        assert isfinite(point["vector"][0]) and isfinite(point["vector"][1])
        assert isfinite(point["running_length"])


def test_no_points(output_json: Sequence[StrokePoint]) -> None:
    """Get stroke points from a line with no points."""
    points = get_stroke_points([])
    assert points == approx(output_json)


@pytest.mark.input_json("onePoint")
def test_one_point(
    input_json: Sequence[Sequence[float]], output_json: Sequence[StrokePoint]
) -> None:
    """Get stroke points from a line with a single points."""
    points = get_stroke_points(input_json)
    compare_stroke_points(points, output_json)


@pytest.mark.input_json("twoPoints")
def test_two_points(
    input_json: Sequence[Sequence[float]], output_json: Sequence[StrokePoint]
) -> None:
    """Get stroke points from a line with two points."""
    points = get_stroke_points(input_json)
    compare_stroke_points(points, output_json)


@pytest.mark.input_json("twoEqualPoints")
def test_two_equal_points(
    input_json: Sequence[Sequence[float]], output_json: Sequence[StrokePoint]
) -> None:
    """Get stroke points from a line with two equal points."""
    points = get_stroke_points(input_json)
    compare_stroke_points(points, output_json)


@pytest.mark.input_json("manyPoints")
def test_many_points(
    input_json: Sequence[Sequence[float]], output_json: Sequence[StrokePoint]
) -> None:
    """Get stroke points from a line with many points."""
    points = get_stroke_points(input_json)
    compare_stroke_points(points, output_json)


@pytest.mark.input_json("withDuplicates")
def test_with_duplicates(
    input_json: Sequence[Sequence[float]], output_json: Sequence[StrokePoint]
) -> None:
    """Get stroke points from a line with duplicates."""
    points = get_stroke_points(input_json)
    compare_stroke_points(points, output_json)
