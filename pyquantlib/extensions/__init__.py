# PyQuantLib: Python bindings for QuantLib
# Copyright (c) 2025, 2026 Yassine Idyiahia
# Licensed under the BSD 3-Clause License. See LICENSE file for details.

"""
PyQuantLib Extensions: Pure Python implementations for rapid prototyping.

This module provides pricing engines, instruments, and models implemented
in pure Python. These leverage pybind11's ability to subclass C++ abstract
base classes, integrating seamlessly with QuantLib's infrastructure.

Benefits of pure Python extensions:
- Rapid prototyping without C++ compilation
- Easy modification and experimentation
- Full access to QuantLib infrastructure (handles, observers, etc.)
- Comparable performance for closed-form formulas

Example
-------
>>> from pyquantlib.extensions import ModifiedKirkEngine, SviSmileSection
>>> engine = ModifiedKirkEngine(process1, process2, correlation=0.95)
>>> option.setPricingEngine(engine)
>>>
>>> # Pure Python SVI smile - validates against ql.SviSmileSection
>>> smile = SviSmileSection(1.0, 100.0, [0.04, 0.1, 0.3, -0.4, 0.0])
>>> print(smile.volatility(100.0))
"""

from pyquantlib.extensions.modified_kirk_engine import ModifiedKirkEngine
from pyquantlib.extensions.svi_smile_section import (
    SviSmileSection,
    check_svi_parameters,
    svi_total_variance,
)

__all__ = [
    "ModifiedKirkEngine",
    "SviSmileSection",
    "check_svi_parameters",
    "svi_total_variance",
]
