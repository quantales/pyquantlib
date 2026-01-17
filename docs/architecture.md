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
│   └── pyquantlib.h           # Forward declarations
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

## Implicit Conversion

PyQuantLib uses `py::implicitly_convertible` to enable seamless Python/C++ type conversion.

### Date: Implicit Conversion

`Date` uses `py::implicitly_convertible` to allow passing `datetime.date` or `datetime.datetime` directly to functions:

```python
from datetime import date
import pyquantlib as ql

# All work identically
d1 = date(2024, 5, 1)
d2 = date(2024, 5, 10)
delta = ql.daysBetween(d1, d2)  # datetime.date accepted directly
delta = ql.daysBetween(ql.Date(d1), ql.Date(d2))  # explicit also works
```

This is implemented via a constructor that accepts `py::object` (duck-typed for date attributes), plus:

```cpp
py::implicitly_convertible<py::object, QuantLib::Date>();
```

### Array: Implicit Conversion

`Array` uses `py::implicitly_convertible` to allow passing lists and numpy arrays directly to functions:

```python
import pyquantlib as ql
import numpy as np

# All work identically
result = ql.DotProduct(ql.Array([1, 2, 3]), ql.Array([4, 5, 6]))
result = ql.DotProduct([1, 2, 3], [4, 5, 6])
result = ql.DotProduct(np.array([1, 2, 3]), np.array([4, 5, 6]))
```

This is implemented via constructors that accept `py::list` and `py::array`, plus:

```cpp
py::implicitly_convertible<py::list, Array>();
py::implicitly_convertible<py::array, Array>();
```

### Matrix: Implicit Conversion

`Matrix` also uses `py::implicitly_convertible` to allow passing 2D lists and numpy arrays directly to functions:

```python
import pyquantlib as ql
import numpy as np

# All work identically
result = ql.transpose(ql.Matrix([[1, 2], [3, 4]]))
result = ql.transpose([[1, 2], [3, 4]])
result = ql.transpose(np.array([[1, 2], [3, 4]]))
```

This is implemented via constructors that accept `py::list` and `py::array`, plus:

```cpp
py::implicitly_convertible<py::list, Matrix>();
py::implicitly_convertible<py::array, Matrix>();
```

### Summary

| Type | Binding | Automatic Conversion |
|------|---------|---------------------|
| Date | `py::class_` + `implicitly_convertible<py::object>` | Yes |
| Array | `py::class_` + `implicitly_convertible<py::list/array>` + buffer protocol | Yes |
| Matrix | `py::class_` + `implicitly_convertible<py::list/array>` + buffer protocol | Yes |

### Buffer Protocol vs Implicit Conversion

These two pybind11 mechanisms achieve similar user experiences but work very differently under the hood.

#### Implicit Conversion (Copy)

`py::implicitly_convertible` is a **conversion bridge** that creates a new object by copying data:

```cpp
py::implicitly_convertible<py::list, Array>();
```

When pybind11 sees a Python list but needs a `QuantLib::Array`, it calls the registered constructor, allocating new memory and copying values.

**Characteristics:**
- Creates a new C++ object (copy)
- One-way: Python input → new C++ object
- Changes to one do not affect the other
- Cost: proportional to data size

**Best for:** Value types like `Date`, small structs, or when memory layouts differ (e.g., `datetime.date` vs `QuantLib::Date`).

#### Buffer Protocol (Zero-Copy)

The buffer protocol is a **memory window** that shares memory between Python and C++:

```cpp
pyArray.def_buffer([](Array& a) -> py::buffer_info {
    return py::buffer_info(a.begin(), sizeof(Real), ...);
});
```

This tells Python: "This C++ object has a block of memory here. You can wrap a NumPy array around this exact address."

**Characteristics:**
- No data copying (shares memory)
- Two-way: modifications in Python affect C++ and vice versa
- Cost: near zero (just pointer passing)
- Requires compatible memory layouts

**Best for:** Container types like arrays, matrices, images.

#### PyQuantLib's Approach

**Array** uses both mechanisms:

```python
# BUFFER PROTOCOL (zero-copy): QuantLib → NumPy
ql_arr = ql.Array([1, 2, 3])
np_view = np.array(ql_arr, copy=False)  # Shares memory, instant
np_view[0] = 99  # Modifies ql_arr too!

# IMPLICIT CONVERSION (copy): Python → QuantLib
result = ql.DotProduct([1, 2, 3], [4, 5, 6])  # Creates temporary Arrays
```

The copy on input is unavoidable because QuantLib functions expect `QuantLib::Array`, not `numpy.ndarray`. For performance-critical code with large arrays, work directly with `ql.Array` objects to avoid repeated conversions.

**Date** uses only implicit conversion because `datetime.date` and `QuantLib::Date` have completely different memory layouts. Since dates are small (just 3 integers), the copy is instant.

**Matrix** uses only buffer protocol (no implicit conversion) because `shared_ptr` holders and `implicitly_convertible` conflict in pybind11.

#### Comparison

| Aspect | Implicit Conversion | Buffer Protocol |
|--------|---------------------|-----------------|
| Mechanism | Calls constructor | Exposes raw memory |
| Data access | Copy (new object) | Reference (shared memory) |
| Speed | Slower for large data | Instant (zero-copy) |
| Sync | Changes independent | Changes affect both |
| Direction | Python → C++ | Bidirectional |
| Used by | `Date`, `Array`, `Matrix` (input) | `Array`, `Matrix` (output) |

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

### Why Implicit Conversion?

- **Pythonic API**: Users work with `datetime.date`, lists, and numpy arrays directly
- **NumPy integration**: Seamless array and matrix interoperability
- **Gradual adoption**: Can add more conversions without API breaks

### Why Static QuantLib?

- **Singleton correctness**: Prevents duplicate `Settings` instances
- **Simpler deployment**: No dynamic library dependencies
- **Cross-platform consistency**: Same behavior on all platforms
