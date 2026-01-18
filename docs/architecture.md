# Architecture

This document provides a high-level overview of PyQuantLib's design.

```{seealso}
- {doc}`internals` for detailed implementation: BindingManager, module patterns, trampolines
- {doc}`extending` for Python subclassing guide
- {doc}`building` for build setup
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
│   ├── core/                  # Core module bindings
│   ├── math/                  # Math module bindings
│   └── ...                    # Other domain modules
└── pyquantlib/
    ├── __init__.py            # Python package init
    ├── extensions/            # Pure Python extensions
    └── _pyquantlib/           # Compiled extension
```

## Key Components

### BindingManager

Orchestrates module organization and binding registration. Handles dependency ordering (base classes before derived) and submodule management.

See {doc}`internals` for implementation details.

### Trampoline Classes

Enable Python code to subclass QuantLib abstract base classes. Virtual method calls are intercepted and redirected to Python.

See {doc}`extending` for user guide and {doc}`internals` for implementation.

### Implicit Conversion

Automatic conversion from Python types to QuantLib types using `py::implicitly_convertible`:

| Type | Converts From |
|------|---------------|
| `Date` | `datetime.date`, `datetime.datetime` |
| `Array` | lists, numpy arrays |
| `Matrix` | list of lists, 2D numpy arrays |

See {doc}`numpy` for usage and {doc}`internals` for implementation.

### Hidden Handles

Pythonic API that accepts raw objects instead of handles. Handles are created internally.

See {doc}`handles` for user guide.

## Design Decisions

### Why pybind11?

- **Type-safe**: Bindings resolved at compile time
- **Standard C++**: No additional DSL or code generation
- **Low overhead**: Thin wrapper around QuantLib
- **Active ecosystem**: Well-maintained, widely used

### Why BindingManager?

- **Dependency ordering**: Base classes must be bound before derived
- **Error isolation**: Clear error messages when bindings fail
- **Submodule management**: Clean separation of ABCs into `pyquantlib.base`

### Why Separate Trampolines Header?

- **Single source of truth**: All trampolines in one place
- **Easier maintenance**: Update virtual methods once
- **Documentation**: Clear inventory of overridable classes

### Why Implicit Conversion?

- **Pythonic API**: Users work with `datetime.date`, lists, numpy arrays
- **No special syntax**: Standard Python types just work
- **Gradual migration**: Can add more conversions without API breaks

### Why Static QuantLib?

- **Singleton correctness**: Prevents duplicate `Settings` instances
- **Simpler deployment**: No dynamic library dependencies
- **Cross-platform consistency**: Same behavior on all platforms
