# The Settings Singleton Mystery

*A tale of duplicate instances, static libraries, and Python attribute shadowing.*

Every QuantLib program begins the same way: set the evaluation date.

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
```

Simple enough. Except, during early development, this line did absolutely nothing. Prices came out wrong. Discount factors were bizarre. The evaluation date appeared to be stuck at some default value, no matter what we assigned.

This article documents two investigations: a C++ linking bug that created duplicate singletons, and a Python attribute shadowing bug that bypassed the property setter entirely. Both produced the same symptom -- the evaluation date appeared correct but calculations were wrong.

## The Symptom

The code looked correct:

```python
today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today

# Verify the assignment
print(ql.Settings.instance().evaluationDate)  # Prints: June 15th, 2025
```

The print statement showed the correct date. But pricing engines behaved as if the date was never set. Discount factors were wrong. Option prices made no sense.

## The Investigation

### Hypothesis 1: Property Binding Bug

Perhaps the property setter was not actually calling QuantLib's assignment operator?

```cpp
.def_property("evaluationDate",
    [](const Settings& self) { return static_cast<Date>(self.evaluationDate()); },
    [](Settings& self, const Date& d) { self.evaluationDate() = d; })
```

Adding debug prints confirmed the setter was being called. The C++ side received the correct date. Dead end.

### Hypothesis 2: Copy vs Reference

Maybe `Settings::instance()` was returning a copy instead of a reference?

```cpp
static Settings& instance();  // QuantLib's declaration
```

No, QuantLib returns a reference. And pybind11 was configured with `py::return_value_policy::reference`. Dead end.

### Hypothesis 3: Multiple Instances

This hypothesis seemed absurd. `Settings` is a singleton. There can only be one instance. That is the entire point of the pattern.

But let us check anyway:

```cpp
// In QuantLib's settings.cpp
Settings& Settings::instance() {
    static Settings instance_;
    return instance_;
}
```

A static local variable. The classic Meyers singleton. One instance per... wait.

One instance per *what*?

## The Root Cause

In C++, a static local variable has one instance *per translation unit that contains its definition*. When QuantLib is built as a **shared library** (DLL on Windows, .so on Linux), and then linked into a Python extension module, something unexpected happens.

The Python extension module (`_pyquantlib.pyd`) links against `QuantLib.dll`. When Python imports the extension:

1. `QuantLib.dll` is loaded. It has its own `Settings::instance()` with its own static `instance_`.
2. The extension module's code calls `Settings::instance()`. But due to how dynamic linking works, the call may resolve to a *different* static variable.

The result: two `Settings` singletons. The Python binding writes to one. The QuantLib pricing code reads from the other.

```
┌─────────────────────┐     ┌─────────────────────┐
│  _pyquantlib.pyd    │     │   QuantLib.dll      │
│                     │     │                     │
│  Settings::instance │     │  Settings::instance │
│  ┌───────────────┐  │     │  ┌───────────────┐  │
│  │ evaluationDate│◄─┼─────┼──│ evaluationDate│  │
│  │ = June 15     │  │     │  │ = (default)   │  │
│  └───────────────┘  │     │  └───────────────┘  │
│                     │     │         ▲           │
│  Python writes here │     │  C++ reads here     │
└─────────────────────┘     └─────────────────────┘
```

The assignment succeeds. The getter returns the correct value (reading from the same instance we wrote to). But QuantLib's internal code uses a completely different instance.

## The Solution

The fix is straightforward once the cause is understood: **build QuantLib as a static library**.

When QuantLib is statically linked into the Python extension, there is only one copy of `Settings::instance()`. No duplicate singletons. No silent data loss.

```bash
cmake .. \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DQL_USE_STD_SHARED_PTR=ON \
  -DQL_USE_STD_OPTIONAL=ON \
  -DQL_USE_STD_ANY=ON
```

The key flags:

| Flag | Purpose |
|------|---------|
| `BUILD_SHARED_LIBS=OFF` | Static library, not shared |
| `CMAKE_POSITION_INDEPENDENT_CODE=ON` | Required for linking into a shared Python extension |
| `QL_USE_STD_*` | Use standard library types for ABI compatibility |

With static linking, the singleton is embedded directly into `_pyquantlib.pyd`. There is only one `Settings::instance()`. Python and C++ share the same evaluation date.

## Why This Was Hard to Debug

Several factors made this bug particularly insidious:

1. **The getter worked.** Reading `evaluationDate` returned the value we just wrote. The bug only manifested in code paths that used the *other* singleton.

2. **No error messages.** Both singletons functioned correctly in isolation. Nothing threw an exception or logged a warning.

3. **Platform-dependent.** The exact behavior depends on the linker and operating system. Some configurations might accidentally work.

4. **Singletons are supposed to be single.** The mental model of "one instance" is so ingrained that questioning it feels wrong.

The Settings singleton mystery cost a day of debugging. The fix was a one-line CMake change. Such is the nature of linking bugs: obvious in hindsight, invisible until understood.

## The Python API Trap

With static linking solved, the natural binding was:

```python
# Expose the Settings class
ql.Settings.instance().evaluationDate = today
```

This worked. But during a large pytest run, a subtle variant crept in:

```python
ql.Settings.evaluationDate = today
```

The missing `.instance()` call changes everything. `ql.Settings` here is the *class object*, not an instance. Python allows setting arbitrary attributes on classes. So this line silently creates a new class attribute called `evaluationDate` -- a plain `Date` object sitting on the class dict. The property descriptor on the instance is never invoked. QuantLib's C++ singleton never receives the date.

The same debugging pattern repeated: reading `ql.Settings.evaluationDate` returned the "correct" value (the class attribute), but all calculations used the wrong date. The bug surfaced not at the point of assignment, but hundreds of tests later as wrong prices and discount factors.

### The Fix

Export `Settings` as the singleton instance, not the class:

```python
# In __init__.py
Settings = _ql.Settings.instance()
```

Now `ql.Settings` *is* the instance. Both spellings reach the same property setter:

```python
ql.Settings.evaluationDate = today               # works: property setter on instance
ql.Settings.instance().evaluationDate = today     # also works: redundant but harmless
```

The first form is the intended API. The second still works because `instance()` returns `self` (the same singleton). There is no class object in the Python namespace to accidentally shadow.
