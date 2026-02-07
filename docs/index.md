# PyQuantLib Documentation

```{image} https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
:alt: License
:target: https://github.com/quantales/pyquantlib/blob/main/LICENSE
```
```{image} https://img.shields.io/badge/Python-3.9%2B-blue.svg
:alt: Python
:target: https://www.python.org/downloads/
```

**Modern Python bindings for QuantLib**

PyQuantLib provides Python bindings for [QuantLib](https://www.quantlib.org/), the open-source library for quantitative finance.

```{warning}
**Alpha Status**: This project is under active development. API may change.
```

## Motivation

There are existing Python bindings for QuantLib:

* **[QuantLib-SWIG](https://github.com/lballabio/QuantLib-SWIG)**: official bindings generated using SWIG
* **[PyQL](https://github.com/enthought/pyql)**: bindings implemented using Cython

Both are mature projects. However, they introduce an additional language beyond C++ and Python: SWIG's interface definition language or Cython's hybrid syntax. This increases cognitive load when navigating binding code or keeping wrappers in sync with upstream QuantLib.

PyQuantLib is built on [pybind11](https://github.com/pybind/pybind11), with all bindings written in standard C++. The wrapper code directly exposes QuantLib's C++ APIs, with no intermediate DSL or code generation step.

### Pythonic API

Pass Python types directly to functions:

```python
result = ql.DotProduct([1, 2, 3], [4, 5, 6])
transposed = ql.transpose([[1, 2], [3, 4]])
date = ql.Date(15, ql.June, 2025)  # or datetime.date(2025, 6, 15)
```

### Zero-Copy NumPy Integration

Buffer protocol for efficient, bidirectional data exchange:

```python
arr = ql.Array([1, 2, 3, 4, 5])
np_view = np.array(arr, copy=False)  # shared memory, no copy
```

### Developer Experience

* No additional language beyond C++ and Python (no SWIG, no Cython)
* Type-safe bindings resolved at compile time (signature mismatches fail at build, not runtime)
* Debugging with standard C++ tools (no generated code obscuring the call stack)
* Wrapper code mirrors QuantLib headers and class structure
* IDE autocompletion via `.pyi` type stubs

## Performance

PyQuantLib uses pybind11, which provides a thin, low-overhead C++/Python boundary. Function calls are dispatched directly to QuantLib's C++ implementation, with no runtime code generation or reflection.

In practice, the dominant cost in typical QuantLib usage (pricing, curve construction, calibration) remains the underlying C++ computation, not the binding layer. Where applicable, PyQuantLib supports {doc}`zero-copy data exchange <numpy>` with NumPy arrays.

As with any Python binding, performance-critical loops should remain in C++. PyQuantLib is designed to expose QuantLib's APIs efficiently, while preserving Python's productivity for orchestration, configuration, and analysis.

## Features

* **Pythonic API**: Implicit conversion, {doc}`hidden handles <handles>`, native `datetime.date`
* **NumPy integration**: {doc}`Zero-copy data exchange <numpy>` via buffer protocol
* **Type hints**: IDE-friendly with complete `.pyi` stubs
* **Python subclassing**: Extend QuantLib classes without C++ recompilation
* **Modern tooling**: {doc}`scikit-build-core <building>`, CMake presets, CI/CD ready

## Quick Example

```python
import pyquantlib as ql

# Set evaluation date
today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today

# Market data
spot = ql.SimpleQuote(100.0)
rate = ql.SimpleQuote(0.05)
vol = ql.SimpleQuote(0.20)

# Term structures (pass quotes directly, handles created internally)
dc = ql.Actual365Fixed()
risk_free = ql.FlatForward(today, rate, dc)
dividend = ql.FlatForward(today, 0.0, dc)
volatility = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)

# Black-Scholes process (pass objects directly)
process = ql.GeneralizedBlackScholesProcess(spot, dividend, risk_free, volatility)

# European call option
payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
option = ql.VanillaOption(payoff, exercise)

# Price with analytic Black-Scholes
option.setPricingEngine(ql.AnalyticEuropeanEngine(process))

print(f"NPV:   {option.NPV():.4f}")    # 10.4506
print(f"Delta: {option.delta():.4f}")  # 0.6368
print(f"Gamma: {option.gamma():.4f}")  # 0.0188
print(f"Vega:  {option.vega():.4f}")   # 37.5240
print(f"Theta: {option.theta():.4f}")  # -6.4140
```

## Documentation

```{toctree}
:maxdepth: 2
:caption: Getting Started

installation
quickstart
building
```

```{toctree}
:maxdepth: 2
:caption: User Guide

numpy
handles
extending
examples/index
```

```{toctree}
:maxdepth: 2
:caption: API Reference

api/index
```

```{toctree}
:maxdepth: 2
:caption: Architecture

architecture
internals
design/index
```

```{toctree}
:maxdepth: 2
:caption: Development

contributing
troubleshooting
changelog
```

## Links

- **GitHub**: [github.com/quantales/pyquantlib](https://github.com/quantales/pyquantlib)
- **QuantLib**: [quantlib.org](https://www.quantlib.org/)
- **Issues**: [Report a bug](https://github.com/quantales/pyquantlib/issues)

## License

BSD 3-Clause License. See [LICENSE](https://github.com/quantales/pyquantlib/blob/main/LICENSE) for details.

## Acknowledgments

- [QuantLib](https://www.quantlib.org/): Quantitative finance library
- [pybind11](https://github.com/pybind/pybind11): C++/Python bindings
- [scikit-build-core](https://github.com/scikit-build/scikit-build-core): Build system
