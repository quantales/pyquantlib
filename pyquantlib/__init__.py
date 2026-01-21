# pyquantlib/__init__.py

from .version import __version__ as __version__

try:
    from . import _pyquantlib as _ql
    from ._pyquantlib import *  # noqa: F403
except ImportError as e:
    raise ImportError(f"Failed to import PyQuantLib: {e}") from e

# base = _ql.base
# sys.modules['pyquantlib.base'] = _ql.base

__ql_version__ = _ql.__ql_version__                     # QuantLib C++ version
__ql_hexversion__ = _ql.__ql_hexversion__
__boost_version__ = _ql.__boost_version__               # Boost version used at QuantLib compile-time

# Export Settings as the singleton instance to allow direct property access:
#   ql.Settings.evaluationDate = date  # Works correctly
Settings = _ql.Settings.instance()

del _ql


# Helpers for readable Boost version
def boost_version_tuple() -> tuple[int, int, int]:
    v = __boost_version__
    return v // 100000, (v // 100) % 1000, v % 100


def boost_version_str() -> str:
    return ".".join(map(str, boost_version_tuple()))
