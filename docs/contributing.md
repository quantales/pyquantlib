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

## Adding or Updating Bindings

### Workflow

When adding or modifying bindings, follow these steps:

1. **C++ bindings**: Create/update `.cpp` file in `src/`
2. **Tests**: Add tests in `tests/`
3. **Build and verify**: `pip install -e . && pytest`
4. **API docs**: Update examples in `docs/api/` if needed
5. **Stubs**: Maintainer regenerates (contributors skip this step)

### File Checklist

- [ ] Add/update `.cpp` file in appropriate `src/` subdirectory
- [ ] Declare binding function in `include/pyquantlib/pyquantlib.h`
- [ ] Register in module's `all.cpp`
- [ ] Consider hidden handle constructors for classes using handles
- [ ] Add tests in `tests/`
- [ ] Update API docs examples (if user-facing API changed)

### Hidden Handles (Recommended)

For a more Pythonic API, consider adding overloads that accept raw objects instead of handles:

```cpp
// Explicit handle (for power users who need relinking)
.def(py::init<const Handle<Quote>&, const DayCounter&>(), ...)

// Hidden handle (simpler for common use cases)
.def(py::init([](const ext::shared_ptr<Quote>& quote, const DayCounter& dc) {
    return ext::make_shared<MyClass>(Handle<Quote>(quote), dc);
}), py::arg("quote"), py::arg("dayCounter"),
    "Constructs from quote (handle created internally).")
```

When using `Handle<T>` in lambdas, include the header that fully defines `T` so the compiler sees its inheritance to `Observable`. Otherwise MSVC fails with "cannot convert from shared_ptr<T> to shared_ptr<Observable>".

Example includes:
```cpp
#include <ql/quote.hpp>                                   // for Handle<Quote>
#include <ql/termstructures/yieldtermstructure.hpp>       // for Handle<YieldTermStructure>
#include <ql/termstructures/volatility/equityfx/blackvoltermstructure.hpp>  // for Handle<BlackVolTermStructure>
```

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
