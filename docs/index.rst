.. SPDX-FileCopyrightText: 2021 Stephen Ruiz Ltd
   SPDX-FileCopyrightText: 2022 Calvin Walton
   
   SPDX-License-Identifier: MIT

.. image:: _static/perfect-freehand-logo.svg
   :alt: Perfect Freehand

Draw perfect pressure-sensitive freehand lines.

This is a Python port of the 
`perfect-freehand library <https://github.com/steveruizok/perfect-freehand>`_
originally written by Steve Ruiz in TypeScript. Please reference the
documentation for that library for additional usage examples, links to
other implementations, and to support the original author.

Introduction
============

This package exports a function named :func:`perfect_freehand.get_stroke` that
will generate the points for a polygon based on an array of points.

.. image:: _static/process.gif
   :alt: A GIF showing a stroke with input points, outline points, and a curved
      path connecting these points

To do this work, ``get_stroke()`` first creates a set of split points (red)
based on the input points (grey) and then creates outline points (blue). You
can render the result any way you like, using whichever technology you prefer.



Table of Contents
=================

.. toctree::

   usage
   api
   tips
   contrib

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
