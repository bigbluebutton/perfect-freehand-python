# SPDX-FileCopyrightText: 2021 Stephen Ruiz Ltd
# SPDX-FileCopyrightText: 2022 Calvin Walton
#
# SPDX-License-Identifier: MIT

"""Draw perfect pressure-sensitive freehand lines.

For most use cases, the :func:`get_stroke` function is the only thing you will
need. It transforms the input points from the device to a polygon representing
the stroke which can be drawn.
"""

__version__ = "1.2.0"
__all__ = ["get_stroke", "get_stroke_points", "get_stroke_outline_points"]

from math import pi
from typing import Callable, List, Optional, Sequence, Tuple, Union

from . import vec
from .types import InputPoint, StrokePoint

T = Sequence[float]

# Browser strokes seem to be off if PI is regular, a tiny offset seems to fix it
FIXED_PI = pi + 0.0001

# This is the rate of change for simulated pressure. It could be an option.
RATE_OF_PRESSURE_CHANGE = 0.275


def default_easing(t: float) -> float:
    return t


def default_taper_start_ease(t: float) -> float:
    return t * (2 - t)


def default_taper_end_ease(t: float) -> float:
    return (t - 1) * (t - 1) * t


def get_stroke_radius(
    size: float,
    thinning: float,
    pressure: float,
    easing: Callable[[float], float] = default_easing,
) -> float:
    """Compute a radius based on the pressure."""
    return size * easing(0.5 - thinning * (0.5 - pressure))


def get_stroke(
    points: Sequence[Union[T, InputPoint]],
    *,
    size: float = 16.0,
    streamline: float = 0.5,
    last: bool = False,
    thinning: float = 0.5,
    smoothing: float = 0.5,
    easing: Callable[[float], float] = default_easing,
    simulate_pressure: bool = True,
    cap_start: bool = True,
    taper_start: Union[bool, float] = False,
    taper_start_ease: Callable[[float], float] = default_taper_start_ease,
    cap_end: bool = True,
    taper_end: Union[bool, float] = False,
    taper_end_ease: Callable[[float], float] = default_taper_end_ease,
) -> List[Tuple[float, float]]:
    """Get an array of points describing a polygon that surrounds the input points.

    Internally, this calls :func:`get_stroke_points` to pre-process the points
    (normalizing, smoothing, adding extra metadata) then
    :func:`get_stroke_outline_points` to transform the points to an outline of
    the drawn stroke.

    :param points: An array of points, as a iterable ``(x, y, pressure)`` or a
        dict ``{"x": x, "y": y, "pressure": p}``.

        Pressure is optional in both cases.
    :param size: The base size (diameter) of the stroke.
    :param streamline: Adjust the interpolation level between points.
    :param last: Whether to handle the points as a completed stroke.
    :param thinning: The effect of pressure on the stroke's size.
    :param smoothing: How much to soften the stroke's edges.
    :param easing: An easing function to apply to each point's pressure.
    :param simulate_pressure: Whether to simulate pressure based on velocity.
    :param cap_start: Whether to draw a round cap at the start of the line.
        This parameter has no effect if ``taper_start`` is non-zero.
    :param taper_start: The distance to apply the start taper. If set to
        ``True``, the taper will be the total length of the stroke.
    :param taper_start_ease: An easing function for the start taper. Default is
        based on a quadratic curve.
    :param cap_end: Whether to draw a round cap at the end of the line. This
        parameter has no effect if ``taper_end`` is non-zero.
    :param taper_end: The distance to apply the end taper. If set to ``True``,
        the taper will be the total length of the stroke.
    :param taper_end_ease: An easing function for the end taper. Default is
        based on a cubic curve.
    :return: A sequence of points (each represented by a tuple of ``(x, y)``)
        that represent an outline of the drawn stroke.

    :return: A sequence of points (each represented by a tuple of ``(x, y)``) that
        represent an outline of the drawn stroke.
    """
    return get_stroke_outline_points(
        get_stroke_points(points, size=size, streamline=streamline, last=last),
        size=size,
        thinning=thinning,
        smoothing=smoothing,
        last=last,
        easing=easing,
        simulate_pressure=simulate_pressure,
        cap_start=cap_start,
        taper_start=taper_start,
        taper_start_ease=taper_start_ease,
        cap_end=cap_end,
        taper_end=taper_end,
        taper_end_ease=taper_end_ease,
    )


def get_stroke_points(
    points: Sequence[Union[T, InputPoint]],
    *,
    size: float = 16.0,
    streamline: float = 0.5,
    last: bool = False,
) -> List[StrokePoint]:
    """Returns a sequence of stroke points with an adjusted point, pressure,
    vector, distance, and running length.

    :param points: An array of points, as a iterable ``(x, y, pressure)`` or a
        dict ``{"x": x, "y": y, "pressure": p}``.

        Pressure is optional in both cases.
    :param size: The base size (diameter) of the stroke.
    :param streamline: Adjust the interpolation level between points.
    :param last: Whether to handle the points as a completed stroke.
    :return: A sequence of :class:`types.StrokePoint` objects.

    .. note::
        When the ``last`` property is ``True``, the line's end will be drawn at
        the last input point, rather than slightly behind it.
    """

    # If we don't have any points, return an empty array.
    if len(points) == 0:
        return []

    # Find the interpolation level between points
    t: float = 0.15 + (1.0 - streamline) * 0.85

    # Convert the input to a list of tuples regardless of input type
    pts: List[T] = list(
        point
        if isinstance(point, Sequence)
        else (point["x"], point["y"], point["pressure"])
        if "pressure" in point
        else (point["x"], point["y"], 0.5)
        for point in points
    )

    # Add extra points between the two, to help avoid "dash" lines
    # for strokes with tapered start and ends. Don't mutate the
    # input array!
    if len(pts) == 2:
        last_pt = pts.pop()
        pts.extend(vec.lrp(pts[0], last_pt, i / 4.0) for i in range(1, 5))

    # If there's only one point, add another point at a 1pt offset.
    if len(pts) == 1:
        pts.append(vec.add(pts[0], (1.0, 1.0, 0.0)))

    # The stroke_points array will hold the points for the stroke.
    # Start it out with the first point, which needs no adjustment.
    stroke_points: List[StrokePoint] = [
        StrokePoint(
            point=(pts[0][0], pts[0][1]),
            pressure=pts[0][2] if len(pts[0]) > 2 else 0.25,
            vector=(1.0, 1.0),
            distance=0.0,
            running_length=0.0,
        )
    ]

    # A flag to see whether we've already reached our minimum length
    has_reached_minimum_length = False

    # We use the running_length to keep track of the total distance
    running_length = 0.0

    # We've set this to the latest point, so we can use it to calculate
    # the distance and vector of the next point.
    prev = stroke_points[0]

    max = len(pts) - 1

    for i in range(1, len(pts)):
        if last and i == max:
            # If we're at the last point and the last option is true,
            # then add the actual input point.
            point = (pts[i][0], pts[i][1])
        else:
            # Otherwise, using the t calculated from the streamline
            # option, interpolate a new point between the previous
            # point and the current point.
            point = vec.lrp(prev["point"], pts[i], t)

        # If the new point is the same as the previous point, skip ahead
        if prev["point"] == point:
            continue

        # How far is the new point from the previous point?
        distance = vec.dist(point, prev["point"])

        # Add this distance to the total "running length" of the line.
        running_length += distance

        # At the start of the line, we wait until the new point is a
        # certain distance away from the original point, to avoid noise
        if i < max and not has_reached_minimum_length:
            if running_length < size:
                continue
            has_reached_minimum_length = True
            # TODO: Backfill the missing points so that tapering works correctly.

        # Create a new strokepoint (it will be the new "previous" one).
        prev = StrokePoint(
            point=point,
            pressure=pts[i][2] if len(pts[i]) > 2 else 0.5,
            vector=vec.uni(vec.sub(prev["point"], point)),
            distance=distance,
            running_length=running_length,
        )

        # Push it to the stroke_points array.
        stroke_points.append(prev)

    # Set the vector of the first point to be the same as the second point
    if len(stroke_points) > 1:
        stroke_points[0]["vector"] = stroke_points[1]["vector"]
    else:
        stroke_points[0]["vector"] = (0.0, 0.0)

    return stroke_points


def get_stroke_outline_points(
    points: Sequence[StrokePoint],
    *,
    size: float = 16.0,
    thinning: float = 0.5,
    smoothing: float = 0.5,
    easing: Callable[[float], float] = default_easing,
    simulate_pressure: bool = True,
    last: bool = False,
    cap_start: bool = True,
    taper_start: Union[bool, float] = False,
    taper_start_ease: Callable[[float], float] = default_taper_start_ease,
    cap_end: bool = True,
    taper_end: Union[bool, float] = False,
    taper_end_ease: Callable[[float], float] = default_taper_end_ease,
) -> List[Tuple[float, float]]:
    """Get an array of points (as ``(x, y)``) representing the outline of a stroke.

    :param points: An array of :class:`types.StrokePoint` as returned from
        :func:`get_stroke_points`.
    :param size: The base size (diameter) of the stroke.
    :param thinning: The effect of pressure on the stroke's size.
    :param smoothing: How much to soften the stroke's edges.
    :param easing: An easing function to apply to each point's pressure.
    :param simulate_pressure: Whether to simulate pressure based on velocity.
    :param last: Whether to handle the points as a completed stroke.
    :param cap_start: Whether to draw a round cap at the start of the line.
        This parameter has no effect if ``taper_start`` is non-zero.
    :param taper_start: The distance to apply the start taper. If set to
        ``True``, the taper will be the total length of the stroke.
    :param taper_start_ease: An easing function for the start taper. Default is
        based on a quadratic curve.
    :param cap_end: Whether to draw a round cap at the end of the line. This
        parameter has no effect if ``taper_end`` is non-zero.
    :param taper_end: The distance to apply the end taper. If set to ``True``,
        the taper will be the total length of the stroke.
    :param taper_end_ease: An easing function for the end taper. Default is
        based on a cubic curve.
    :return: A sequence of points (each represented by a tuple of ``(x, y)``)
        that represent an outline of the drawn stroke.
    """

    # We can't do anything with an empty array or a stroke with negative size.
    if len(points) == 0 or size <= 0.0:
        return []

    total_length = points[-1]["running_length"]

    if isinstance(taper_start, bool):
        if taper_start:
            taper_start = max(size, total_length)
        else:
            taper_start = 0.0

    if isinstance(taper_end, bool):
        if taper_end:
            taper_end = max(size, total_length)
        else:
            taper_end = 0.0

    # The minimum allowed distance between points (squared)
    min_distance = (size * smoothing) ** 2

    # Our collected left and right points
    left_pts: List[Tuple[float, float]] = []
    right_pts: List[Tuple[float, float]] = []

    # Previous pressure (start with average of first five pressures,
    # in order to prevent fat starts for every line. Drawn lines
    # almost always start slow!)
    prev_pressure = points[0]["pressure"]
    for point_i in points[0:10]:
        pressure = point_i["pressure"]
        if simulate_pressure:
            # Speed of change - how fast should the pressure change?
            sp = min(1.0, point_i["distance"] / size)
            # Rate of change - how much of a change is there?
            rp = min(1.0, 1.0 - sp)
            # Accelerate the pressure
            pressure = min(
                1.0,
                prev_pressure + (rp - prev_pressure) * (sp * RATE_OF_PRESSURE_CHANGE),
            )

        prev_pressure = (prev_pressure + pressure) / 2

    # The current radius
    radius = get_stroke_radius(size, thinning, points[-1]["pressure"], easing)

    # The radius of the first saved point
    first_radius: Optional[float] = None

    # Previous vector
    prev_vector = points[0]["vector"]

    # Previous left and right points
    pl = points[0]["point"]
    pr = pl

    # Temporary left and right points
    tl = pl
    tr = pr

    # Keep track of whether the previous point is a sharp corner
    # ... so that we don't detect the same corner twice
    is_prev_point_sharp_corner = False

    # Find the outline's left and right points
    #
    # Iterating through the points and populate the right_pts and left_pts arrays,
    # skipping the first and last points, which will get caps later on.
    for i, point_i in enumerate(points):
        pressure = point_i["pressure"]
        point = point_i["point"]
        vector = point_i["vector"]
        distance = point_i["distance"]
        running_length = point_i["running_length"]

        # Removes noise from the end of the line
        if i < len(points) - 1 and total_length - running_length < 3:
            continue

        # Calculate the radius
        #
        # If not thinning, the current point's radius will be half the size; or
        # otherwise, the size will be based on the current (real or simulated)
        # pressure.
        if thinning:
            if simulate_pressure:
                # If we're simulating pressure, then do so based on the distance
                # between the current point and the previous point, and the size
                # of the stroke. Otherwise use the input pressure.
                sp = min(1.0, distance / size)
                rp = min(1.0, 1.0 - sp)
                pressure = min(
                    1.0,
                    prev_pressure
                    + (rp - prev_pressure) * (sp * RATE_OF_PRESSURE_CHANGE),
                )

            radius = get_stroke_radius(size, thinning, pressure, easing)
        else:
            radius = size / 2.0

        if first_radius is None:
            first_radius = radius

        # Apply tapering
        #
        # If the current length is within the taper distance at either the
        # start or the end, calculate the taper strengths. Apply the smaller
        # of the two taper strengths to the radius.
        if running_length < taper_start:
            ts = taper_start_ease(running_length / taper_start)
        else:
            ts = 1.0

        if total_length - running_length < taper_end:
            te = taper_end_ease((total_length - running_length) / taper_end)
        else:
            te = 1.0

        radius = max(0.01, radius * min(ts, te))

        # Add points to left and right

        # Handle sharp corners
        #
        # Find the difference (dot product) between the current and next vector.
        # If the next vector is at more than a right angle to the current vector,
        # draw a cap at the current point.
        next_vector = (
            points[i + 1]["vector"] if i < len(points) - 1 else points[i]["vector"]
        )
        next_dpr = vec.dpr(vector, next_vector) if i < len(points) - 1 else 1.0
        prev_dpr = vec.dpr(vector, prev_vector)

        is_point_sharp_corner = prev_dpr < 0 and not is_prev_point_sharp_corner
        is_next_point_sharp_corner = next_dpr < 0

        if is_point_sharp_corner or is_next_point_sharp_corner:
            # It's a sharp corner. Draw a rounded cap and move on to the next point
            # Considering saving these and drawing them later? So that we can avoid
            # crossing future points.
            offset = vec.mul(vec.per(prev_vector), radius)

            for i in range(0, 14):
                t = i / 13.0

                tl = vec.rotAround(vec.sub(point, offset), point, FIXED_PI * t)
                left_pts.append(tl)

                tr = vec.rotAround(vec.add(point, offset), point, FIXED_PI * -t)
                right_pts.append(tr)

            pl = tl
            pr = tr

            if is_next_point_sharp_corner:
                is_prev_point_sharp_corner = True

            continue

        is_prev_point_sharp_corner = False

        # Handle the last point
        if i == len(points) - 1:
            offset = vec.mul(vec.per(vector), radius)
            left_pts.append(vec.sub(point, offset))
            right_pts.append(vec.add(point, offset))
            continue

        # Add regular points
        #
        # Project points to either side of the current point, using the
        # calculated size as a distance. If a point's distance to the
        # previous point on that side is greater than the minimum distance
        # (or if the corner is kinda sharp), add the points to the side's
        # points array.
        offset = vec.mul(vec.per(vec.lrp(next_vector, vector, next_dpr)), radius)

        tl = vec.sub(point, offset)
        if i <= 1 or vec.dist2(pl, tl) > min_distance:
            left_pts.append(tl)
            pl = tl

        tr = vec.add(point, offset)
        if i <= 1 or vec.dist2(pr, tr) > min_distance:
            right_pts.append(tr)
            pr = tr

        # Set variables for next iteration
        prev_pressure = pressure
        prev_vector = vector

    # Drawing caps
    #
    # Now that we have our points on either side of the line, we need to
    # draw caps at the start and end. Tapered lines don't have caps, but
    # may have dots for very short lines.

    first_point = points[0]["point"]

    if len(points) > 1:
        last_point = points[-1]["point"]
    else:
        last_point = vec.add(first_point, (1.0, 1.0))

    start_cap: List[Tuple[float, float]] = []
    end_cap: List[Tuple[float, float]] = []

    # Draw a dot for very short or completed strokes
    #
    # If the line is too short to gather left or right points and if the line is
    # not tapered on either side, draw a dot. If the line is tapered, then only
    # draw a dot if the line is both very short and complete. If we draw a dot,
    # we can just return those points

    if first_radius is None:
        first_radius = radius

    if len(points) == 1:
        if not (taper_start or taper_end) or last:
            start = vec.prj(
                first_point,
                vec.uni(vec.per(vec.sub(first_point, last_point))),
                -first_radius,
            )
            dot_pts: List[Tuple[float, float]] = []
            for i in range(1, 14):
                t = i / 13.0
                dot_pts.append(vec.rotAround(start, first_point, FIXED_PI * 2 * t))
            return dot_pts
    else:
        # Draw a start cap
        #
        # Unless the line has a tapered start, or unless the line has a tapered end
        # and the line is very short, draw a start cap around the first point. Use
        # the distance between the second left and right point for the cap's radius.
        # Finally remove the first left and right points.

        if taper_start or (taper_end and len(points) == 1):
            # The start point is tapered, noop
            pass
        elif cap_start:
            # Draw the round cap - add thirteen points rotating the right point around the start point to the left point
            for i in range(1, 14):
                t = i / 13.0
                pt = vec.rotAround(right_pts[0], first_point, FIXED_PI * t)
                start_cap.append(pt)
        else:
            # Draw the flat cap - add a point to the left and right of the start point
            corners_vector = vec.sub(left_pts[0], right_pts[0])
            offset_a = vec.mul(corners_vector, 0.5)
            offset_b = vec.mul(corners_vector, 0.51)

            start_cap.append(vec.sub(first_point, offset_a))
            start_cap.append(vec.sub(first_point, offset_b))
            start_cap.append(vec.add(first_point, offset_b))
            start_cap.append(vec.add(first_point, offset_a))

        # Draw an end cap
        #
        # If the line does not have a tapered end, and unless the line has a tapered
        # start and the line is very short, draw a cap around the last point. Finally,
        # remove the last left and right points. Otherwise, add the last point. Note
        # that this cap is a full-turn-and-a-half: this prevents incorrect caps on
        # sharp end turns.

        direction = vec.per(vec.neg(points[-1]["vector"]))

        if taper_end or (taper_start and len(points) == 1):
            # Tapered end - push the last point to the line
            end_cap.append(last_point)
        elif cap_end:
            # Draw the round end cap
            start = vec.prj(last_point, direction, radius)
            for i in range(1, 30):
                t = i / 29.0
                end_cap.append(vec.rotAround(start, last_point, FIXED_PI * 3 * t))
        else:
            # Draw the flat end cap
            end_cap.append(vec.add(last_point, vec.mul(direction, radius)))
            end_cap.append(vec.add(last_point, vec.mul(direction, radius * 0.99)))
            end_cap.append(vec.sub(last_point, vec.mul(direction, radius * 0.99)))
            end_cap.append(vec.sub(last_point, vec.mul(direction, radius)))

    # Return the points in the correct winding order: begin on the left side, then
    # continue around the end cap, then come back along the right side, and finally
    # complete the start cap.
    left_pts.extend(end_cap)
    left_pts.extend(reversed(right_pts))
    left_pts.extend(start_cap)
    return left_pts
