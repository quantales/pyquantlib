# Architecture

This document describes the internal design of PyQuantLib: useful for contributors and those interested in how the bindings work.

```{seealso}
{doc}`building` for build setup and {doc}`contributing` for development workflow.
```

## Overview

PyQuantLib uses [pybind11](https://github.com/pybind/pybind11) to create Python bindings for QuantLib. The architecture is designed around several key principles:

- **Deferred registration**: Bindings are collected and executed in dependency order
- **Clean namespaces**: Abstract base classes in `pyquantlib.base`, concrete classes in main module
- **Pythonic types**: Native Python objects (`datetime.date`, `numpy.ndarray`) where possible
- **Python extensibility**: Trampoline classes enable subclassing QuantLib ABCs in Python

## Project Structure

```
pyquantlib/
├── include/pyquantlib/
│   ├── binding_manager.h      # Central orchestration
│   ├── trampolines.h          # Python subclassing support
│   ├── pyquantlib.h           # Forward declarations
│   └── type_casters/          # Custom type conversions
│       ├── date.h             # Date ↔ datetime.date
│       └── array.h            # Array ↔ numpy/list
├── src/
│   ├── main.cpp               # Module entry point
│   ├── submodules.cpp         # Creates base submodule
│   ├── time/                  # Time module bindings
│   │   ├── all.cpp            # Aggregates time bindings
│   │   ├── date.cpp
│   │   ├── calendar.cpp
│   │   └── ...
│   ├── core/                  # Core module bindings
│   ├── math/                  # Math module bindings
│   └── ...                    # Other domain modules
└── pyquantlib/
    ├── __init__.py            # Python package init
    └── _pyquantlib/           # Compiled extension
```

## BindingManager

The `BindingManager` class is the central orchestrator for module organization and binding registration.

### Purpose

1. **Submodule management**: Creates and tracks submodules (`pyquantlib.base`)
2. **Deferred execution**: Collects binding functions for ordered execution
3. **sys.modules registration**: Ensures proper Python import behavior
4. **Helper utilities**: Provides `bindHandle<T>` and `bindRelinkableHandle<T>` templates

### Key Methods

```cpp
class BindingManager {
public:
    // Register a binding function for later execution
    void addFunction(void (*register_func)(py::module_&),
                     py::module_& target_module,
                     const std::string& description = "");

    // Create or retrieve a submodule
    py::module_ getOrCreateSubmodule(const std::string& name,
                                     const std::string& doc = "");

    // Execute all registered bindings
    void finalize();
};
```

### Usage Pattern

```cpp
// In main.cpp
BindingManager manager(m, "pyquantlib");

submodules_bindings(manager);   // Creates "base" submodule first
patterns_bindings(manager);     // Observer/Observable (depends on base)
time_bindings(manager);         // Date, Calendar, etc.
// ... other modules

manager.finalize();             // Execute all bindings in order
```

### Convenience Macros

```cpp
// Declare a module binding function
DECLARE_MODULE_BINDINGS(time_bindings);

// Add binding to base submodule
ADD_BASE_BINDING(manager, ql_patterns::observable, "Observable");

// Add binding to main module
ADD_MAIN_BINDING(manager, ql_time::date, "Date");
```

### Why Deferred Execution?

pybind11 requires base classes to be bound before derived classes. The BindingManager solves this by:

1. Collecting all binding functions during module initialization
2. Executing them in the correct order via `finalize()`
3. Providing clear error messages if dependencies fail

## Module Organization

Each QuantLib domain maps to a source directory with a consistent structure.

### Directory Pattern

```
src/quotes/
├── all.cpp              # Module aggregator
├── simplequote.cpp      # Individual class binding
├── derivedquote.cpp
└── compositequote.cpp
```

### Aggregator Pattern (`all.cpp`)

```cpp
#include "pyquantlib/pyquantlib.h"
#include "pyquantlib/binding_manager.h"

DECLARE_MODULE_BINDINGS(quotes_bindings) {
    auto m = manager.module();

    manager.addFunction(ql_quotes::simplequote, m, "SimpleQuote");
    manager.addFunction(ql_quotes::derivedquote, m, "DerivedQuote");
    manager.addFunction(ql_quotes::compositequote, m, "CompositeQuote");
}
```

### Individual Binding Pattern

```cpp
// simplequote.cpp
#include <ql/quotes/simplequote.hpp>
#include <pybind11/pybind11.h>

namespace py = pybind11;

namespace ql_quotes {

void simplequote(py::module_& m) {
    py::class_<QuantLib::SimpleQuote,
               QuantLib::Quote,
               QuantLib::ext::shared_ptr<QuantLib::SimpleQuote>>(
        m, "SimpleQuote", "Quote with a settable value.")
        .def(py::init<QuantLib::Real>(),
             py::arg("value") = 0.0,
             "Creates a SimpleQuote with the given value.")
        .def("setValue", &QuantLib::SimpleQuote::setValue,
             py::arg("value"),
             "Sets the quote value and notifies observers.");
}

}  // namespace ql_quotes
```

### Forward Declarations (`pyquantlib.h`)

All binding functions are declared in a central header:

```cpp
namespace ql_quotes {
    void simplequote(py::module_&);
    void derivedquote(py::module_&);
    void compositequote(py::module_&);
}

namespace ql_time {
    void date(py::module_&);
    void calendar(py::module_&);
    // ...
}
```

## Trampoline Classes

Trampoline classes enable Python code to subclass QuantLib abstract base classes.

### How They Work

pybind11 trampolines intercept virtual method calls and redirect them to Python:

```cpp
class PyQuote : public QuantLib::Quote {
public:
    using QuantLib::Quote::Quote;

    QuantLib::Real value() const override {
        PYBIND11_OVERRIDE_PURE(
            QuantLib::Real,      // Return type
            QuantLib::Quote,     // Parent class
            value,               // Method name
        );
    }

    bool isValid() const override {
        PYBIND11_OVERRIDE_PURE(
            bool,
            QuantLib::Quote,
            isValid,
        );
    }
};
```

### Binding with Trampoline

```cpp
py::class_<QuantLib::Quote,
           PyQuote,                              // Trampoline class
           QuantLib::ext::shared_ptr<QuantLib::Quote>,
           QuantLib::Observable>(
    m, "Quote", "Abstract base class for market quotes.")
    .def(py::init_alias<>());                   // Enables Python subclassing
```

### Python Usage

```python
from pyquantlib.base import Quote

class MyCustomQuote(Quote):
    def __init__(self, value):
        super().__init__()
        self._value = value

    def value(self):
        return self._value

    def isValid(self):
        return self._value is not None
```

### Available Trampolines

Trampolines exist for QuantLib's key abstract base classes: patterns, term structures, instruments, pricing engines, models, and stochastic processes. The list grows as more ABCs are bound.

See `include/pyquantlib/trampolines.h` for the current inventory.

### Trampoline Guidelines

1. **Only virtual methods**: Non-virtual methods bypass the trampoline
2. **Use `override`**: If it doesn't compile with `override`, the method isn't virtual
3. **Trailing comma**: `PYBIND11_OVERRIDE` macros need trailing comma for zero-arg methods (C++20 compatibility)

## Type Casters

Custom type casters enable automatic conversion between Python and C++ types.

### Location

All type casters are included only in `main.cpp`:

```
include/pyquantlib/
└── type_casters/
    ├── date.h             # Date ↔ datetime.date
    └── array.h            # Array ↔ numpy/list
```

### Why No Matrix Type Caster?

Matrix does **not** have a type caster because type casters and `shared_ptr` holders conflict in pybind11. Additionally, the type caster's `cast()` function (C++ to Python) cannot call `py::cast()` without causing infinite recursion.

Instead, Matrix provides constructors that accept numpy arrays and list of lists:

```python
import numpy as np
import pyquantlib as ql

# Create from numpy array
mat = ql.Matrix(np.array([[1, 2], [3, 4]], dtype=float))

# Create from list of lists
mat = ql.Matrix([[1, 2], [3, 4]])
```

### Date Type Caster

Converts between `datetime.date` / `datetime.datetime` and `QuantLib::Date`:

```cpp
template <>
struct type_caster<QuantLib::Date> {
    PYBIND11_TYPE_CASTER(QuantLib::Date, _("QuantLib::Date"));

    // Python → C++
    bool load(py::handle src, bool) {
        py::object datetime = py::module_::import("datetime");
        if (py::isinstance(src, datetime.attr("date")) ||
            py::isinstance(src, datetime.attr("datetime"))) {
            auto dt = py::reinterpret_borrow<py::object>(src);
            int day = dt.attr("day").cast<int>();
            int month = dt.attr("month").cast<int>();
            int year = dt.attr("year").cast<int>();
            value = QuantLib::Date(day, static_cast<QuantLib::Month>(month), year);
            return true;
        }
        return false;
    }

    // C++ → Python
    static handle cast(const QuantLib::Date& d, return_value_policy, handle) {
        py::module_ datetime = py::module_::import("datetime");
        return datetime.attr("date")(d.year(), d.month(), d.dayOfMonth()).release();
    }
};
```

### Array Type Caster

Converts between `list` / `numpy.ndarray` and `QuantLib::Array`:

```cpp
template <>
struct type_caster<QuantLib::Array> {
    PYBIND11_TYPE_CASTER(QuantLib::Array, _("Array"));

    bool load(handle src, bool) {
        // NumPy array
        if (py::isinstance<py::array>(src)) {
            auto np_arr = py::array_t<QuantLib::Real>::ensure(src);
            value = QuantLib::Array(np_arr.size());
            std::memcpy(value.begin(), np_arr.data(),
                np_arr.size() * sizeof(QuantLib::Real));
            return true;
        }

        // Python list/tuple
        if (py::isinstance<py::iterable>(src)) {
            std::vector<QuantLib::Real> temp;
            for (auto item : py::iter(src)) {
                temp.push_back(item.cast<QuantLib::Real>());
            }
            value = QuantLib::Array(temp.begin(), temp.end());
            return true;
        }

        return false;
    }
};
```

### Usage in Python

```python
import pyquantlib as ql
from datetime import date

# datetime.date works where QuantLib::Date is expected
today = date(2025, 6, 15)
ql.Settings.instance().evaluationDate = today  # Automatic conversion

# Lists and numpy arrays work where QuantLib::Array is expected
import numpy as np
arr = ql.Array([1.0, 2.0, 3.0])      # From list
arr = ql.Array(np.array([1, 2, 3]))  # From numpy
```

### Type Casters vs Holders (Why Matrix Has No Type Caster)

Type casters and `shared_ptr` holders are **mutually exclusive** in pybind11. When a type caster is defined for a type, pybind11 treats it as a value type with copy semantics. Attempting to use a holder causes a compilation error:

```
error C2338: static_assert failed: 'Holder classes are only supported for custom types'
```

Additionally, type casters that coexist with `py::class_` bindings face a recursion problem: the `cast()` function (C++ to Python) cannot call `py::cast()` without infinite recursion.

This is why Matrix uses a `shared_ptr` holder and explicit constructors instead of a type caster:

```python
# Matrix requires explicit conversion
mat = ql.Matrix(np.array([[1, 2], [3, 4]], dtype=float))
correlation = ql.Matrix([[1.0, 0.5], [0.5, 1.0]])
```

**When type casters work** (value types without holders):
- `Array`: No holder, type caster works for automatic list/numpy conversion
- `Date`: No holder, type caster works for automatic datetime conversion

**When to use holders instead** (reference types):
- Objects with shared ownership: `Matrix`, `Instrument`, `PricingEngine`, `TermStructure`
- Inheritance hierarchies with Python subclassing
- Objects that maintain identity across the Python/C++ boundary

## Handle Patterns

QuantLib uses `Handle<T>` and `RelinkableHandle<T>` extensively. PyQuantLib provides helper templates for binding these.

### bindHandle Template

```cpp
template <typename T>
auto bindHandle(py::module_& m,
                const std::string& class_name,
                const std::string& doc_string = "") {
    using HandleType = QuantLib::Handle<T>;

    return py::class_<HandleType>(m, class_name.c_str(), doc_string.c_str())
        .def(py::init<>(), "Creates an empty handle.")
        .def(py::init<const QuantLib::ext::shared_ptr<T>&, bool>(),
             py::arg("ptr"), py::arg("registerAsObserver") = true)
        .def("empty", &HandleType::empty)
        .def("__bool__", [](const HandleType& h) { return !h.empty(); })
        .def("currentLink", &HandleType::currentLink)
        .def(py::self == py::self)
        .def(py::self != py::self);
}
```

### bindRelinkableHandle Template

```cpp
template <typename T>
auto bindRelinkableHandle(py::module_& m,
                          const std::string& class_name,
                          const std::string& doc_string = "") {
    using RelinkableHandleType = QuantLib::RelinkableHandle<T>;
    using HandleType = QuantLib::Handle<T>;

    return py::class_<RelinkableHandleType, HandleType>(m, class_name.c_str())
        .def(py::init<>())
        .def(py::init<const QuantLib::ext::shared_ptr<T>&, bool>(),
             py::arg("ptr"), py::arg("registerAsObserver") = true)
        .def("linkTo", &RelinkableHandleType::linkTo,
             py::arg("ptr"), py::arg("registerAsObserver") = true);
}
```

### Usage

```cpp
// In yieldtermstructurehandle.cpp
bindHandle<QuantLib::YieldTermStructure>(
    m, "YieldTermStructureHandle",
    "Handle to a yield term structure.");

// In relinkableyieldtermstructurehandle.cpp
bindRelinkableHandle<QuantLib::YieldTermStructure>(
    m, "RelinkableYieldTermStructureHandle",
    "Relinkable handle to a yield term structure.");
```

## Build System

PyQuantLib uses CMake with scikit-build-core for Python packaging.

### CMake Structure

```cmake
# CMakeLists.txt (simplified)
cmake_minimum_required(VERSION 3.18)
project(pyquantlib)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)
find_package(QuantLib REQUIRED)

# Auto-detect all source files
file(GLOB_RECURSE PYQUANTLIB_SOURCES CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/src/*.cpp"
)

pybind11_add_module(_pyquantlib MODULE ${PYQUANTLIB_SOURCES})

target_link_libraries(_pyquantlib PRIVATE QuantLib::QuantLib)
target_include_directories(_pyquantlib PRIVATE include)
```

Source files are discovered automatically via `GLOB_RECURSE`: just add files to `src/` and they're included in the build.

### QuantLib Requirements

QuantLib must be built as a **static library** with specific flags:

```bash
cmake .. \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DQL_USE_STD_SHARED_PTR=ON
```

This ensures the Settings singleton works correctly (see {doc}`troubleshooting` for details).

### Adding New Bindings

1. Create `src/<module>/<class>.cpp` with binding function
2. Add declaration to `include/pyquantlib/pyquantlib.h`
3. Register in `src/<module>/all.cpp`
4. Add trampoline to `trampolines.h` if ABC

Source files are auto-detected by CMake: no need to edit `CMakeLists.txt`.

## Design Decisions

### Why BindingManager?

- **Dependency ordering**: Base classes must be bound before derived
- **Error isolation**: Clear error messages when bindings fail
- **Submodule management**: Clean separation of ABCs into `pyquantlib.base`

### Why Separate Trampolines Header?

- **Single source of truth**: All trampolines in one place
- **Easier maintenance**: Update virtual methods once
- **Documentation**: Clear inventory of overridable classes

### Why Custom Type Casters?

- **Pythonic API**: Users work with `datetime.date`, not `ql.Date`
- **NumPy integration**: Seamless array interoperability
- **Gradual migration**: Can add more casters without API breaks

### Why Static QuantLib?

- **Singleton correctness**: Prevents duplicate `Settings` instances
- **Simpler deployment**: No dynamic library dependencies
- **Cross-platform consistency**: Same behavior on all platforms
