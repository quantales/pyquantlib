# PyQuantLib: Modern Python bindings for QuantLib

[![macOS](https://github.com/quantales/pyquantlib/actions/workflows/macos.yml/badge.svg)](https://github.com/quantales/pyquantlib/actions/workflows/macos.yml)
[![Linux](https://github.com/quantales/pyquantlib/actions/workflows/linux.yml/badge.svg)](https://github.com/quantales/pyquantlib/actions/workflows/linux.yml)
[![Windows](https://github.com/quantales/pyquantlib/actions/workflows/windows.yml/badge.svg)](https://github.com/quantales/pyquantlib/actions/workflows/windows.yml)
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

> ⚠️ **Important**: PyQuantLib requires QuantLib compiled with `std::shared_ptr` for pybind11 compatibility.

QuantLib must be built from source with:

```bash
cmake -DQL_USE_STD_SHARED_PTR=ON \
      -DCMAKE_BUILD_TYPE=Release \
      ...
```

As of QuantLib 1.40, `QL_USE_STD_OPTIONAL` and `QL_USE_STD_ANY` are ON by default. Only `QL_USE_STD_SHARED_PTR` needs explicit activation (QuantLib defaults to `boost::shared_ptr`).

**Note**: Pre-built packages (Homebrew, vcpkg, apt) use default settings and are **not compatible**. You must build QuantLib from source. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed build instructions.

### From Source

```bash
# After building QuantLib with required flags (see CONTRIBUTING.md)
pip install git+https://github.com/quantales/pyquantlib.git
```

## Quick Start

```python
import pyquantlib as ql

# Create dates
today = ql.Date(15, ql.June, 2025)
maturity = today + ql.Period(1, ql.Years)

# Calendar and day counter
calendar = ql.TARGET()
day_counter = ql.Actual365Fixed()

# Build a schedule
schedule = ql.MakeSchedule() \
    .fromDate(today) \
    .to(maturity) \
    .withCalendar(calendar) \
    .withFrequency(ql.Quarterly) \
    .value()

# Iterate over schedule dates
for date in schedule:
    print(date)
```

## Module Organization

```python
# Main module
from pyquantlib import Date, Period, Calendar, Schedule, DayCounter

# Abstract base classes - for subclassing
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
