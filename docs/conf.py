# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
import sys

# Ensure autodoc imports the installed PyPI wheel, not the source tree
# (source tree has no compiled _pyquantlib extension)
_src_root = os.path.normcase(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path = [p for p in sys.path if os.path.normcase(os.path.abspath(p)) != _src_root]

# Diagnostic: verify pyquantlib is importable (remove after confirming RTD works)
try:
    import pyquantlib as _pql
    print(f"[conf.py] pyquantlib {_pql.__version__} from {_pql.__file__}")
    del _pql
except ImportError as _e:
    print(f"[conf.py] pyquantlib import FAILED: {_e}")
    print(f"[conf.py] sys.path = {sys.path[:5]}")

# -- Project information -----------------------------------------------------

project = "PyQuantLib"
copyright = "2025, Yassine Idyiahia"
author = "Yassine Idyiahia"

# Version info - read directly to avoid importing compiled module
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

# Keep only section headings in the right-hand page TOC
toc_object_entries = False

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
    "special-members": "__init__",
}

autodoc_member_order = "groupwise"
autodoc_typehints = "description"
autodoc_typehints_format = "short"

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

# -- Autodoc signature cleanup -----------------------------------------------


def process_signature(app, what, name, obj, options, signature, return_annotation):
    """Clean up pybind11 signatures."""
    if signature:
        # Remove module paths: pyquantlib._pyquantlib.ClassName -> ClassName
        signature = re.sub(r"pyquantlib\._pyquantlib\.", "", signature)
        # Remove self parameter
        signature = re.sub(r"\(self: [^,]+, ", "(", signature)
        signature = re.sub(r"\(self: [^)]+\)", "()", signature)
    if return_annotation:
        return_annotation = re.sub(r"pyquantlib\._pyquantlib\.", "", return_annotation)
    return signature, return_annotation


def process_docstring(app, what, name, obj, options, lines):
    """Clean up pybind11 overloaded signatures in docstrings."""
    for i, line in enumerate(lines):
        # Remove module paths
        line = re.sub(r"pyquantlib\._pyquantlib\.", "", line)
        # Remove typing. prefix
        line = re.sub(r"typing\.", "", line)
        # Remove self parameter in overloaded signatures
        line = re.sub(r"\(self: [^,]+, ", "(", line)
        line = re.sub(r"\(self: [^)]+\)", "()", line)
        lines[i] = line


def setup(app):
    app.connect("autodoc-process-signature", process_signature)
    app.connect("autodoc-process-docstring", process_docstring)
