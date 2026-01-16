# Contributing

Thank you for your interest in contributing to PyQuantLib!

## Development Setup

For detailed setup instructions, see the {doc}`installation` guide.

### Quick Start

```bash
# Clone
git clone https://github.com/quantales/pyquantlib.git
cd pyquantlib

# Virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install
pip install -r requirements-dev.txt
pip install -e .

# Test
pytest
```

## Development Workflow

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=pyquantlib

# Specific file
pytest tests/test_date.py

# Verbose
pytest -v
```

### Linting

```bash
ruff check tests/ pyquantlib/
```

### Building Documentation

```bash
# Install docs dependencies (first time only)
pip install -e ".[docs]"

# Build HTML docs
cd docs
sphinx-build -b html . _build/html

# View locally
# Windows:
start _build/html/index.html
# macOS:
open _build/html/index.html
# Linux:
xdg-open _build/html/index.html
```

Or use the convenience script:

```bash
python scripts/build_docs.py
```

### Building Wheels

```bash
python -m build
# Output in dist/
```

## Adding New Bindings

1. Create `.cpp` file in appropriate `src/` subdirectory
2. Declare binding function in `include/pyquantlib/pyquantlib.h`
3. Register in module's `all.cpp`
4. Add tests in `tests/`

### Example Binding

```cpp
// src/quotes/simplequote.cpp
#include <ql/quotes/simplequote.hpp>
#include <pybind11/pybind11.h>
#include "pyquantlib/binding_manager.h"

namespace py = pybind11;
using namespace QuantLib;

void bind_simplequote(BindingManager& manager) {
    py::class_<SimpleQuote, Quote, ext::shared_ptr<SimpleQuote>>(
        manager.getModule(), "SimpleQuote", "Simple quote with settable value.")
        .def(py::init<Real>(), py::arg("value") = 0.0)
        .def("setValue", &SimpleQuote::setValue, py::arg("value"))
        .def("reset", &SimpleQuote::reset);
}
```

## Code Conventions

### File Headers

Every `.cpp` and `.h` file needs:

```cpp
/*
 * PyQuantLib: Python bindings for QuantLib
 * Copyright (c) 2025 Yassine Idyiahia
 *
 * QuantLib is Copyright (c) 2000-2025 The QuantLib Authors
 * QuantLib is free software under a modified BSD license.
 * See http://quantlib.org/ for more information.
 *
 * Source: https://github.com/quantales/pyquantlib
 * Licensed under the BSD 3-Clause License. See LICENSE file for details.
 */
```

### Includes

```cpp
// GOOD: Specific headers
#include <ql/quotes/simplequote.hpp>
#include <ql/time/date.hpp>

// BAD: Avoid umbrella header
#include <ql/quantlib.hpp>
```

### Docstrings

Keep concise:

```cpp
// GOOD
.def("value", &Quote::value, "Returns the current value.")

// AVOID
.def("value", &Quote::value, "This method returns the current value of the quote object.")
```

## Common Pitfalls

### Bridge-Pattern Classes

QuantLib's `DayCounter` and `Calendar` have empty default constructors that create invalid objects.

```cpp
// BAD: Causes import failure
py::arg("dayCounter") = DayCounter()

// GOOD: Use concrete default
py::arg("dayCounter") = Actual365Fixed()
```

### Enum Pass-by-Reference

Never pass enums by reference:

```cpp
// BAD
.def("check", [](const Foo& self, SomeEnum& e) { ... })

// GOOD
.def("check", [](const Foo& self, SomeEnum e) { ... })
```

### Trampoline Classes

Only include **virtual** methods. Use `override` to verify:

```cpp
// If this compiles, method is virtual: keep it
Date date() const override {
    PYBIND11_OVERRIDE_PURE(Date, Coupon, date,);
}

// If override causes error, method is non-virtual: remove it
```

## Type Stubs

After changing bindings, maintainer regenerates stubs:

```bash
python scripts/stubgen.py
```

Contributors should **not** regenerate stubs in PRs.

## Questions?

Open an issue on [GitHub](https://github.com/quantales/pyquantlib/issues).
