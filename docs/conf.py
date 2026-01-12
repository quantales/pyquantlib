# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Path setup --------------------------------------------------------------

# Add project root to path for autodoc
sys.path.insert(0, os.path.abspath(".."))

# -- Project information -----------------------------------------------------

project = "PyQuantLib"
copyright = "2025, Yassine Idyiahia"
author = "Yassine Idyiahia"

# Version info - read directly to avoid importing compiled module
import re

version_file = os.path.join(os.path.dirname(__file__), "..", "pyquantlib", "version.py")
try:
    with open(version_file) as f:
        version_content = f.read()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', version_content)
    release = match.group(1) if match else "0.1.0"
    version = ".".join(release.split(".")[:2])
except Exception:
    version = "0.1"
    release = "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "myst_parser",
    "sphinx_copybutton",
]

# MyST-Parser configuration (for Markdown support)
myst_enable_extensions = [
    "dollarmath",
    "colon_fence",
    "deflist",
    "fieldlist",
    "tasklist",
]
myst_heading_anchors = 3

# Source file suffixes
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# The master toctree document
master_doc = "index"

# Patterns to exclude
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Pygments style for code highlighting
pygments_style = "tango"
pygments_dark_style = "material"

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"

html_theme_options = {
    "source_repository": "https://github.com/quantales/pyquantlib",
    "source_branch": "main",
    "source_directory": "docs/",
    "sidebar_hide_name": True,
    "light_css_variables": {
        "color-brand-primary": "#2962ff",
        "color-brand-content": "#2962ff",
    },
    "dark_css_variables": {
        "color-brand-primary": "#82b1ff",
        "color-brand-content": "#82b1ff",
    },
}

html_title = "PyQuantLib"
html_short_title = "PyQuantLib"

# Custom static files
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Logo and favicon
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.svg"

# -- Options for autodoc -----------------------------------------------------

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}

autodoc_member_order = "groupwise"
autodoc_typehints = "description"

# -- Options for intersphinx -------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# -- Options for napoleon (Google/NumPy docstrings) --------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# -- Options for copybutton --------------------------------------------------

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: "
copybutton_prompt_is_regexp = True
