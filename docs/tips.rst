.. SPDX-FileCopyrightText: 2021 Stephen Ruiz Ltd
   SPDX-FileCopyrightText: 2022 Calvin Walton
   
   SPDX-License-Identifier: MIT

Tips & Tricks
=============

Freehand Anything
-----------------

While this library was designed for rendering the types of input points
generated by the movement of the human hand, you can pass any set of points
into the library's functions. For example, here's what you get when running
`Feather Icons <https://feathericons.com/>`_ through
:func:`perfect_freehand.get_stroke`.

.. image:: _static/icons.png

Rendering
---------

While :func:`perfect_freehand.get_stroke` returns an array of points
representing the outline of a stroke, it's up to you to decide how you will
render these points.

The function below will turn the points returned by ``get_stroke()`` into SVG
path data::

    from itertools import chain, pairwise

    def svg_path_from_stroke(stroke):
        if len(stroke) == 0:
            return ""

        d = ['M', f'{stroke[0][0]}', f'{stroke[0][1]}', 'Q']
        for ((x0, y0), (x1, y1)) in pairwise(chain(stroke, [stroke[0]])):
            d.extend([
                f'{(x0 + x1) / 2}',
                f'{(y0 + y1) / 2}',
                f'{x1}',
                f'{y1}'
            ])
        
        d.append('Z')
        return ' '.join(d)

To use this function, first run your input points through ``get_stroke()``,
then pass the result to ``svg_path_from_stroke``. The path must be rendered in
the SVG using ``fill-rule="nonzero"``.

Flattening
----------

By default, the polygon's paths include self-crossings. You may wish to remove
these crossings and render a stroke as a "flattened" polygon. One example of
how this can be done is using the
`object.buffer() <https://shapely.readthedocs.io/en/stable/manual.html#object.buffer>`_
method provided by `shapely <https://shapely.readthedocs.io/>`_.

As an example, here's a method for generating a flattened svg polygon, re-using
the ``svg_path_from_stroke()`` function seen in the previous example::

    from shapely.geometry import Polygon

    def flat_svg_path_from_stroke(stroke):
        polygon = Polygon(stroke)

        # At this point, polygon.is_valid may be False due to self-
        # crossings. To fix this, use the "buffer" method with an
        # offset of 0.
        polygon = polygon.buffer(0)

        # The polygon will now consist of one exterior ring, and holes
        # will be represented by interior rings.
        d = [svg_path_from_stroke(polygon.exterior.coords)]
        for interior in polygon.interiors:
            d.append(svg_path_from_stroke(interior.coords))

        return ' '.join(d)

Since the SVG path now consists of multiple separate rings, in order for the
holes to be rendered you must used ``fill-rule="evenodd"``.
