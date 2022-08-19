# SPDX-FileCopyrightText: 2022 Calvin Walton
#
# SPDX-License-Identifier: MIT

# Configuration file for the Sphinx documentation builder.

# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------

from perfect_freehand import __version__ as release

project = "perfect-freehand-python"
copyright = "2022, Calvin Walton, Steve Ruiz Ltd"
author = "Calvin Walton, Steve Ruiz"

# -- General configuration ---------------------------------------------------

extensions = ["sphinx.ext.autodoc", "sphinx_autodoc_typehints"]

templates_path = ["_templates"]

exclude_patterns = []

autodoc_default_options = {"members": True}

# -- Options for HTML output -------------------------------------------------

html_theme = "alabaster"

html_static_path = ["_static"]
