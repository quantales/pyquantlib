# The Builder Pattern

*When C++ method chaining meets Python keyword arguments.*

QuantLib uses builder classes -- `MakeSchedule`, `MakeCapFloor`, `MakeOIS`, `MakeVanillaSwap` -- to construct complex objects through fluent method chaining. In C++, the pattern reads naturally:

```cpp
auto cap = MakeCapFloor(CapFloor::Cap, 5*Years, euribor, 0.05)
    .withNominal(1000000.0)
    .withPricingEngine(engine);
// implicit conversion to shared_ptr<CapFloor>
```

The builder accumulates options through `with*` methods that return a reference to themselves, and an implicit conversion operator produces the final object. The question is: how should this surface in Python?

## The Research

Before designing an approach, it is worth studying what the official QuantLib-SWIG bindings do. The answer is surprising.

### The QuantLib-SWIG approach: builders do not exist

QuantLib-SWIG hides the builder entirely. The C++ class is renamed to `_MakeCapFloor` (private), and a Python function takes its place:

```python
def MakeCapFloor(capFloorType, capFloorTenor, iborIndex,
                 strike=None, forwardStart=Period(0, Days), **kwargs):
    mv = _MakeCapFloor(capFloorType, capFloorTenor, iborIndex,
                       strike, forwardStart)
    _apply_kwargs("MakeCapFloor", _MAKECAPFLOOR_METHODS, mv, kwargs)
    return mv.makeCapFloor()
```

A dictionary maps keyword argument names to `with*` methods:

```python
_MAKECAPFLOOR_METHODS = {
    "nominal": "withNominal",
    "calendar": "withCalendar",
    "convention": "withConvention",
    "pricingEngine": "withPricingEngine",
    # ...
}
```

The user writes:

```python
cap = ql.MakeCapFloor(ql.CapFloor.Cap, Period(5, Years), euribor, 0.05,
                       nominal=1000000, pricingEngine=engine)
```

No builder object, no chaining, no explicit conversion call. One function, keyword arguments, instrument returned.

All QuantLib-SWIG builders (`MakeSchedule`, `MakeVanillaSwap`, `MakeCapFloor`, `MakeOIS`, ...) follow the exact same pattern.

### Why QuantLib-SWIG hides the builder

The QuantLib-SWIG choice is deliberately Pythonic. Keyword arguments are Python's native mechanism for optional, named parameters. Method chaining with `with*` prefixes is a C++ and Java idiom that exists precisely because those languages lack keyword arguments. Translating `withNominal(n)` to `nominal=n` is not simplification -- it is the correct Python equivalent.

## The Tension

PyQuantLib has a secondary objective that QuantLib-SWIG does not share: the Python API mirrors the C++ API closely. Every QuantLib class is exposed under its original name, methods keep their C++ names, and the mapping from header to binding file is 1:1. Hiding builders behind functions breaks that contract.

But exposing only the raw builder creates its own problem. Consider the conversion step. In C++, the builder has an `operator shared_ptr<CapFloor>()` that triggers implicitly:

```cpp
shared_ptr<CapFloor> cap = MakeCapFloor(...).withNominal(n);
// compiler calls the conversion operator automatically
```

Python has no implicit conversion operators. The builder must expose an explicit way to produce the result. This means either a named method (`.capFloor()`), a `__call__()` operator, or `py::implicitly_convertible`. Each has drawbacks:

- **Named method** (`.capFloor()`, `.ois()`, `.schedule()`) -- clear, but users must remember the method name.
- **`__call__()`** -- `MakeCapFloor(...)()` looks like a double invocation and confuses readers.
- **Implicit conversion** -- only works when the result flows into a typed argument slot, not when assigned to a variable.

None of these match the ergonomics of the C++ original. The builder pattern is simply not a natural fit for Python.

## The Decision

PyQuantLib follows the QuantLib-SWIG approach: **keyword-argument functions are the public API**.

### The internal C++ binding

The C++ builder class is bound with its full set of `with*` methods and a named conversion method (`.capFloor()`, `.ois()`, `.schedule()`). This binding exists internally so that the Python wrapper function can delegate to it. It is not part of the public API.

The conversion method is named after what it builds -- no `__call__`, no implicit conversion for instrument builders. These are internal design choices documented here for contributors, not user-facing decisions.

### The public API: keyword-argument functions

A Python function in `pyquantlib/builders.py` wraps each C++ builder with `**kwargs`. The wrapper is re-exported from `pyquantlib/__init__.py`, shadowing the C++ class name:

```python
cap = ql.MakeCapFloor(ql.CapFloor.Cap, Period(5, Years), euribor, 0.05,
                       nominal=1_000_000, pricingEngine=engine)
```

One function call, keyword arguments, instrument returned.

### The kwargs mapping convention

Builder `with*` methods map to keyword arguments by dropping the `with` prefix and lowercasing the first letter:

| C++ method | Python kwarg |
|------------|-------------|
| `withNominal(n)` | `nominal=n` |
| `withPricingEngine(e)` | `pricingEngine=e` |
| `withFixedLegDayCount(dc)` | `fixedLegDayCount=dc` |
| `withCalendar(cal)` | `calendar=cal` |

Methods without the `with` prefix (like `receiveFixed`, `asOptionlet`, `forwards`, `backwards`) keep their name as-is.

The `from_` method on `MakeSchedule` maps to `effectiveDate` in the kwargs function, avoiding Python's reserved `from` keyword.

## Examples

```python
import pyquantlib as ql

# --- MakeSchedule ---
schedule = ql.MakeSchedule(
    effectiveDate=ql.Date(15, 1, 2025),
    terminationDate=ql.Date(15, 1, 2030),
    tenor=ql.Period(6, ql.Months),
    calendar=ql.TARGET(),
    convention=ql.ModifiedFollowing,
    terminationDateConvention=ql.ModifiedFollowing,
    rule=ql.DateGeneration.Forward,
    endOfMonth=False,
)

# --- MakeCapFloor ---
euribor = ql.Euribor6M(flat_curve)
engine = ql.BlackCapFloorEngine(flat_vol_curve)

cap = ql.MakeCapFloor(
    ql.CapFloor.Cap, ql.Period(5, ql.Years), euribor, 0.04,
    nominal=1_000_000,
    pricingEngine=engine,
)

# --- MakeOIS ---
sofr = ql.Sofr(flat_curve)

swap = ql.MakeOIS(
    ql.Period(2, ql.Years), sofr, 0.03,
    nominal=10_000_000,
    fixedLegDayCount=ql.Actual360(),
    pricingEngine=engine,
)
```

## The Convention

Every `Make*` builder in PyQuantLib follows this pattern:

1. **Public API**: a keyword-argument function that returns the built object directly
2. **Internal C++ binding**: builder class with `with*` chaining + named conversion method
3. **kwargs mapping**: drop `with` prefix, lowercase first letter
4. **No `__call__`**: named conversion methods internally
5. **Implicit conversion**: only for value-type results (`MakeSchedule`) used as function arguments
