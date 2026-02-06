# The Enum Singleton Problem

*When pass-by-reference meets singleton semantics.*

An enum value that looks fine in isolation but corrupts itself during tests. A failure that disappears when you add debug prints. The smoking gun hiding in plain sight in the error message. This is the story of how pybind11's singleton enum implementation clashes with C++'s pass-by-reference idiom, and why the simplest binding is sometimes the wrong binding.

## The Setup

Binding QuantLib's `EndCriteria` class to Python required exposing several check methods that determine when optimization should stop:

```cpp
class EndCriteria {
public:
    enum Type {
        None = 0,
        MaxIterations = 1,
        StationaryPoint = 2,
        StationaryFunctionValue = 3,
        StationaryFunctionAccuracy = 4,
        ZeroGradientNorm = 5,
        FunctionEpsilonTooSmall = 6,
        Unknown = 7
    };

    bool checkMaxIterations(Size iteration, Type& ecType) const;
    bool checkStationaryPoint(Real xOld, Real xNew,
                              Size& statState, Type& ecType) const;
    // ... more check methods
};
```

The C++ API uses a common pattern: pass the current `Type` by reference, and the method updates it based on what condition triggered. This allows returning both a boolean (did we stop?) and the reason (which condition?).

## The Naive Binding

The straightforward binding mirrors the C++ signature:

```cpp
py::enum_<EndCriteria::Type>(pyEndCriteria, "Type")
    .value("None_", EndCriteria::Type::None)
    .value("MaxIterations", EndCriteria::Type::MaxIterations)
    .value("StationaryPoint", EndCriteria::Type::StationaryPoint)
    // ... all enum values
    .value("Unknown", EndCriteria::Type::Unknown);

pyEndCriteria
    .def("checkStationaryPoint",
        &EndCriteria::checkStationaryPoint,
        py::arg("xOld"), py::arg("xNew"),
        py::arg("statState"), py::arg("ecType"),
        "Checks for stationary point. Returns bool.");
```

This compiles cleanly. Initial tests pass. Ship it, right?

## The Mysterious Failure

After running the full test suite:

```
tests/test_methods.py::test_endcriteria_static_succeeded FAILED

def test_endcriteria_static_succeeded():
    assert not ql.EndCriteria.succeeded(ql.EndCriteria.Type.Unknown)
E   AssertionError: assert not True
E    +  where <Type.StationaryPoint: 2> = <class 'pyquantlib.EndCriteria.Type'>.Unknown
```

The error message contains a critical clue that is easy to miss: `ql.EndCriteria.Type.Unknown` is displaying as `<Type.StationaryPoint: 2>`.

`Unknown` should be value 7. But it's showing as `StationaryPoint` (value 2). The enum singleton has been silently mutated.

## The Wrong Diagnosis

The first suspicion: maybe the enum values are wrong. Perhaps a missing enum value is causing integer assignments to shift. The binding had omitted `FunctionEpsilonTooSmall` (value 6), so maybe `Unknown` was being assigned 6 instead of 7?

Adding `FunctionEpsilonTooSmall` back to the binding, rebuilding, running tests: **same failure**.

## The Stale Build Theory

Next theory: stale compiled code. Maybe the binding is caching an old definition somewhere.

Clean build from scratch. Remove `build/` directory. Uninstall and reinstall. Rebuild everything. Run tests: **same failure**.

## The Debug Script

Desperate for clues, a debug script to inspect the enum values directly:

```python
import pyquantlib as ql

print("EndCriteria.Type enum values:")
for name in dir(ql.EndCriteria.Type):
    if not name.startswith('_'):
        value = getattr(ql.EndCriteria.Type, name)
        print(f"{name:30} = {value} (int: {int(value)})")
```

Running this script:

```
None_                          = Type.None_ (int: 0)
MaxIterations                  = Type.MaxIterations (int: 1)
StationaryPoint                = Type.StationaryPoint (int: 2)
StationaryFunctionValue        = Type.StationaryFunctionValue (int: 3)
StationaryFunctionAccuracy     = Type.StationaryFunctionAccuracy (int: 4)
ZeroGradientNorm               = Type.ZeroGradientNorm (int: 5)
FunctionEpsilonTooSmall        = Type.FunctionEpsilonTooSmall (int: 6)
Unknown                        = Type.Unknown (int: 7)
```

**Every value is correct.** `Unknown = 7`, exactly as it should be.

But pytest says `Unknown` equals `StationaryPoint` (2). The debug script says `Unknown` equals 7. How can the same enum value be different in different contexts?

## The Smoking Gun

The key insight: the debug script runs in a **fresh Python process** where no methods have been called yet. The pytest failure happens **after other tests have run**.

Looking at the test execution order:

```python
def test_endcriteria_stationary_point(end_criteria):
    """Test EndCriteria checkStationaryPoint method."""
    has_ended, _ = end_criteria.checkStationaryPoint(
        xOld=1.0, xNew=1.0000001, statState=10,
        ecType=ql.EndCriteria.Type.Unknown  # <-- Pass Unknown here
    )
    assert has_ended

def test_endcriteria_static_succeeded():
    """Runs AFTER the above test."""
    assert not ql.EndCriteria.succeeded(ql.EndCriteria.Type.Unknown)  # <-- Fails here
```

The first test calls `checkStationaryPoint()` and passes `ql.EndCriteria.Type.Unknown` as the `ecType` argument. The C++ signature is:

```cpp
bool checkStationaryPoint(Real xOld, Real xNew,
                          Size& statState, Type& ecType) const;
```

That `Type& ecType` is a **non-const reference**. When the stationary point condition is met, the C++ code modifies `ecType` in place:

```cpp
bool EndCriteria::checkStationaryPoint(..., Type& ecType) const {
    if (/* condition met */) {
        ecType = StationaryPoint;  // Modifies the reference
        return true;
    }
    return false;
}
```

In pure C++, this is fine. The caller passes a local variable by reference, the function modifies it, the caller reads the updated value. Normal pass-by-reference semantics.

But pybind11 enums are **singletons**.

## Understanding pybind11 Enum Singletons

When pybind11 creates a `py::enum_`, each enum value becomes a **singleton object**:

```python
>>> a = ql.EndCriteria.Type.Unknown
>>> b = ql.EndCriteria.Type.Unknown
>>> a is b
True  # Same object!
```

This is efficient and matches Python's enum behavior. But it has a critical implication: there is exactly **one** `Unknown` object for the entire Python process lifetime.

When the binding passes this singleton by reference to a C++ function that modifies it:

1. Python passes the singleton `Unknown` object to C++
2. C++ receives it as `Type& ecType` (reference to the underlying enum)
3. C++ modifies the referenced enum: `ecType = StationaryPoint`
4. The singleton's **internal value** changes from 7 to 2
5. Every subsequent access to `ql.EndCriteria.Type.Unknown` now returns `StationaryPoint`

The singleton is permanently corrupted for the rest of the Python session.

## Why the Debug Script Worked

The debug script ran in a fresh Python interpreter before any `check*` methods were called. The singletons were pristine. Of course `Unknown` was 7.

The pytest failure happened after `test_endcriteria_stationary_point` had already corrupted the `Unknown` singleton by passing it to `checkStationaryPoint()`. By the time `test_endcriteria_static_succeeded` ran, `Unknown` had been mutated to `StationaryPoint`.

Test order mattered. Running tests in isolation worked. Running the full suite failed. Classic symptom of shared mutable state.

## The Fix

The solution: **never pass pybind11 enums by reference to C++ functions that modify them**.

Instead, pass by value and return the modified value as part of a tuple:

```cpp
.def("checkStationaryPoint",
    [](const EndCriteria& self, Real xOld, Real xNew,
       Size statState, EndCriteria::Type ecType) {  // Pass by VALUE
        bool result = self.checkStationaryPoint(xOld, xNew, statState, ecType);
        return py::make_tuple(result, ecType);  // Return modified value
    },
    py::arg("xOld"), py::arg("xNew"),
    py::arg("statState"), py::arg("ecType"),
    "Checks for stationary point. Returns (bool, ecType).")
```

Key changes:

1. **Lambda wrapper**: Can't bind directly, need to intercept the call
2. **Pass by value**: `Type ecType` (no `&`) creates a **copy** of the enum
3. **C++ modifies the copy**: The singleton remains untouched
4. **Return tuple**: `py::make_tuple(result, ecType)` returns both values to Python

From Python's perspective:

```python
# Before: single return value, mysterious side effect
has_ended = end_criteria.checkStationaryPoint(
    xOld=1.0, xNew=1.0000001, statState=10,
    ecType=ql.EndCriteria.Type.Unknown
)
# Unknown singleton is now corrupted!

# After: tuple return, explicit values
has_ended, ecType = end_criteria.checkStationaryPoint(
    xOld=1.0, xNew=1.0000001, statState=10,
    ecType=ql.EndCriteria.Type.Unknown
)
# Unknown singleton unchanged, ecType holds the result
```

After applying this fix to all five `check*` methods, all tests pass. No more singleton corruption.

## The General Pattern

This pattern applies whenever a C++ function takes an enum by reference:

```cpp
// C++ API: modifies enum in place
void someFunction(SomeEnum& e);

// Python binding: pass by value, return modified value
.def("someFunction",
    [](MyClass& self, SomeEnum e) {  // VALUE, not reference
        self.someFunction(e);
        return e;  // Return the potentially modified value
    })

// If the function returns something else, use tuple
.def("someFunction",
    [](MyClass& self, SomeEnum e) {
        ReturnType result = self.someFunction(e);
        return py::make_tuple(result, e);  // Both values
    })
```

In Python:

```python
# Single return value
e = obj.someFunction(MyEnum.Value)

# Tuple unpacking when function returns something else
result, e = obj.someFunction(MyEnum.Value)
```

## When This Doesn't Apply

Not all enum parameters need this treatment:

### Const References (Safe)

```cpp
void processType(const EndCriteria::Type& ecType);  // Can't modify
```

Const references are safe to bind directly. The C++ code can't modify the singleton.

### Pass by Value in C++ (Safe)

```cpp
bool succeeded(EndCriteria::Type ecType);  // Already pass-by-value
```

If the C++ signature already takes the enum by value, bind it directly. No modification can occur.

### Return Values (Safe)

```cpp
EndCriteria::Type getStatus() const;  // Returns enum
```

Returning enums is always safe. pybind11 looks up the singleton for the returned value.

## Why This Isn't Documented

This behavior isn't explicitly documented in pybind11 because it follows from two separate design decisions:

1. **Enums are singletons** - efficient, matches Python semantics
2. **References bind naturally** - convenient for most cases

The interaction between these two features creates the footgun: modifying a singleton via reference corrupts it globally. This is technically "correct" behavior given those design choices, but it's unexpected and violates Python's immutability norms (enums shouldn't spontaneously change their values).

Related pybind11 issues touch on enum identity (pybind11#1177, #2332) but don't explicitly warn about the pass-by-reference danger.

## pybind11 v3 and py::native_enum

pybind11 v3 introduced `py::native_enum`, which uses Python's native `enum` module instead of custom singleton objects. This may behave differently, but as of PyQuantLib's creation, `py::native_enum` has not been tested and `py::enum_` remains the standard approach.

## Usage in PyQuantLib

PyQuantLib uses this pattern for all `EndCriteria::check*` methods:

- `checkMaxIterations` - returns `(bool, ecType)`
- `checkStationaryPoint` - returns `(bool, ecType)`
- `checkStationaryFunctionValue` - returns `(bool, statStateIterations, ecType)`
- `checkStationaryFunctionAccuracy` - returns `(bool, ecType)`
- `checkZeroGradientNorm` - returns `(bool, ecType)`

This pattern is now a project convention documented in {doc}`/contributing` to prevent future singleton corruption bugs.

## The Lesson

Not all C++ idioms translate transparently to Python. Pass-by-reference is cheap and natural in C++, but in pybind11 it can violate Python's expectations about value immutability.

When binding enums:

- **Inspect the C++ signature** - does it take `Type&` (non-const reference)?
- **Check if it modifies** - does the function change the enum value?
- **Use the lambda pattern** - pass by value, return the modified value explicitly

The debug script showing correct values in isolation is the tell-tale sign of singleton corruption. When an enum "works alone but breaks in tests," check for pass-by-reference in the bindings.

Understanding this pattern prevents a whole class of confusing, test-order-dependent failures that look like memory corruption but are actually semantic mismatches between C++'s mutable references and Python's immutable enum expectations.

## See Also

- {doc}`/contributing` for the Enum Pass-by-Reference convention
- [endcriteria.cpp](https://github.com/quantales/pyquantlib/blob/main/src/math/optimization/endcriteria.cpp) for the complete implementation
- [pybind11 enum documentation](https://pybind11.readthedocs.io/en/stable/classes.html#enumerations) for enum binding basics
