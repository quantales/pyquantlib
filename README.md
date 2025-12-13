# PyQuantLib: Modern Python bindings for QuantLib

[![macOS](https://github.com/quantales/pyquantlib/actions/workflows/macos.yml/badge.svg)](https://github.com/quantales/pyquantlib/actions/workflows/macos.yml)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://github.com/quantales/pyquantlib/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/quantales/pyquantlib/blob/main/CONTRIBUTING.md)

> ⚠️ **Alpha Status**: This project is under active development. API may change.

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

> ⚠️ **Important**: PyQuantLib requires QuantLib compiled with specific flags for pybind11 compatibility.

QuantLib must be built from source with:

```bash
cmake -DQL_USE_STD_SHARED_PTR=ON \
      -DQL_USE_STD_OPTIONAL=ON \
      -DQL_USE_STD_ANY=ON \
      -DCMAKE_BUILD_TYPE=Release \
      ...
```

The `QL_USE_STD_SHARED_PTR=ON` flag is **required** because pybind11 uses `std::shared_ptr` as its default holder type. Using QuantLib's default (`boost::shared_ptr`) will cause runtime errors or segmentation faults.

**Note**: Pre-built packages (Homebrew, vcpkg, apt) use default settings and are **not compatible**. You must build QuantLib from source. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed build instructions.

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

# Create market data
spot = ql.SimpleQuote(100.0)
rate = ql.SimpleQuote(0.05)
vol = ql.SimpleQuote(0.20)

# Build term structures
day_counter = ql.Actual365Fixed()
risk_free_ts = ql.FlatForward(today, ql.QuoteHandle(rate), day_counter)
vol_ts = ql.BlackConstantVol(today, ql.TARGET(), ql.QuoteHandle(vol), day_counter)
dividend_ts = ql.FlatForward(today, 0.0, day_counter)

# Create Black-Scholes process
process = ql.GeneralizedBlackScholesProcess(
    ql.QuoteHandle(spot),
    ql.YieldTermStructureHandle(dividend_ts),
    ql.YieldTermStructureHandle(risk_free_ts),
    ql.BlackVolTermStructureHandle(vol_ts)
)

# Price a European call option
payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
exercise = ql.EuropeanExercise(today + ql.Period(1, ql.Years))
option = ql.VanillaOption(payoff, exercise)

engine = ql.AnalyticEuropeanEngine(process)
option.setPricingEngine(engine)

print(f"NPV: {option.NPV():.4f}")
print(f"Delta: {option.delta():.4f}")
print(f"Gamma: {option.gamma():.4f}")
print(f"Vega: {option.vega():.4f}")
```

## Module Organization

```python
# Concrete classes - main module
from pyquantlib import Date, SimpleQuote, Period, VanillaOption

# Abstract base classes - for subclassing
from pyquantlib.base import Observer, Observable, Instrument
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

PyQuantLib is in early development. Current coverage includes:

- ✅ Date, Period, Calendar, Schedule
- ✅ Quotes (Simple, Derived, Composite)
- ✅ Term structures (Yield, Volatility)
- ✅ Black-Scholes and Heston processes
- ✅ Vanilla option pricing (Analytic, Monte Carlo)
- 🔄 More instruments and models in progress

For broader QuantLib coverage today, use [QuantLib-SWIG](https://github.com/lballabio/QuantLib-SWIG).
