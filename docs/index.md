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

PyQuantLib provides Python bindings for [QuantLib](https://www.quantlib.org/), the open-source library for quantitative finance. Unlike the SWIG-based [QuantLib-Python](https://github.com/lballabio/QuantLib-SWIG), PyQuantLib uses [pybind11](https://github.com/pybind/pybind11) for cleaner integration and modern build tooling.

```{warning}
**Alpha Status**: This project is under active development. API may change.
```

## Features

- **Modern build system** — Built with pybind11 and scikit-build-core
- **Cross-platform** — Windows, macOS, and Linux support
- **Type hints** — Full `.pyi` stub files for IDE autocomplete
- **Clean module organization** — Abstract base classes in `pyquantlib.base`

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

- [QuantLib](https://www.quantlib.org/) — Quantitative finance library
- [pybind11](https://github.com/pybind/pybind11) — C++/Python bindings
- [scikit-build-core](https://github.com/scikit-build/scikit-build-core) — Build system
