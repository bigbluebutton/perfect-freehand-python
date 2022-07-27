# MIT License
#
# Copyright (c) 2022 Calvin Walton
# Copyright (c) 2021 Stephen Ruiz

from typing import Callable


def default_easing(t: float) -> float:
    return t


def get_stroke_radius(
    size: float,
    thinning: float,
    pressure: float,
    easing: Callable[[float], float] = default_easing,
) -> float:
    """Compute a radius based on the pressure."""
    return size * easing(0.5 - thinning * (0.5 - pressure))
