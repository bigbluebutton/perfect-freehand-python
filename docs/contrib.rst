.. SPDX-FileCopyrightText: 2022 Calvin Walton
   
   SPDX-License-Identifier: MIT

.. highlight:: sh

Development & Contributions
===========================

Development of perfect-freehand-python takes place on Github:
`bigbluebutton/perfect-freehand-python <https://github.com/bigbluebutton/perfect-freehand-python>`_.

This Python port of the
`perfect-freehand <https://github.com/steveruizok/perfect-freehand>`_ library
is maintained by the `BigBlueButton <https://bigbluebutton.org/>`_ project.
Like the original TypeScript version, the code is made available under the
`MIT license <https://spdx.org/licenses/MIT.html>`_.

Pull requests are welcome! It's important for the code in this repository to
be kept in sync with the TypeScript
`perfect-freehand <https://github.com/steveruizok/perfect-freehand>`_ library,
so if you have any functionality changes that you would like to propose, please
send them to the upstream library first for discussion.

Development Environment
-----------------------

Start by cloning the perfect-freehand-python git repository::

    git clone https://github.com/bigbluebutton/perfect-freehand-python.git
    cd perfect-freehand-python

Rather than installing the development dependencies into your global
environment, I recommend using
`venv <https://docs.python.org/3/library/venv.html>`_. Set up a venv and
install the dependencies by running the following commands::

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-dev.txt

Every time you'd like to work on the project, you need to run
``source .venv/bin/activate`` after changing to the project directory.

Common Development Tasks
------------------------

Automatic Formatting
^^^^^^^^^^^^^^^^^^^^

Run `black <https://github.com/psf/black>`_ with the following command to
apply automatic formatting::

    black src tests

You might also be interested in
`integrating black with your editor <https://black.readthedocs.io/en/stable/integrations/editors.html>`_.

Running Tests
^^^^^^^^^^^^^

Because of the structure of the code in the repository, you must set the
``PYTHONPATH`` environment variable to run ``pytest`` against the uninstalled
(development) code. Use the following command::

    PYTHONPATH=src pytest

Static Type-checking
^^^^^^^^^^^^^^^^^^^^

This project includes static type hints. These can be checked using
`mypy <http://mypy-lang.org/>`_::

    mypy src tests

Building documentation
^^^^^^^^^^^^^^^^^^^^^^

The HTML documentation (what you are reading right now!) can be built by
running the following command::

    sphinx-build docs build/html
