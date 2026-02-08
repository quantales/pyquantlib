# Architecture

High-level overview of PyQuantLib's design: the problems it solves, the patterns it uses, and the reasoning behind key decisions.

```{seealso}
- {doc}`internals` for implementation details: BindingManager API, module patterns, trampoline code
- {doc}`design/index` for deep-dive stories on specific binding challenges
- {doc}`extending` for the Python subclassing guide
- {doc}`building` for build setup
```

## The Binding Challenge

Binding a C++ library to Python is usually mechanical: wrap a class, expose its methods, move on. QuantLib makes this harder than most libraries. Its C++ design relies on idioms that clash with Python's memory model and runtime semantics.

The tensions that shaped PyQuantLib's architecture:

**Object lifetimes.** QuantLib's interpolation classes store iterators to external data, assuming the data outlives the interpolation. Python users pass temporary lists that die immediately. The binding layer must keep data alive without changing QuantLib's API. See {doc}`design/interpolation`.

**Singleton identity.** QuantLib's `Settings` singleton uses a C++ static local variable. When QuantLib is built as a shared library, dynamic linking can create duplicate singletons: Python writes the evaluation date to one, QuantLib reads from the other. The assignment succeeds, the getter returns the correct value, but all calculations use the wrong date. See {doc}`design/settings-singleton`.

**Virtual dispatch across languages.** Python subclasses can override QuantLib virtual methods via pybind11 trampolines. But accessing C++ objects from Python during these callbacks creates temporary wrappers that dangle after the expression ends. The trampoline design must enforce clean separation between C++ object management and Python computation. See {doc}`design/python-subclassing`.

**Handle indirection.** QuantLib uses `Handle<T>` extensively for lazy evaluation and relinking. This pattern is natural in C++ but adds friction in Python, where users expect to pass objects directly. See {doc}`design/hidden-handles`.

**Import-time traps.** QuantLib's bridge-pattern classes (`DayCounter`, `Calendar`) have default constructors that create invalid objects. Using these as pybind11 default arguments crashes at import time, before any user code runs. See {doc}`design/bridge-defaults`.

**Protected member access.** Python subclasses that override QuantLib virtual methods sometimes need access to C++ protected members. pybind11 lambdas cannot reach protected fields, and friend declarations require modifying QuantLib headers. A helper struct that inherits from the base class exploits C++ inheritance rules to expose the member without changing upstream code. See {doc}`design/protected-members`.

**Enum mutation.** pybind11 represents enum values as singletons. Passing them by reference to C++ functions that modify the reference corrupts the singleton for the entire Python session. See {doc}`design/enum-singletons`.

**Cross-file type resolution.** pybind11's compile-time type resolution breaks when a method returns `shared_ptr<T>` for a type registered in a different source file. The solution requires deferring type conversion from compile time to runtime. See {doc}`design/cross-tu-holders`.

**Diamond inheritance.** QuantLib classes occasionally inherit from two base classes that share a common virtual ancestor, forming a diamond. pybind11's classic holder system computes pointer offsets at compile time using `static_cast`, which cannot resolve the ambiguous paths through virtual bases. The solution requires migrating the entire inheritance chain to pybind11 3.0's `smart_holder` system. See {doc}`design/diamond-inheritance`.

**Builder pattern translation.** QuantLib's `Make*` builders use C++ method chaining and implicit conversion operators to construct complex objects. Python has no implicit conversion operators, and method chaining with `with*` prefixes is not idiomatic when keyword arguments exist. PyQuantLib exposes both a C++ builder class for chaining and a Python wrapper function that maps keyword arguments to builder methods, returning the result directly. See {doc}`design/builder-pattern`.

These are not hypothetical risks. Each one was discovered through debugging production failures. The {doc}`design notes <design/index>` document these investigations in full.

## Layered Design

```
┌──────────────────────────────────────────────────────┐
│  Python application code                             │
│  import pyquantlib as ql                             │
├──────────────────────────────────────────────────────┤
│  pyquantlib Python package                           │
│  __init__.py · extensions/ · .pyi type stubs         │
├──────────────────────────────────────────────────────┤
│  pybind11 binding layer  (_pyquantlib)               │
│  src/**/*.cpp · trampolines.h · binding_manager.h    │
├──────────────────────────────────────────────────────┤
│  QuantLib C++ library  (statically linked)           │
│  ql/**/*.hpp · libQuantLib.a                         │
└──────────────────────────────────────────────────────┘
```

Each layer has a clear responsibility:

| Layer | Responsibility |
|-------|---------------|
| **Python package** | Public API surface (`import pyquantlib as ql`). Houses pure Python extensions and `.pyi` type stubs for IDE support. |
| **Binding layer** | Translates between C++ and Python. Manages object lifetimes, type conversions, handle wrapping, and trampoline dispatch. |
| **QuantLib** | All financial computation. Linked statically to ensure singleton correctness and eliminate runtime library dependencies. |

The binding layer exposes two Python namespaces:

- **`pyquantlib`** (main namespace): Concrete classes ready for direct use: `SimpleQuote`, `FlatForward`, `AnalyticEuropeanEngine`, etc.
- **`pyquantlib.base`**: Abstract base classes for subclassing: `Quote`, `CashFlow`, `PricingEngine`, etc. Separated because ABCs are not meant to be instantiated directly; placing them in a submodule makes extending the library an explicit choice.

## Module Organization

### File Mapping

Each QuantLib header has a corresponding binding file. The directory structure mirrors QuantLib's:

| QuantLib Header | PyQuantLib Binding |
|-----------------|-------------------|
| `ql/pricingengines/vanilla/mcamericanengine.hpp` | `src/pricingengines/vanilla/mcamericanengine.cpp` |
| `ql/termstructures/yield/flatforward.hpp` | `src/termstructures/yield/flatforward.cpp` |
| `ql/time/date.hpp` | `src/time/date.cpp` |
| `ql/instrument.hpp` | `src/core/instrument.cpp` |

Top-level QuantLib files (e.g., `ql/instrument.hpp`) map to `src/core/`. This 1:1 convention makes it straightforward to locate the binding for any QuantLib class.

### Directory Structure

```
pyquantlib/
├── include/pyquantlib/
│   ├── binding_manager.h      # Central orchestration
│   ├── trampolines.h          # All trampoline classes
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
├── pyquantlib/
│   ├── __init__.py            # Python package init
│   ├── extensions/            # Pure Python extensions
│   └── _pyquantlib/           # Compiled extension
└── tests/                     # Test files
```

Each domain directory follows the aggregator pattern: an `all.cpp` registers all binding functions for the directory, and individual `.cpp` files contain one class binding each. See {doc}`internals` for the code patterns.

### Test Organization

Test files group by QuantLib subdirectory:

| QuantLib Path | Test File |
|---------------|-----------|
| `ql/pricingengines/vanilla/*.hpp` | `tests/test_pricingengines_vanilla.py` |
| `ql/time/*.hpp` | `tests/test_time.py` |
| `ql/math/*.hpp` | `tests/test_math.py` |

## Core Mechanisms

### Deferred Registration

pybind11 requires base classes to be registered before derived classes. In a project with hundreds of classes across many files, managing this ordering manually is fragile.

The `BindingManager` solves this by collecting binding functions during initialization and executing them in dependency order via `finalize()`. Each domain module registers its bindings; the manager ensures `Observable` is bound before `Quote`, `Quote` before `SimpleQuote`, and so on.

This also provides error isolation: if a binding fails, the error message identifies which registration caused it, rather than producing a cryptic pybind11 template error.

See {doc}`internals` for the BindingManager API and macros.

### Python Subclassing

QuantLib's abstract base classes (`Quote`, `CashFlow`, `PricingEngine`, etc.) can be subclassed in Python. This enables rapid prototyping of custom pricing engines, term structures, and market data sources without C++ recompilation.

The mechanism is pybind11's trampoline pattern: a C++ class intercepts virtual method calls and redirects them to Python:

```
QuantLib C++ code  →  Trampoline class  →  Python method
```

The key architectural constraint is that **Python overrides should only receive simple types** (numbers, enums, strings), not C++ objects. Accessing C++ objects from Python during callbacks creates temporary wrappers with dangerous lifetime semantics.

This is enforced by carefully choosing which virtual methods the trampoline exposes. For example, pricing engines expose the computational `calculate(f1, f2, strike, ...)` method (pure numbers) but not the parameter-extraction `calculate()` method (which accesses C++ handles and term structures).

All trampolines live in a single header (`trampolines.h`) to provide a clear inventory of overridable classes and methods.

See {doc}`extending` for the user guide and {doc}`internals` for implementation details.

### Hidden Handles

QuantLib's `Handle<T>` pattern provides lazy evaluation and relinking, but it adds verbosity in Python:

```python
# Without hidden handles
process = ql.GeneralizedBlackScholesProcess(
    ql.QuoteHandle(spot),
    ql.YieldTermStructureHandle(dividend),
    ql.YieldTermStructureHandle(risk_free),
    ql.BlackVolTermStructureHandle(volatility),
)

# With hidden handles
process = ql.GeneralizedBlackScholesProcess(
    spot, dividend, risk_free, volatility
)
```

PyQuantLib provides both APIs via constructor overloads. When a user passes a raw object, a non-relinkable `Handle` is created internally. When an explicit handle is passed, it goes through directly. Python's duck typing selects the right overload automatically.

The trade-off is that hidden handles do not support relinking. Users who need to swap the underlying object at runtime use explicit `RelinkableHandle` constructors.

See {doc}`handles` for the user guide and {doc}`design/hidden-handles` for implementation details.

### Implicit Conversion

Python types convert automatically to QuantLib types:

| QuantLib Type | Accepts |
|---------------|---------|
| `Date` | `datetime.date`, `datetime.datetime` |
| `Array` | Python lists, NumPy arrays |
| `Matrix` | Nested lists, 2D NumPy arrays |

Functions expecting `Array` accept plain Python lists, and dates can be passed as `datetime.date` objects. Conversions are registered via `py::implicitly_convertible` at the end of each binding file.

See {doc}`numpy` for NumPy interoperability details.

## Coverage

PyQuantLib binds a curated subset of QuantLib. Initial versions focused on the most widely used components. Coverage is actively growing. The {doc}`api/index` provides the complete reference. Each new binding follows the checklist in {doc}`contributing`.

## Design Decisions

### Why pybind11?

The existing Python bindings for QuantLib use SWIG (QuantLib-SWIG) and Cython (PyQL). Both introduce an additional language beyond C++ and Python: SWIG's interface definition files or Cython's hybrid syntax. This increases cognitive load when navigating binding code or keeping wrappers synchronized with upstream QuantLib changes.

pybind11 bindings are written in standard C++. The wrapper code directly references QuantLib headers and classes, with no intermediate DSL, code generation step, or third language to learn. A developer who knows C++ and Python can read and modify bindings immediately.

Additional factors:

- **Compile-time type safety**: Signature mismatches fail at build time, not runtime
- **Standard debugging**: C++ debuggers work directly on the binding code, with no generated-code layers obscuring the call stack
- **Active ecosystem**: Extensive documentation and community support

### Why Static Linking?

QuantLib's `Settings` singleton uses a C++ static local variable. When QuantLib is built as a shared library and loaded into a Python extension module, dynamic linking can create duplicate singleton instances. The Python binding writes the evaluation date to one instance; QuantLib's pricing code reads from another. The assignment succeeds, the getter returns the correct value, but all calculations use the wrong date.

Static linking embeds QuantLib directly into the Python extension module, guaranteeing a single singleton instance. This also simplifies deployment by eliminating dynamic library dependencies.

See {doc}`design/settings-singleton` for the full investigation.

### Why a Base Submodule?

Abstract base classes live in `pyquantlib.base`, separate from the main namespace. This signals that these classes are for subclassing, not direct instantiation. A user writing `from pyquantlib.base import Quote` is making an explicit choice to extend the library, while `import pyquantlib as ql` provides only concrete, ready-to-use classes.

### Why Deferred Registration?

pybind11 requires base classes to be bound before derived classes. Without centralized ordering, adding a new class requires knowing the entire dependency graph. The BindingManager collects all registrations and executes them in the declared order, with clear error messages when something fails. This scales to hundreds of classes without manual dependency tracking.

### Why a Single Trampolines Header?

All trampoline classes are in `include/pyquantlib/trampolines.h`. This provides a single source of truth for which classes are overridable from Python and which virtual methods are exposed. When QuantLib updates a virtual method signature, there is one place to update. The file also serves as documentation: a complete inventory of Python-extensible classes.

### Why 1:1 File Mapping?

Each QuantLib header maps to exactly one binding file. This convention makes it trivial to find the binding for any QuantLib class (replace `ql/` with `src/` and `.hpp` with `.cpp`). It also prevents binding files from growing into unmanageable monoliths and keeps compilation units small for faster incremental builds.

The trade-off is that methods returning types from other files encounter pybind11's cross-translation-unit type resolution limitation. This is handled with a `py::cast()` pattern documented in {doc}`design/cross-tu-holders`.
