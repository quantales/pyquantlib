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

## Why PyQuantLib?

There are existing Python bindings for QuantLib:

- **[QuantLib-SWIG](https://github.com/lballabio/QuantLib-SWIG)**: Official bindings using SWIG
- **[PyQL](https://github.com/enthought/pyql)**: Cython-based bindings

Both are excellent projects, but require learning an additional language beyond C++ and Python: SWIG's interface definition language or Cython's Python/C hybrid syntax.

**PyQuantLib uses [pybind11](https://github.com/pybind/pybind11)**: bindings are written in pure C++. If you know C++ and Python, you can read, debug, and contribute to the wrapper code directly.

### Pythonic API

PyQuantLib aims to be a truly Pythonic version of QuantLib, using native Python types where possible:

| QuantLib C++ | PyQuantLib |
|--------------|------------|
| `ql::Date` | `datetime.date` |
| `std::vector<double>` | `list` / `np.ndarray` |
| `ql::Matrix` | `np.ndarray` |
| Handles everywhere | Hidden where possible |

This is achieved via pybind11 type casters and lambda overrides: making the API feel native to Python.

### Rapid Prototyping in Python

Extend QuantLib without touching C++. PyQuantLib exposes abstract base classes with trampoline classes, enabling Python subclassing:

```python
from pyquantlib.base import PricingEngine

class MyCustomEngine(PricingEngine):
    """Prototype new engines in pure Python."""
    
    def calculate(self):
        # Your pricing logic here
        pass
```

No recompilation needed: quants can prototype custom engines, instruments, and processes directly in Python.

### Features

- **Pure C++ and Python**: No SWIG or Cython to learn
- **Full docstrings and type hints**: IDE-friendly with `.pyi` stubs
- **Organized namespaces**: `pyquantlib.base` for ABCs, logical module grouping
- **NumPy integration**: Native array/matrix interoperability
- **Modern tooling**: scikit-build-core, CMake presets, CI/CD ready

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

# Term structures
dc = ql.Actual365Fixed()
risk_free = ql.FlatForward(today, ql.QuoteHandle(rate), dc)
dividend = ql.FlatForward(today, 0.0, dc)
volatility = ql.BlackConstantVol(today, ql.TARGET(), ql.QuoteHandle(vol), dc)

# Black-Scholes process
process = ql.GeneralizedBlackScholesProcess(
    ql.QuoteHandle(spot),
    ql.YieldTermStructureHandle(dividend),
    ql.YieldTermStructureHandle(risk_free),
    ql.BlackVolTermStructureHandle(volatility),
)

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
```

```{toctree}
:maxdepth: 2
:caption: User Guide

examples/index
```

```{toctree}
:maxdepth: 2
:caption: API Reference

api/index
```

```{toctree}
:maxdepth: 2
:caption: Development

architecture
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
