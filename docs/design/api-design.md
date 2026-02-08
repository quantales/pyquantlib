# API Design

*Mirror the domain model. Translate the idioms.*

PyQuantLib wraps a C++ library for a Python audience. Two goals pull in different directions: fidelity to QuantLib, and a natural Python experience. This note explains how PyQuantLib resolves the tension.

## The Distinction

Not everything in QuantLib's API is a QuantLib concept. Some of it is C++ solving problems that Python does not have.

**Domain model** -- the names, the class hierarchy, the financial semantics. `FixedRateBond`, `BlackScholesMertonProcess`, `Euribor6M`, `dayCounter()`, `startDate()`, `nominal()`. These are quantitative finance vocabulary. Renaming `dayCounter()` to `day_counter()` would not make the library more Pythonic; it would just break every QuantLib tutorial and textbook ever written.

**Language idioms** -- the patterns C++ uses because it is C++. `Handle<T>` wrappers because C++ has no duck typing. Builder method chaining because C++ has no keyword arguments. `Null<Rate>()` sentinels because C++ has no `None`. Implicit conversion operators because C++ can overload type coercion. The Settings class accessed through `::instance()` because C++ singletons need a static method.

The litmus test: *Is this a QuantLib concept, or a C++ concept?* If it is QuantLib, preserve it. If it is C++, find the Python equivalent.

## What Gets Preserved

**Class names.** `FixedRateBond`, not `fixed_rate_bond`. `AnalyticEuropeanEngine`, not `analytic_european_engine`. These are domain names that appear in textbooks, papers, and QuantLib's own documentation. Preserving them means QuantLib knowledge transfers directly.

**Method names.** `dayCounter()`, `startDate()`, `nominal()`. camelCase is not Pythonic, but these are the names the quant finance community uses. Converting to snake_case would make QuantLib documentation useless for PyQuantLib users.

**Class hierarchy.** `FixedRateBond` inherits from `Bond` inherits from `Instrument`. The inheritance tree reflects genuine domain relationships, not C++ implementation choices.

**File structure.** Each QuantLib header maps 1:1 to a binding file. This is an organizational choice that makes the codebase navigable, not an API-surface decision.

## What Gets Translated

Each translation replaces a C++ idiom with its Python equivalent. The domain semantics are unchanged; only the mechanism differs.

| C++ Idiom | Python Equivalent | Design Note |
|-----------|-------------------|-------------|
| `Handle<Quote>(quote)` | Pass the object directly | {doc}`hidden-handles` |
| `MakeCapFloor(...).withNominal(n)` | `MakeCapFloor(..., nominal=n)` | {doc}`builder-pattern` |
| `Null<Rate>()` | `None` | {doc}`bridge-defaults` |
| `DayCounter()` (invalid default) | `py::none()` sentinel or concrete default | {doc}`bridge-defaults` |
| `Settings::instance().evaluationDate()` | `ql.Settings.evaluationDate` | {doc}`settings-singleton` |
| Implicit conversion operators | Named methods or `py::implicitly_convertible` | {doc}`builder-pattern` |

In every case, the C++ idiom exists to work around a limitation that Python does not share. Keyword arguments replace method chaining. `None` replaces null sentinels. Duck typing replaces explicit handle wrapping. The Python user gets the same functionality through native Python mechanisms.

## The Boundary

This principle has a clear limit: PyQuantLib does not invent new abstractions. It does not merge classes, add convenience methods, or redesign QuantLib's API. The domain model is QuantLib's. PyQuantLib only translates the *delivery mechanism* from C++ idioms to Python idioms.

A user who reads QuantLib's C++ documentation should recognize every class, every method name, and every parameter. The difference is how they *call* those classes -- with Python's syntax, Python's defaults, and Python's conventions for optional parameters.
