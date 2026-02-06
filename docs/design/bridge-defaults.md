# The Bridge Pattern Trap

*When default arguments crash at import time.*

Some QuantLib classes look simple but hide a dangerous quirk. `DayCounter` and `Calendar` have default constructors that create objects in an invalid state. Using them as default arguments in Python bindings causes crashes---not when the function is called, but when the module is imported.

## The Symptom

The binding code looks reasonable:

```cpp
.def(py::init<const Date&, Rate, const DayCounter&>(),
    py::arg("referenceDate"),
    py::arg("rate"),
    py::arg("dayCounter") = DayCounter())  // Default: empty day counter
```

But importing the module fails:

```python
>>> import pyquantlib as ql
RuntimeError: no day counter implementation provided
```

The error occurs before any user code runs. The module cannot even be imported.

## The Cause

`DayCounter` and `Calendar` use the bridge pattern (also called pimpl or handle-body). The class is a thin wrapper around an implementation pointer:

```cpp
class DayCounter {
private:
    ext::shared_ptr<Impl> impl_;
public:
    DayCounter() : impl_() {}  // Null implementation!

    BigInteger dayCount(const Date& d1, const Date& d2) const {
        QL_REQUIRE(impl_, "no day counter implementation provided");
        return impl_->dayCount(d1, d2);
    }
};
```

The default constructor creates a `DayCounter` with a null `impl_`. Any method call throws. This is intentional---it forces users to choose a concrete day counter like `Actual365Fixed` or `Thirty360`.

The problem arises in pybind11. When the binding is registered:

```cpp
py::arg("dayCounter") = DayCounter()
```

pybind11 evaluates `DayCounter()` immediately during module initialization. It then attempts to convert this C++ object to a Python object. That conversion process may invoke methods on the `DayCounter`. The null implementation throws.

## The Solution

Replace the invalid default with a concrete implementation:

```cpp
// Wrong - crashes at import
py::arg("dayCounter") = DayCounter()

// Right - works
py::arg("dayCounter") = Actual365Fixed()
```

Or make the parameter required:

```cpp
// Also right - no default at all
py::arg("dayCounter")
```

The same applies to `Calendar`:

```cpp
// Wrong
py::arg("calendar") = Calendar()

// Right
py::arg("calendar") = TARGET()
// or
py::arg("calendar") = NullCalendar()
```

## The Plot Twist

Problem solved? Not quite. The two fixes above work for most cases, but `FloatingRateCoupon` exposed a subtlety that neither handles well.

QuantLib's `FloatingRateCoupon` constructor takes a `DayCounter` with a default of `DayCounter()`. But that empty default is not just laziness or a placeholder. It carries meaning: "use the index's day counter." The constructor checks for null and falls back to the index's own convention. It is a sentinel.

Replacing it with `Actual365Fixed()` compiles. It imports. It runs. And it silently produces wrong accrual calculations for any index that does not use Actual/365 Fixed. The fix becomes the bug.

Making it required is also wrong. QuantLib users never specify this parameter. Forcing them to would make the Python API more cumbersome than the C++ original---the opposite of the project's goal.

There is a third option. The C++ sentinel is "null object." The Python sentinel is `None`. Map one to the other:

```cpp
.def(py::init([](/* ... */,
                 const py::object& dayCounter,
                 /* ... */) {
    DayCounter dc;
    if (!dayCounter.is_none())
        dc = dayCounter.cast<DayCounter>();
    return ext::make_shared<FloatingRateCoupon>(/* ... */, dc, /* ... */);
}),
     py::arg("dayCounter") = py::none())
```

The lambda accepts `py::object` instead of `DayCounter`. The default is `py::none()`, which pybind11 evaluates harmlessly at import time---`None` is always a valid Python object. Inside the lambda, `None` maps to `DayCounter()` (the null sentinel), and any real day counter passes through via `.cast<>()`.

The Python user sees exactly what they expect:

```python
# Uses the index's day counter (default)
coupon = ql.FloatingRateCoupon(pay_date, nominal, start, end, 2, index)

# Overrides with a specific day counter
coupon = ql.FloatingRateCoupon(pay_date, nominal, start, end, 2, index,
                                dayCounter=ql.Actual360())
```

The same pattern handles `Null<Natural>()`, another QuantLib sentinel that pybind11 cannot convert:

```cpp
const py::object& lookbackDays,
...
Natural lb = Null<Natural>();
if (!lookbackDays.is_none())
    lb = lookbackDays.cast<Natural>();
...
py::arg("lookbackDays") = py::none()
```

## Identifying Bridge-Pattern Classes

Not all QuantLib classes with default constructors have this problem. The dangerous ones share these traits:

1. **Default constructor exists** but creates an unusable object
2. **Method calls check for valid state** and throw if invalid
3. **pybind11 conversion may invoke methods** during default argument evaluation

Classes that follow this pattern in QuantLib:

| Class | Safe Default Alternative |
|-------|-------------------------|
| `DayCounter` | `Actual365Fixed()`, or `py::none()` if the null has meaning |
| `Calendar` | `TARGET()`, `NullCalendar()` |
| `Null<T>()` | `py::none()` with lambda conversion |
| `Index` | (make required, no universal default) |
| `Interpolation` | (make required) |

## Choosing the Right Fix

The three solutions serve different situations:

| Situation | Fix |
|-----------|-----|
| Default is arbitrary (any valid value works) | Replace with a concrete default |
| Default does not exist in C++ | Make the parameter required |
| Default is a sentinel with semantic meaning | Use `py::none()` + lambda |

Most bindings fall into the first category. A few, like `FloatingRateCoupon`'s day counter and `OvernightIndexedCoupon`'s lookback days, fall into the third. Recognizing which category a parameter belongs to is the real skill. Getting it wrong in the first category just changes a default. Getting it wrong in the third produces silent, incorrect results.

## Why This Fails at Import

The crash timing surprises most developers. The expectation is that default arguments are evaluated when the function is called, not when the module loads.

In pybind11, default argument values are converted to Python objects during module initialization. This conversion can trigger C++ code paths that assume the object is valid. For bridge-pattern classes with null defaults, those assumptions fail.

The error message rarely points to the actual cause. "no day counter implementation provided" gives no hint that the problem is a default argument in a binding definition.

Knowing this pattern exists makes the debugging straightforward. Seeing it for the first time, without context, can cost hours.
