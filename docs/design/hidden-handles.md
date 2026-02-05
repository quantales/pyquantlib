# The Hidden Handle Pattern

*Making C++ idioms disappear.*

QuantLib loves handles. `Handle<Quote>`, `Handle<YieldTermStructure>`, `Handle<BlackVolTermStructure>`. They appear everywhere: in constructors, in method parameters, in return types.

```cpp
// C++ - typical QuantLib constructor
FlatForward(const Date& referenceDate,
            const Handle<Quote>& forward,
            const DayCounter& dayCounter);
```

The handle pattern is elegant in C++. It provides lazy evaluation, automatic observer registration, and the ability to relink term structures without reconstructing dependent objects. But in Python, it creates friction.

## The Friction

A Python user pricing a simple option must write:

```python
rate = ql.SimpleQuote(0.05)
rate_handle = ql.QuoteHandle(rate)
curve = ql.FlatForward(today, rate_handle, day_counter)
```

Three lines where one feels natural. The handle adds no value here---the user just wants to pass a rate to a curve. The indirection is visible but provides no benefit for this common case.

Compare to what feels natural:

```python
rate = ql.SimpleQuote(0.05)
curve = ql.FlatForward(today, rate, day_counter)
```

The question: can we support both? Explicit handles for power users who need relinking, and implicit handles for everyone else?

## The Solution

Provide two constructor overloads. One accepts the handle explicitly. The other accepts the underlying object and wraps it internally.

```cpp
// Explicit handle (for power users who need relinking)
.def(py::init<const Date&, const Handle<Quote>&, const DayCounter&>(),
    py::arg("referenceDate"),
    py::arg("forward"),
    py::arg("dayCounter"),
    "Constructs from a quote handle.")

// Hidden handle (simpler for common use)
.def(py::init([](const Date& referenceDate,
                 const ext::shared_ptr<Quote>& forward,
                 const DayCounter& dayCounter) {
    return ext::make_shared<FlatForward>(
        referenceDate,
        Handle<Quote>(forward),
        dayCounter);
}),
    py::arg("referenceDate"),
    py::arg("forward"),
    py::arg("dayCounter"),
    "Constructs from a quote (handle created internally).")
```

Python's duck typing does the rest. When the user passes a `SimpleQuote`, pybind11 matches the second overload. When they pass a `QuoteHandle`, it matches the first.

```python
# Both work
curve1 = ql.FlatForward(today, ql.QuoteHandle(rate), dc)  # Explicit
curve2 = ql.FlatForward(today, rate, dc)                   # Hidden
```

## The Trade-off

Hidden handles sacrifice one capability: relinking.

```python
# With explicit handle - relinking works
handle = ql.RelinkableQuoteHandle(rate1)
curve = ql.FlatForward(today, handle, dc)
handle.linkTo(rate2)  # Curve now uses rate2

# With hidden handle - no relinking possible
curve = ql.FlatForward(today, rate1, dc)
# Cannot change what rate the curve uses
```

This is acceptable. Users who need relinking can use explicit handles. Users who want simplicity get it by default. The API serves both audiences without forcing the complex path on everyone.

## Implementation Notes

When implementing hidden handles, the lambda must fully specify the `Handle<T>` construction:

```cpp
.def(py::init([](const ext::shared_ptr<Quote>& quote, ...) {
    return ext::make_shared<FlatForward>(
        ...,
        Handle<Quote>(quote),  // Explicit Handle construction
        ...);
}), ...)
```

Including the full header for the underlying type is required:

```cpp
#include <ql/quote.hpp>                              // For Handle<Quote>
#include <ql/termstructures/yieldtermstructure.hpp>  // For Handle<YieldTermStructure>
```

Without these includes, the compiler may see only forward declarations, causing cryptic template errors.

## Where This Pattern Applies

The hidden handle pattern appears throughout PyQuantLib:

| Class | Hidden Handle Parameter |
|-------|------------------------|
| `FlatForward` | `Quote`, `YieldTermStructure` |
| `BlackConstantVol` | `Quote` |
| `GeneralizedBlackScholesProcess` | `Quote`, `YieldTermStructure`, `BlackVolTermStructure` |
| `HestonProcess` | `Quote`, `YieldTermStructure` |
| Most pricing engines | Various term structures |

The pattern transforms verbose C++ idioms into clean Python APIs while preserving full functionality for advanced use cases.
