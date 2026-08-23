---
hide-toc: true
# Both descriptions are set explicitly because the badges directly under the
# title would otherwise be scraped into the auto-generated summary.
"og:description": "Python bindings for QuantLib, the open-source library for quantitative finance. Built on pybind11, with no interface-definition layer."
myst:
  html_meta:
    "description": "Python bindings for QuantLib, the open-source library for quantitative finance. Built on pybind11, with no interface-definition layer."
---

# PyQuantLib

**Python bindings for [QuantLib](https://www.quantlib.org/), the open-source library for quantitative finance.**

```{image} https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
:alt: License
:target: https://github.com/quantales/pyquantlib/blob/main/LICENSE
```
```{image} https://img.shields.io/badge/Python-3.10%2B-blue.svg
:alt: Python
:target: https://www.python.org/downloads/
```
```{image} https://img.shields.io/badge/QuantLib-1.43%2B-0F766E.svg
:alt: QuantLib
:target: https://www.quantlib.org/
```

PyQuantLib is built on [pybind11](https://github.com/pybind/pybind11): every binding is written in standard C++, with no interface-definition language and no code-generation step between the caller and the QuantLib source. It is designed for rapid prototyping in Python, backed by QuantLib's C++ implementation.

As an independent project, PyQuantLib complements the official [QuantLib-SWIG](https://github.com/lballabio/QuantLib-SWIG) bindings, which remain the established and most widely used way to run QuantLib from Python.

## Key features

- **Pythonic API**: pass quotes and term structures directly; handles are created internally. Plain Python types convert automatically. `None` instead of `Null<Real>()`.
- **Zero-copy NumPy**: `Array` and `Matrix` use the buffer protocol. `np.array(arr, copy=False)` shares memory; no overhead, no marshalling.
- **Type-safe and IDE-friendly**: signature mismatches fail at compile time. Full `.pyi` stubs ship in the wheel for autocomplete and type-checking.
- **Subclass in Python**: override QuantLib's abstract base classes via pybind11 trampolines. Prototype custom engines without C++ recompilation.

See {doc}`architecture` for the design rationale behind these features.

## Quick example

```python
import pyquantlib as ql

# Set evaluation date
today = ql.Date(15, 6, 2025)
ql.Settings.evaluationDate = today

# Market data
spot = ql.SimpleQuote(100.0)
rate = ql.SimpleQuote(0.05)
vol  = ql.SimpleQuote(0.20)

# Term structures (pass quotes directly; handles created internally)
dc           = ql.Actual365Fixed()
risk_free    = ql.FlatForward(today, rate, dc)
dividend     = ql.FlatForward(today, 0.0, dc)
volatility   = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)

# Black-Scholes process
process = ql.GeneralizedBlackScholesProcess(spot, dividend, risk_free, volatility)

# European call option, 1 year to expiry
payoff   = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
option   = ql.VanillaOption(payoff, exercise)

# Price with analytic Black-Scholes
option.setPricingEngine(ql.AnalyticEuropeanEngine(process))

print(f"NPV:   {option.NPV():.4f}")    # 10.4506
print(f"Delta: {option.delta():.4f}")  # 0.6368
print(f"Gamma: {option.gamma():.4f}")  # 0.0188
print(f"Vega:  {option.vega():.4f}")   # 37.5240
print(f"Theta: {option.theta():.4f}")  # -6.4140
```

## Performance

pybind11 provides a thin C++/Python boundary. Function calls dispatch directly to QuantLib's C++ implementation, with no runtime code generation or reflection. In practice, the dominant cost in typical QuantLib usage (pricing, curve construction, calibration) remains the C++ computation, not the binding layer. Where applicable, PyQuantLib supports {doc}`zero-copy data exchange <numpy>` with NumPy arrays.

As with any Python binding, performance-critical loops should remain in C++. PyQuantLib exposes QuantLib's APIs efficiently while preserving Python's productivity for orchestration, configuration, and analysis.

## Links

- **GitHub**: [github.com/quantales/pyquantlib](https://github.com/quantales/pyquantlib)
- **QuantLib**: [quantlib.org](https://www.quantlib.org/)
- **Issues**: [Report a bug](https://github.com/quantales/pyquantlib/issues)
- **License**: BSD 3-Clause (see [LICENSE](https://github.com/quantales/pyquantlib/blob/main/LICENSE))

```{toctree}
:hidden:
:caption: Getting Started

installation
quickstart
building
```

```{toctree}
:hidden:
:caption: User Guide

numpy
handles
extending
examples/index
```

```{toctree}
:hidden:
:caption: Concepts

concepts/index
```

```{toctree}
:hidden:
:caption: Cookbook

cookbook/index
```

```{toctree}
:hidden:
:caption: API Reference

api/index
```

```{toctree}
:hidden:
:caption: Architecture

architecture
```

```{toctree}
:hidden:
:caption: Contributing & Internals

contributing
internals
troubleshooting
changelog
```
