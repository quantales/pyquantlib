# pyquantlib/__init__.py
import sys

from .version import __version__

try:
    from ._pyquantlib import *
    from . import _pyquantlib as _ql
except ImportError as e:
    raise ImportError(f"Failed to import PyQuantLib: {e}")

# base = _ql.base
# sys.modules['pyquantlib.base'] = _ql.base

__ql_version__ = _ql.__ql_version__                     # QuantLib C++ version
__ql_hexversion__ = _ql.__ql_hexversion__
__boost_version__ = _ql.__boost_version__               # Boost version used at QuantLib compile-time  

del _ql

# Helpers for readable Boost version
def boost_version_tuple() -> tuple[int, int, int]:
    v = __boost_version__
    return v // 100000, (v // 100) % 1000, v % 100

def boost_version_str() -> str:
    return ".".join(map(str, boost_version_tuple()))
