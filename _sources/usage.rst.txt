Usage
=====

To use this library, import the :func:`perfect_freehand.get_stroke` function
and pass it a list of **input points**, such as those recorded from a user's
mouse movement. The ``get_stroke()`` function will return a new list of
**outline points**. These outline points will form a polygon (called a "stroke")
that surrounds the input points.

>>> from perfect_freehand import get_stroke
>>> input_points = [
...     (0, 0),
...     (10, 5),
...     (20, 8),
...     # ...
... ]
>>> outline_points = get_stroke(input_points)

You can then **render** your stroke points using your technology of choice.

You can **customize** the appearance of the stroke shape by passing additional
keyword parameters to the ``get_stroke()`` function. The available options are
described in the documentation for the :func:`perfect_freehand.get_stroke_points`
and :func:`perfect_freehand.get_stroke_outline_points` functions.

>>> stroke = get_stroke(my_points, size=32, thinning=0.7)

The appearance of a stroke is affected by the **pressure** associated with each
input point. Bu default, the ``get_stroke()`` function will simulate pressure
based on the distance between input points.

To use **real pressure**, such as that from a pen or stylus, provide the
pressure as the third number for each input point, and set the
``simulate_pressure`` option to ``False``.

>>> input_points = [
...     (0, 0, 0.5),
...     (10, 5, 0.7),
...     (20, 8, 0.8),
...     # ...
... ]
>>> outline_points = get_stroke(input_points, simulate_pressure=False)

In addition to providing points as an iterable sequence type like a ``tuple``
or ``list``, you can also provide them as a ``dict`` as shown in the example
below. In both cases, the value for pressure is optional (it will default to
``0.5``).

>>> input_points = [
...     {'x': 0, 'y': 0, 'pressure': 0.5},
...     {'x': 10, 'y': 5, 'pressure': 0.7},
...     {'x': 20, 'y': 8, 'pressure': 0.8},
...     # ...
... ]
>>> outline_points = get_stroke(input_points, simulate_pressure=False)

Note that providing points in ``dict`` format introduces an extra conversion
step in the ``get_stroke()`` function which will have an effect on performance.
