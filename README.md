# PyQuantLib: Modern Python bindings for QuantLib

[![Documentation](https://readthedocs.org/projects/pyquantlib/badge/?version=latest)](https://pyquantlib.readthedocs.io/en/latest/?badge=latest)
[![macOS](https://github.com/quantales/pyquantlib/actions/workflows/macos.yml/badge.svg)](https://github.com/quantales/pyquantlib/actions/workflows/macos.yml)
[![Linux](https://github.com/quantales/pyquantlib/actions/workflows/linux.yml/badge.svg)](https://github.com/quantales/pyquantlib/actions/workflows/linux.yml)
[![Windows](https://github.com/quantales/pyquantlib/actions/workflows/windows.yml/badge.svg)](https://github.com/quantales/pyquantlib/actions/workflows/windows.yml)
[![codecov](https://codecov.io/github/quantales/pyquantlib/graph/badge.svg?token=Q1HNBAK7S1)](https://codecov.io/github/quantales/pyquantlib)
[![PyPI](https://img.shields.io/pypi/v/pyquantlib.svg)](https://pypi.org/project/pyquantlib/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18529027.svg)](https://doi.org/10.5281/zenodo.18529027)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://github.com/quantales/pyquantlib/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/quantales/pyquantlib/blob/main/CONTRIBUTING.md)

## Overview

PyQuantLib provides Python bindings for [QuantLib](https://www.quantlib.org/), the open-source library for quantitative finance. It is built on [pybind11](https://github.com/pybind/pybind11): every binding is written in standard C++, with no interface-definition language and no code-generation step between the caller and the QuantLib source.

As an independent project, PyQuantLib complements the official [QuantLib-SWIG](https://github.com/lballabio/QuantLib-SWIG) bindings, which remain the established and most widely used way to run QuantLib from Python.

## Features

- **Pythonic API**: pass quotes and term structures directly; handles are created internally. Plain Python types convert automatically, and `None` replaces `Null<Real>()`.
- **Zero-copy NumPy**: `Array` and `Matrix` use the buffer protocol, so `np.array(arr, copy=False)` shares memory with no marshalling.
- **Type hints**: complete `.pyi` stubs ship in the wheel for autocomplete and type-checking.
- **Python subclassing**: override QuantLib's abstract base classes via pybind11 trampolines, without C++ recompilation.
- **Modern build**: scikit-build-core, CMake presets, cross-platform CI.

## Installation

```bash
pip install pyquantlib
```

Pre-built wheels are available for Python 3.10 to 3.14 on Linux (x86_64), macOS (ARM), and Windows (x64). QuantLib is statically linked, so no separate installation is required.

### From source

Building from source requires QuantLib 1.44+ compiled with specific CMake flags. Packages from Homebrew, vcpkg, and apt use shared builds and `boost::shared_ptr`, and are not compatible. See [CONTRIBUTING.md](CONTRIBUTING.md) for the required flags and full build instructions.

```bash
pip install git+https://github.com/quantales/pyquantlib.git
```

## Quick start

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
dc         = ql.Actual365Fixed()
risk_free  = ql.FlatForward(today, rate, dc)
dividend   = ql.FlatForward(today, 0.0, dc)
volatility = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)

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

## Module organization

```python
import pyquantlib as ql          # Concrete classes
from pyquantlib.base import ...  # Abstract base classes (for subclassing)
```

Coverage includes dates and calendars, market quotes, yield and volatility term structures, stochastic processes, instruments, and pricing engines. See the [API Reference](https://pyquantlib.readthedocs.io/en/latest/api/index.html) for the complete list.

## Documentation

Full documentation is available at [pyquantlib.readthedocs.io](https://pyquantlib.readthedocs.io/).

| Section | Contents |
|---------|----------|
| [Quickstart](https://pyquantlib.readthedocs.io/en/latest/quickstart.html) | Installation and a first pricing example |
| [Concepts](https://pyquantlib.readthedocs.io/en/latest/concepts/index.html) | Term structures, observables, engines, calibration, and the binding patterns behind them |
| [Cookbook](https://pyquantlib.readthedocs.io/en/latest/cookbook/index.html) | Runnable recipes: curve bootstrapping, volatility surfaces, Heston calibration, NumPy interop |
| [Examples](https://pyquantlib.readthedocs.io/en/latest/examples/index.html) | Jupyter notebooks, also available in [examples/](examples/) |
| [API Reference](https://pyquantlib.readthedocs.io/en/latest/api/index.html) | Every bound class, by module |
| [Architecture](https://pyquantlib.readthedocs.io/en/latest/architecture.html) | Design rationale and internals |
| [Changelog](https://pyquantlib.readthedocs.io/en/latest/changelog.html) | Release history |

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

QuantLib is free software distributed under its own [modified BSD license](https://www.quantlib.org/license.shtml), and is copyright of its respective contributors.
