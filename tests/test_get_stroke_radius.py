from perfect_freehand.get_stroke_radius import get_stroke_radius
from pytest import approx


def test_thinning_zero():
    """When thinning is zero it uses half the size."""
    assert get_stroke_radius(100.0, 0.0, 0.0) == approx(50.0)
    assert get_stroke_radius(100.0, 0.0, 0.25) == approx(50.0)
    assert get_stroke_radius(100.0, 0.0, 0.5) == approx(50.0)
    assert get_stroke_radius(100.0, 0.0, 0.75) == approx(50.0)
    assert get_stroke_radius(100.0, 0.0, 1.0) == approx(50.0)


def test_thinning_positive_half():
    """When thinning is positive it scales between 25% and 75% at 0.5 thinning."""
    assert get_stroke_radius(100.0, 0.5, 0.0) == approx(25.0)
    assert get_stroke_radius(100.0, 0.5, 0.25) == approx(37.5)
    assert get_stroke_radius(100.0, 0.5, 0.5) == approx(50.0)
    assert get_stroke_radius(100.0, 0.5, 0.75) == approx(62.5)
    assert get_stroke_radius(100.0, 0.5, 1.0) == approx(75.0)


def test_thinning_positive_one():
    """When thinning is positive it scales between 0% and 100% at 1 thinning."""
    assert get_stroke_radius(100.0, 1.0, 0.0) == approx(0.0)
    assert get_stroke_radius(100.0, 1.0, 0.25) == approx(25.0)
    assert get_stroke_radius(100.0, 1.0, 0.5) == approx(50.0)
    assert get_stroke_radius(100.0, 1.0, 0.75) == approx(75.0)
    assert get_stroke_radius(100.0, 1.0, 1.0) == approx(100.0)


def test_thinning_negative_half():
    """When thinning is negative it scales between 75% and 25% at -0.5 thinning."""
    assert get_stroke_radius(100.0, -0.5, 0.0) == approx(75.0)
    assert get_stroke_radius(100.0, -0.5, 0.25) == approx(62.5)
    assert get_stroke_radius(100.0, -0.5, 0.5) == approx(50.0)
    assert get_stroke_radius(100.0, -0.5, 0.75) == approx(37.5)
    assert get_stroke_radius(100.0, -0.5, 1.0) == approx(25.0)


def test_thinning_negative_one():
    """When thinning is negative it scales between 100% and 0% at -1 thinning."""
    assert get_stroke_radius(100.0, -1.0, 0.0) == approx(100.0)
    assert get_stroke_radius(100.0, -1.0, 0.25) == approx(75.0)
    assert get_stroke_radius(100.0, -1.0, 0.5) == approx(50.0)
    assert get_stroke_radius(100.0, -1.0, 0.75) == approx(25.0)
    assert get_stroke_radius(100.0, -1.0, 1.0) == approx(0.0)


def test_easing_exponential_thinning_one():
    """When easing is exponential it scales between 0% and 100% at 1 thinning."""

    def easing(t):
        return t * t

    assert get_stroke_radius(100.0, 1.0, 0.0, easing) == approx(0.0)
    assert get_stroke_radius(100.0, 1.0, 0.25, easing) == approx(6.25)
    assert get_stroke_radius(100.0, 1.0, 0.5, easing) == approx(25.0)
    assert get_stroke_radius(100.0, 1.0, 0.75, easing) == approx(56.25)
    assert get_stroke_radius(100.0, 1.0, 1.0, easing) == approx(100.0)


def test_easing_exponential_thinning_negative_one():
    """When easing is exponential it scales between 100% and 0% at -1 thinning."""

    def easing(t):
        return t * t

    assert get_stroke_radius(100.0, -1.0, 0.0, easing) == approx(100.0)
    assert get_stroke_radius(100.0, -1.0, 0.25, easing) == approx(56.25)
    assert get_stroke_radius(100.0, -1.0, 0.5, easing) == approx(25.0)
    assert get_stroke_radius(100.0, -1.0, 0.75, easing) == approx(6.25)
    assert get_stroke_radius(100.0, -1.0, 1.0, easing) == approx(0.0)
