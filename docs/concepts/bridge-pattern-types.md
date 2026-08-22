# Bridge-pattern Types

A handful of QuantLib types behave differently from the rest. `Calendar`, `DayCounter`, and `Region` are the most common examples. They look like value objects (constructor returns an instance, methods return values), but internally they're just thin wrappers around a polymorphic implementation. Understanding why this matters prevents a class of import-time and runtime errors that are otherwise hard to diagnose.

## What the bridge pattern is

The bridge pattern (sometimes called *pimpl*, "pointer to implementation") splits a class into a public interface and a private implementation:

```{mermaid}
classDiagram
    class Calendar {
        -shared_ptr~Impl~ impl_
        +isBusinessDay(date) bool
        +adjust(date, conv) Date
        +advance(date, period) Date
    }
    class CalendarImpl {
        <<abstract>>
        +isBusinessDay(date)*
        +name()*
    }
    class TARGETImpl
    class UnitedStatesImpl
    class JapanImpl

    Calendar o-- CalendarImpl : impl_
    CalendarImpl <|-- TARGETImpl
    CalendarImpl <|-- UnitedStatesImpl
    CalendarImpl <|-- JapanImpl

    class DayCounter
    class DayCounterImpl
    DayCounter o-- DayCounterImpl
```

The user-facing class (`Calendar`, `DayCounter`) is **always concrete** and copyable: it just holds a shared_ptr to an abstract implementation. The actual behaviour comes from concrete subclasses of the implementation (`TARGET`, `UnitedStates`, `Japan`, `Actual365Fixed`, `Thirty360`, ...). The factory functions returning these (`ql.TARGET()`, `ql.Actual365Fixed()`) do the work of constructing both the impl and its public wrapper.

In practice: think of `Calendar` as a *handle to a calendar policy*, not as a calendar itself. The same applies to `DayCounter` and `Region`.

## Why this matters: the empty default

The default constructor of these types returns a wrapper with a **null** implementation. The object exists, but every method call throws because the impl pointer is empty:

```python
dc = ql.DayCounter()                    # creates an empty wrapper
dc.yearFraction(d1, d2)                 # raises: "no day counter implementation provided"
```

This is mostly inert in user code (nobody constructs a bare `DayCounter()` on purpose). The trap is at the **binding layer**: pybind11 default arguments are evaluated *at module import time*. A binding declaring `py::arg("dayCounter") = DayCounter()` creates an empty wrapper while the module loads, and any code path that touches it during import fails.

PyQuantLib's binding code uses three patterns to avoid this, depending on the situation:

| Situation | Fix |
|---|---|
| Default is arbitrary (any valid value works) | Replace with a concrete default: `py::arg("dayCounter") = Actual365Fixed()` |
| No sensible default exists in C++ | Make the parameter required: `py::arg("dayCounter")` |
| Default is a sentinel with semantic meaning ("use the index's day counter") | Use `py::none()` + a lambda that interprets `None` correctly |

Never use a bridge-pattern default constructor as a pybind11 default arg.

## Common bridge-pattern types in QuantLib

| Type | Concrete factories |
|---|---|
| `Calendar` | `TARGET`, `UnitedStates(market)`, `UnitedKingdom(market)`, `Japan`, `Germany`, `JointCalendar(c1, c2)`, ... (see {doc}`/api/time`) |
| `DayCounter` | `Actual360`, `Actual365Fixed`, `Thirty360(convention)`, `ActualActual(convention)`, `Business252(calendar)`, ... |
| `Region` | `EURegion`, `USRegion`, `UKRegion`, `JPRegion`, `FRRegion`, `CustomRegion(name, code)` |

All three follow the same pattern: a polymorphic implementation behind a concrete handle. All three throw on default construction.

## What this implies in user code

Three practical consequences:

1. **Always pass a concrete instance**: `ql.Actual365Fixed()`, never `ql.DayCounter()`.
2. **Equality compares implementations**: two `Calendar` instances are equal if their underlying implementation classes match. `ql.TARGET() == ql.TARGET()` is `True`.
3. **Copies are cheap**: passing a `Calendar` or `DayCounter` to a function copies only the shared_ptr to the impl, not the impl itself. There is no penalty to passing these by value everywhere.

## Common pitfalls

- **Default-constructed bridge type leaking through user code**: usually surfaces as a "no day counter implementation provided" error far from the source. Trace back to the binding or factory that produced the empty wrapper.
- **Region in inflation indexes**: inflation indexes need a `Region`, and a few constructors accept a default-constructed one. Always pass an explicit region.
- **Custom calendars / day counters via subclassing**: subclassing the impl class from Python is technically possible but rarely worth it. The bridge pattern doesn't expose the impl interface cleanly through pybind11; it's almost always simpler to compose existing concrete classes (e.g., `JointCalendar`).

## See also

- {doc}`/api/time`: full `Calendar` and `DayCounter` reference
- {doc}`/contributing`: when adding new bindings, the "Common Pitfalls" section covers the binding-side rules
