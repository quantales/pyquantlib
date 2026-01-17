# Contributing

Contributions to PyQuantLib are welcome!

## Getting Started

For setup instructions, see {doc}`building`.

```bash
git clone https://github.com/quantales/pyquantlib.git
cd pyquantlib
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
pytest
```

## Development Workflow

### Running Tests

```bash
pytest                         # All tests
pytest --cov=pyquantlib        # With coverage
pytest tests/test_date.py      # Specific file
pytest -v                      # Verbose
```

### Linting

```bash
ruff check tests/ pyquantlib/
```

## Adding New Bindings

1. Create `.cpp` file in appropriate `src/` subdirectory
2. Declare binding function in `include/pyquantlib/pyquantlib.h`
3. Register in module's `all.cpp`
4. Add tests in `tests/`

### Example

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

Each file lists its contributors. When adding or substantially modifying a file, add the appropriate copyright line.

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

// If override causes error: remove from trampoline
```

## Type Stubs

After changing bindings, maintainer regenerates stubs:

```bash
python scripts/stubgen.py
```

Contributors should **not** regenerate stubs in PRs.

## Questions?

Open an issue on [GitHub](https://github.com/quantales/pyquantlib/issues).
