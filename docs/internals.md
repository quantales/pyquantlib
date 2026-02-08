# Internals

Implementation reference for PyQuantLib's binding infrastructure: the BindingManager API, module patterns, trampoline implementation, and handle templates.

```{seealso}
{doc}`architecture` for high-level design and rationale, {doc}`extending` for the Python subclassing guide, {doc}`contributing` for development workflow.
```

## BindingManager

The `BindingManager` class is the central orchestrator for module organization and binding registration.

### Purpose

1. **Two-phase initialization**: Collects binding functions first, executes them all via `finalize()`
2. **Submodule management**: Creates and tracks submodules (`pyquantlib.base`)
3. **Error isolation**: Wraps each binding execution in try/catch with descriptive error messages
4. **sys.modules registration**: Ensures proper Python import behavior
5. **Helper utilities**: Provides `bindHandle<T>` and `bindRelinkableHandle<T>` templates

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

// Ordering is manual: modules listed in dependency order.
// patterns before quotes (Observable before Quote),
// quotes before instruments (Quote before Instrument), etc.
submodules_bindings(manager);   // Creates "base" submodule first
patterns_bindings(manager);     // Observer/Observable
time_bindings(manager);         // Date, Calendar, etc.
// ... other modules

manager.finalize();             // Execute all bindings in insertion order
```

### Ordering

`finalize()` executes binding functions in insertion order. There is no automatic dependency resolution -- the developer is responsible for arranging modules in `main.cpp` and classes within each `all.cpp` so that base classes are registered before derived classes.

In practice, module boundaries do most of the work. `patterns_bindings` (Observable) naturally runs before `quotes_bindings` (Quote) because the listing in `main.cpp` follows the inheritance hierarchy. Within each `all.cpp`, the entries are short enough to order by inspection.

When the ordering is wrong, pybind11 raises an error at import time. The BindingManager's error isolation identifies the failing binding by its description string, making it straightforward to diagnose and fix by reordering.

### Convenience Macros

```cpp
// Declare a module binding function
DECLARE_MODULE_BINDINGS(time_bindings);

// Add binding to base submodule
ADD_BASE_BINDING(ql_patterns::observable, "Observable");

// Add binding to main module
ADD_MAIN_BINDING(ql_time::date, "Date");
```

## Module Patterns

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

Trampoline classes enable Python code to subclass QuantLib abstract base classes. See {doc}`extending` for the user-facing documentation.

### Implementation

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

### Guidelines for Contributors

1. **Only virtual methods**: Non-virtual methods cannot be overridden from Python. C++ calls bypass the trampoline and go directly to the base class. Including non-virtual methods gives the false impression they are overridable.
2. **Use `override`**: If it doesn't compile with `override`, the method isn't virtual: remove it from the trampoline
3. **`PYBIND11_OVERRIDE_PURE` vs `PYBIND11_OVERRIDE`**: Use `PYBIND11_OVERRIDE_PURE` for pure virtual methods (`= 0`), which throws if not implemented in Python. Use `PYBIND11_OVERRIDE` for virtual methods with a base implementation, which falls back to C++ if not overridden.
4. **Trailing comma**: `PYBIND11_OVERRIDE` macros need trailing comma for zero-arg methods (C++20 compatibility)

All trampolines are in `include/pyquantlib/trampolines.h`.

## Handle Templates

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

## Implicit Conversion

PyQuantLib uses `py::implicitly_convertible` to enable automatic conversion from Python types to QuantLib types.

| Type | Converts From | Defined In |
|------|---------------|------------|
| `Date` | `datetime.date`, `datetime.datetime` | `date.cpp` |
| `Array` | lists, numpy arrays | `array.cpp` |
| `Matrix` | list of lists, 2D numpy arrays | `matrix.cpp` |

At the end of each binding function, the conversion is registered:

```cpp
py::implicitly_convertible<py::object, QuantLib::Date>();
py::implicitly_convertible<py::list, Array>();
py::implicitly_convertible<py::array, Array>();
```
