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

### API Documentation

API docs in `docs/api/` use a consistent 3-level heading structure:

```
# Module Name (h1)
  ## Group Name (h2) - mirrors QuantLib subdirectory
    ### ClassName (h3) - one per class
```

Each class entry uses Sphinx `autoclass` to pull documentation from C++ docstrings:

````markdown
### NewClassName

Brief description (one line).

```{eval-rst}
.. autoclass:: pyquantlib.NewClassName
   :members:
   :undoc-members:
```

```python
# Optional usage example
engine = ql.NewClassName(process)
```
````

| Part | Source |
|------|--------|
| `autoclass` directive | Automated from C++ docstrings |
| Brief description | Manual (one line) |
| Usage examples | Manual (optional) |

For new classes, the minimum required is the `autoclass` directive with a brief description.

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

Docstrings in pybind11 bindings are automatically pulled into the API documentation via Sphinx `autoclass`. Keep them concise:

```cpp
// GOOD
.def("value", &Quote::value, "Returns the current value.")

// AVOID
.def("value", &Quote::value, "This method returns the current value of the quote object.")
```

Class-level docstrings appear in the API reference, so write them as brief descriptions:

```cpp
py::class_<SimpleQuote, Quote, ext::shared_ptr<SimpleQuote>>(
    m, "SimpleQuote", "Simple quote with settable value.")
```

## Common Pitfalls

### Bridge-Pattern Classes

QuantLib's `DayCounter` and `Calendar` use the bridge (pimpl) pattern. Their default constructors create objects with no implementation (null internal pointer). These "empty" objects throw errors when used, e.g., "no day counter implementation provided".

In pybind11 bindings, default argument values are evaluated at module import time. If a binding uses `DayCounter()` as a default, the invalid object is created during import, which can cause import failures if any code path touches it.

**Convention:** Use a concrete default like `Actual365Fixed()` instead:

```cpp
// BAD: Causes import failure
py::arg("dayCounter") = DayCounter()

// GOOD: Concrete default
py::arg("dayCounter") = Actual365Fixed()

// GOOD: Required argument (no default)
py::arg("dayCounter")
```

This convention is used throughout the codebase (`TermStructure`, `YieldTermStructure`, etc.).

### Enum Pass-by-Reference

pybind11 enum values are singletons. Passing them by reference to C++ functions that modify them corrupts the singleton for all subsequent uses in the Python session.

```cpp
// BAD: corrupts enum singleton
.def("check", [](const Foo& self, SomeEnum& e) {
    return self.check(e);  // e modified in place → singleton corrupted
})

// GOOD: pass by value, return tuple with modified value
.def("check", [](const Foo& self, SomeEnum e) {
    bool result = self.check(e);
    return py::make_tuple(result, e);
})
```

```{note}
This behavior is not explicitly documented in pybind11, but is a consequence of how `py::enum_` implements singletons internally. pybind11 v3 introduced `py::native_enum` which uses Python's native `enum` module and is recommended for new bindings. This may behave differently but has not been tested in PyQuantLib.
```

See {doc}`design/enum-singletons` for the full story of how this issue was discovered and debugged.

### Trampoline Classes

See {doc}`internals` for trampoline implementation details and guidelines.

### Error Handling in Tests

PyQuantLib raises two types of exceptions:

| Exception | Source | When |
|-----------|--------|------|
| `RuntimeError` | PyQuantLib wrapper | Validation in the binding code (e.g., invalid RNG type) |
| `ql.Error` | QuantLib internals | QuantLib's own error checks (e.g., invalid parameters) |

```python
# RuntimeError: PyQuantLib wrapper validates input
with pytest.raises(RuntimeError, match="Unsupported RNG type"):
    ql.MCEuropeanEngine(process, "invalid_rng", ...)

# ql.Error: QuantLib validates internally
with pytest.raises(ql.Error, match="two underlyings"):
    ql.StulzEngine(process_array)  # requires exactly 2 processes
```

Use `RuntimeError` for errors thrown in the wrapper code (`std::runtime_error`) and `ql.Error` for errors originating from QuantLib.

## Type Stubs

PyQuantLib includes `.pyi` stub files for IDE autocompletion and type checking. These are generated using `pybind11-stubgen`.

`pybind11-stubgen` produces non-deterministic import ordering across platforms. The same bindings on Windows vs Linux generate identical stubs but with imports in different order:

```python
# Windows might produce:
from pyquantlib._pyquantlib import GeneralizedBlackScholesProcess as BlackScholesMertonProcess
from pyquantlib._pyquantlib import GeneralizedBlackScholesProcess

# Linux might produce:
from pyquantlib._pyquantlib import GeneralizedBlackScholesProcess
from pyquantlib._pyquantlib import GeneralizedBlackScholesProcess as BlackScholesMertonProcess
```

This causes spurious diffs and merge conflicts. To avoid this, the maintainer regenerates stubs on a single platform (Windows) after merging PRs.

Contributors can regenerate stubs locally, but should not include regenerated stubs in pull requests.

```bash
python scripts/stubgen.py
```

```{note}
Stub validation is not included in CI due to the cross-platform non-determinism described above.
```

## Questions?

Open an issue on [GitHub](https://github.com/quantales/pyquantlib/issues).
