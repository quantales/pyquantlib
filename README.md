# PyQuantLib: Modern Python bindings for QuantLib

[![macOS](https://github.com/quantales/pyquantlib/actions/workflows/macos.yml/badge.svg)](https://github.com/quantales/pyquantlib/actions/workflows/macos.yml)
[![Linux](https://github.com/quantales/pyquantlib/actions/workflows/linux.yml/badge.svg)](https://github.com/quantales/pyquantlib/actions/workflows/linux.yml)
[![Windows](https://github.com/quantales/pyquantlib/actions/workflows/windows.yml/badge.svg)](https://github.com/quantales/pyquantlib/actions/workflows/windows.yml)
[![codecov](https://codecov.io/github/quantales/pyquantlib/graph/badge.svg?token=Q1HNBAK7S1)](https://codecov.io/github/quantales/pyquantlib)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://github.com/quantales/pyquantlib/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/quantales/pyquantlib/blob/main/CONTRIBUTING.md)

> **Alpha Status**: This project is under active development. API may change.

## Overview

PyQuantLib provides Python bindings for [QuantLib](https://www.quantlib.org/), the open-source library for quantitative finance. Unlike the SWIG-based [QuantLib-Python](https://github.com/lballabio/QuantLib-SWIG), PyQuantLib uses [pybind11](https://github.com/pybind/pybind11) for cleaner integration and modern build tooling.

## Features

- **Modern build system** - Built with pybind11 and scikit-build-core
- **Cross-platform** - Windows, macOS, and Linux support
- **Clean module organization** - Abstract base classes in `pyquantlib.base`

## Installation

### Prerequisites

- Python 3.9+
- CMake 3.18+
- C++17 compatible compiler
- Boost headers
- **QuantLib 1.40+** built with `std::shared_ptr` support (see below)

### QuantLib Build Requirement

> **Important**: PyQuantLib requires QuantLib built from source with specific settings.

**Required CMake flags:**

```bash
cmake -DBUILD_SHARED_LIBS=OFF \
      -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
      -DQL_USE_STD_SHARED_PTR=ON \
      -DCMAKE_BUILD_TYPE=Release \
      ...
```

| Flag | Why Required |
|------|--------------|
| `BUILD_SHARED_LIBS=OFF` | Static build prevents Settings singleton issues on Linux/macOS |
| `CMAKE_POSITION_INDEPENDENT_CODE=ON` | Required for static libs in Python modules |
| `QL_USE_STD_SHARED_PTR=ON` | pybind11 uses `std::shared_ptr` as default holder |

**Note**: Pre-built packages (Homebrew, vcpkg, apt) use shared builds and `boost::shared_ptr` — they are **not compatible**. You must build QuantLib from source. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed build instructions.

### From Source

```bash
# After building QuantLib with required flags (see CONTRIBUTING.md)
pip install git+https://github.com/quantales/pyquantlib.git
```

## Quick Start

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

print(f"NPV:   {option.NPV():.4f}")
print(f"Delta: {option.delta():.4f}")
print(f"Gamma: {option.gamma():.4f}")
print(f"Vega:  {option.vega():.4f}")
print(f"Theta: {option.theta():.4f}")
```

Output:
```
NPV:   10.4506
Delta: 0.6368
Gamma: 0.0188
Vega:  37.5240
Theta: -6.4140
```

## Module Organization

```python
import pyquantlib as ql

# Time
ql.Date, ql.Period, ql.Calendar, ql.Schedule, ql.DayCounter

# Market data
ql.SimpleQuote, ql.QuoteHandle

# Term structures
ql.FlatForward, ql.ZeroCurve, ql.BlackConstantVol, ql.BlackVarianceSurface

# Processes
ql.GeneralizedBlackScholesProcess, ql.HestonProcess

# Instruments
ql.VanillaOption, ql.BasketOption

# Pricing engines
ql.AnalyticEuropeanEngine, ql.MCEuropeanEngine, ql.AnalyticHestonEngine

# Abstract base classes (for subclassing)
from pyquantlib.base import Observer, Observable, LazyObject
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

```bash
# Clone and install in development mode
git clone https://github.com/quantales/pyquantlib.git
cd pyquantlib
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .

# Run tests
pytest
```

## License

BSD 3-Clause License. See [LICENSE](LICENSE) for details.

## Acknowledgments

- [QuantLib](https://www.quantlib.org/) - Quantitative finance library
- [pybind11](https://github.com/pybind/pybind11) - C++/Python bindings
- [scikit-build-core](https://github.com/scikit-build/scikit-build-core) - Build system

## Status

PyQuantLib is in early development. For broader QuantLib coverage today, use [QuantLib-SWIG](https://github.com/lballabio/QuantLib-SWIG).
