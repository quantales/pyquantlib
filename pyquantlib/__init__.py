# pyquantlib/__init__.py

from .version import __version__ as __version__

try:
    from . import _pyquantlib as _ql
    from ._pyquantlib import *  # noqa: F403
except ImportError as e:
    raise ImportError(f"Failed to import PyQuantLib: {e}") from e

# base = _ql.base
# sys.modules['pyquantlib.base'] = _ql.base

QL_VERSION = _ql.QL_VERSION                 # QuantLib C++ version
QL_VERSION_HEX = _ql.QL_VERSION_HEX         # QuantLib hex version for comparison
BOOST_VERSION = _ql.BOOST_VERSION           # Boost version (compile-time integer)

# Export Settings as the singleton instance to allow direct property access:
#   ql.Settings.evaluationDate = date  # Works correctly
Settings = _ql.Settings.instance()

del _ql


# Helpers for readable Boost version
def boost_version_tuple() -> tuple[int, int, int]:
    v = BOOST_VERSION
    return v // 100000, (v // 100) % 1000, v % 100


def boost_version_str() -> str:
    return ".".join(map(str, boost_version_tuple()))
