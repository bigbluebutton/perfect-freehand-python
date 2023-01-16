import json
from math import isfinite
from random import Random
from typing import Sequence

import pytest

from perfect_freehand import get_stroke
from tests.test_get_stroke_outline_points import compare_stroke_outline_points


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
def test_defaults(
    input_json: Sequence[Sequence[float]], output_json: Sequence[Sequence[float]]
) -> None:
    """It creates a stroke with default values."""
    result = get_stroke(input_json)
    compare_stroke_outline_points(result, output_json)
    for point in result:
        assert isfinite(point[0])
        assert isfinite(point[1])


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
def test_random(input_json: Sequence[Sequence[float]]) -> None:
    """It creates a stroke with random options."""
    rng = Random("perfect")

    for i in range(500):
        size = rng.uniform(-100, 100)
        thinning = rng.uniform(-1, 1)
        streamline = rng.uniform(-1, 1)
        smoothing = rng.uniform(-1, 1)
        simulate_pressure = rng.choices([False, True], cum_weights=[0.25, 1.0])[0]
        last = rng.choices([False, True], cum_weights=[0.75, 1.0])[0]
        cap_start = rng.choice([False, True])
        taper_start = rng.choice([rng.uniform(-100, 100), 0.0])
        cap_end = rng.choice([False, True])
        taper_end = rng.choice([rng.uniform(-100, 100), 0.0])
        print(
            f"options: size={size}, thinning={thinning}, streamline={streamline}, smoothing={smoothing}, last={last}, cap_start={cap_start}, taper_start={taper_start}, cap_end={cap_end}, taper_end={taper_end}"
        )

        result = get_stroke(
            input_json,
            size=size,
            thinning=thinning,
            streamline=streamline,
            smoothing=smoothing,
            simulate_pressure=simulate_pressure,
            last=last,
            cap_start=cap_start,
            taper_start=taper_start,
            cap_end=cap_end,
            taper_end=taper_end,
        )

        for point in result:
            assert isfinite(point[0])
            assert isfinite(point[1])


def test_no_points(output_json: Sequence[Sequence[float]]) -> None:
    """It gets stroke from a line with no points"""
    stroke = get_stroke([])
    compare_stroke_outline_points(stroke, output_json)


@pytest.mark.input_json("twoPoints")
def test_caps_points(input_json: Sequence[Sequence[float]]) -> None:
    """It Caps points"""
    stroke = get_stroke(input_json)
    assert len(stroke) > 4


@pytest.mark.input_json("onePoint")
def test_tricky_stroke_with_only_one_point(
    input_json: Sequence[Sequence[float]], output_json: Sequence[Sequence[float]]
) -> None:
    """It Solves a tricky stroke with only one point."""
    stroke = get_stroke(
        input_json,
        size=1.0,
        thinning=0.6,
        smoothing=0.5,
        streamline=0.5,
        simulate_pressure=True,
        last=False,
    )
    compare_stroke_outline_points(stroke, output_json)
    assert isfinite(stroke[0][0])
