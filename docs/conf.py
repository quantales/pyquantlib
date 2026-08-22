# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import glob
import json
import glob
import os
import re
import shutil
import sys

# Remove the source tree from sys.path when it holds no compiled _pyquantlib
# extension, so autodoc uses the installed PyPI wheel instead. Without this the
# checkout shadows the wheel and `pyquantlib._pyquantlib` resolves to the
# stubs-only directory, which is empty at runtime. Applies to RTD and to any CI
# runner building from the repo root; a local tree with a built extension is
# left alone.
_src_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if not glob.glob(os.path.join(_src_root, "pyquantlib", "_pyquantlib.*")):
    _norm = os.path.normcase(_src_root)
    sys.path = [p for p in sys.path if os.path.normcase(os.path.abspath(p)) != _norm]

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
    # myst_nb supersedes myst_parser: it registers the same Markdown parser
    # and adds the .ipynb reader. Enabling both raises an extension conflict.
    "myst_nb",
    "sphinx_copybutton",
    "sphinxext.opengraph",
    "sphinxcontrib.mermaid",
]

# -- Options for Mermaid -----------------------------------------------------

# Theme that adapts to Furo's light/dark mode via CSS variables. Mermaid's
# "neutral" theme reads well on both backgrounds.
mermaid_init_js = """
mermaid.initialize({
    startOnLoad: true,
    theme: 'neutral',
    securityLevel: 'loose',
});
"""

# MyST-Parser configuration (for Markdown support)
myst_enable_extensions = [
    "dollarmath",
    "colon_fence",
    "deflist",
    "fieldlist",
    "tasklist",
]
myst_heading_anchors = 3

# -- Options for MyST-NB (notebook rendering) --------------------------------

# Notebooks ship with their outputs committed, so the docs build never executes
# them. Building on Read the Docs installs PyQuantLib from PyPI, which lags the
# source tree; executing there would render outputs from a different version
# than the one being documented. Outputs are refreshed with:
#     jupyter nbconvert --execute --inplace examples/*.ipynb
nb_execution_mode = "off"

# Consecutive stdout writes render as one block rather than one per write.
nb_merge_streams = True

# Source file suffixes. myst-nb parses both Markdown and notebooks, so ".md"
# maps to "myst-nb" rather than myst-parser's "markdown".
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",
    ".ipynb": "myst-nb",
}

# The master toctree document
master_doc = "index"

# Patterns to exclude
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]

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
    # Paths relative to _static; Furo swaps them with its theme toggle.
    # A single SVG with a prefers-color-scheme media query cannot react to
    # the toggle because <img>-embedded SVGs only see the OS preference.
    "light_logo": "wordmark-light.svg",
    "dark_logo": "wordmark-dark.svg",
    "light_css_variables": {
        "color-brand-primary": "#0F766E",   # teal-700
        "color-brand-content": "#0F766E",
    },
    "dark_css_variables": {
        "color-brand-primary": "#2DD4BF",   # teal-400
        "color-brand-content": "#2DD4BF",
    },
}

html_title = "PyQuantLib"
html_short_title = "PyQuantLib"

# Custom static files
html_static_path = ["_static"]
html_css_files = ["custom.css"]

# Favicon (logo is set via light_logo/dark_logo in html_theme_options)
html_favicon = "_static/favicon.svg"

# -- Options for linkcheck ---------------------------------------------------

# Anchor checking is off: GitHub renders heading anchors client-side, so the
# builder reports them missing even when they resolve in a browser.
linkcheck_anchors = False
linkcheck_timeout = 15
linkcheck_retries = 2
linkcheck_ignore = [
    # Published after the docs that reference them, so they 404 until release.
    r"https://pypi\.org/project/pyquantlib/.*",
    # Serves 403 to the checker; the page resolves in a browser.
    r"https://sourceforge\.net/.*",
]

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

# -- Options for OpenGraph (social cards) ------------------------------------

ogp_site_url = "https://pyquantlib.readthedocs.io/"
ogp_site_name = "PyQuantLib"
# Must be a raster image: social platforms do not render SVG previews.
# Regenerate with scripts/make_social_card.py.
ogp_image = "https://pyquantlib.readthedocs.io/en/latest/_static/social-card.png"
ogp_image_alt = "PyQuantLib: Python bindings for QuantLib"
ogp_description_length = 200
ogp_type = "website"
ogp_enable_meta_description = True

# Without an explicit card type, X renders a small thumbnail rather than the
# full-width image.
ogp_custom_meta_tags = [
    '<meta name="twitter:card" content="summary_large_image" />',
]

# -- Options for napoleon (Google/NumPy docstrings) --------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# -- Options for copybutton --------------------------------------------------

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: "
copybutton_prompt_is_regexp = True

# -- Autodoc signature cleanup -----------------------------------------------


# QuantLib's Null<T> sentinels reach pybind11 signatures through their repr,
# e.g. `timeSteps: int = Null<NullSize>()`. The angle brackets are not a
# parseable Python default, so Sphinx gives up on the whole argument list.
# The sentinels mean "unset", which is what None conveys to a Python reader.
_NULL_SENTINEL_RE = re.compile(r"Null<Null\w+>\(\)")


def process_signature(app, what, name, obj, options, signature, return_annotation):
    """Clean up pybind11 signatures."""
    if signature:
        # Remove module paths: pyquantlib._pyquantlib.ClassName -> ClassName
        signature = re.sub(r"pyquantlib\._pyquantlib\.", "", signature)
        signature = _NULL_SENTINEL_RE.sub("None", signature)
        # Remove self parameter
        signature = re.sub(r"\(self: [^,]+, ", "(", signature)
        signature = re.sub(r"\(self: [^)]+\)", "()", signature)
    if return_annotation:
        return_annotation = re.sub(r"pyquantlib\._pyquantlib\.", "", return_annotation)
    return signature, return_annotation


# An enum member named `None` is bound as `None_` to dodge the Python keyword.
# RST reads a trailing underscore as a reference, so `None_` resolves against a
# target named "none" that does not exist. Rendering it as literal text keeps
# the member name visible and stops the lookup.
_ENUM_NONE_RE = re.compile(r"(?<!`)\bNone_(?!`)")

# `|rho|` in prose is RST substitution syntax, not absolute-value bars. Escaping
# the pipes renders them literally.
_PIPE_PAIR_RE = re.compile(r"\|(\w+)\|")


def _separate_indented_blocks(lines):
    """Insert the blank line RST needs after an indented block.

    pybind11 docstrings written as::

        The formula is:
          w(k) = a + b * ...
        where k is the log-moneyness.

    parse as a definition list whose definition ends without a blank line,
    which docutils reports as an unexpected unindent. A blank line before the
    dedented text closes the block cleanly.
    """
    out = []
    for line in lines:
        previous_is_indented = bool(out) and out[-1][:1] in (" ", "\t")
        current_is_flush = line.strip() and not line[:1].isspace()
        if previous_is_indented and current_is_flush:
            out.append("")
        out.append(line)
    return out


def process_docstring(app, what, name, obj, options, lines):
    """Clean up pybind11 overloaded signatures in docstrings."""
    for i, line in enumerate(lines):
        # Remove module paths
        line = re.sub(r"pyquantlib\._pyquantlib\.", "", line)
        # Remove typing. prefix
        line = re.sub(r"typing\.", "", line)
        # Unparseable Null<T> sentinel defaults
        line = _NULL_SENTINEL_RE.sub("None", line)
        # Remove self parameter in overloaded signatures
        line = re.sub(r"\(self: [^,]+, ", "(", line)
        line = re.sub(r"\(self: [^)]+\)", "()", line)
        # Constructs docutils would read as markup rather than text
        line = _ENUM_NONE_RE.sub("``None_``", line)
        line = _PIPE_PAIR_RE.sub(r"\\|\1\\|", line)
        lines[i] = line

    lines[:] = _separate_indented_blocks(lines)


# -- Notebook staging --------------------------------------------------------

# The notebooks live in examples/ at the repository root so they can be run
# directly from a clone. Sphinx can only read sources under docs/, so each one
# is copied into docs/examples/notebooks/ before the build reads the source
# tree. The copies are generated artefacts and are not tracked by git.

_DOCS_DIR = os.path.dirname(__file__)
_NOTEBOOK_SOURCE_DIR = os.path.join(_DOCS_DIR, "..", "examples")
_NOTEBOOK_STAGE_DIR = os.path.join(_DOCS_DIR, "examples", "notebooks")
_NOTEBOOK_SOURCE_URL = "https://github.com/quantales/pyquantlib/blob/main/examples/{name}"


def _source_link_cell(name):
    """Markdown cell linking a rendered notebook back to its source file."""
    return {
        "cell_type": "markdown",
        "id": "pyquantlib-source-link",
        "metadata": {},
        "source": [
            "---\n",
            "\n",
            "[View this notebook on GitHub]({}) to run it locally.".format(
                _NOTEBOOK_SOURCE_URL.format(name=name)
            ),
        ],
    }


def stage_notebooks(app):
    """Copy examples/*.ipynb into the docs tree, appending a source link."""
    if os.path.isdir(_NOTEBOOK_STAGE_DIR):
        shutil.rmtree(_NOTEBOOK_STAGE_DIR)
    os.makedirs(_NOTEBOOK_STAGE_DIR)

    for path in sorted(glob.glob(os.path.join(_NOTEBOOK_SOURCE_DIR, "*.ipynb"))):
        name = os.path.basename(path)
        with open(path, encoding="utf-8") as f:
            notebook = json.load(f)
        notebook["cells"].append(_source_link_cell(name))
        with open(os.path.join(_NOTEBOOK_STAGE_DIR, name), "w", encoding="utf-8") as f:
            json.dump(notebook, f)


def setup(app):
    app.connect("autodoc-process-signature", process_signature)
    app.connect("autodoc-process-docstring", process_docstring)
    app.connect("builder-inited", stage_notebooks)
