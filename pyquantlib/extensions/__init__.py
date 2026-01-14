"""
PyQuantLib Extensions: Pure Python implementations for rapid prototyping.

This module provides pricing engines, instruments, and models implemented
in pure Python. These leverage pybind11's ability to subclass C++ abstract
base classes, integrating seamlessly with QuantLib's infrastructure.

Example
-------
>>> from pyquantlib.extensions import ModifiedKirkEngine
>>> engine = ModifiedKirkEngine(process1, process2, correlation=0.95)
>>> option.setPricingEngine(engine)
"""

from pyquantlib.extensions.modified_kirk_engine import ModifiedKirkEngine

__all__ = [
    "ModifiedKirkEngine",
]
