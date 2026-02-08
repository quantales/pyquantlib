# The Diamond Inheritance Problem

*When multiple inheritance meets pybind11's holder system.*

A class that needs two base classes but pybind11 refuses to instantiate it. An error message about "custom holder types" that names the class being constructed but not the real culprit. A fix that migrates an entire inheritance hierarchy and still does not work, until a seemingly unrelated class is changed. This is the story of how pybind11's classic holder system breaks down on diamond-shaped inheritance graphs, and how the `smart_holder` feature in pybind11 3.0 resolves it.

## The Setup

QuantLib's `SabrInterpolatedSmileSection` is a smile section that calibrates SABR parameters to market data. Its inheritance graph forms a double diamond:

```
  Through Observable:              Through Observer:

       Observable                       Observer
        /      \                         /      \
       /        \                       /        \
SmileSection  LazyObject         SmileSection  LazyObject
       \        /                       \        /
        \      /                         \      /
  SabrInterpolated...             SabrInterpolated...
```

The same three bottom classes participate in two overlapping diamonds -- one through `Observable` and one through `Observer` -- forming the classic "Deadly Diamond of Death." Both `SmileSection` and `LazyObject` inherit virtually from both base classes, and `SabrInterpolatedSmileSection` inherits from both middle-layer classes, closing both diamonds.

Multiple inheritance itself is not new to PyQuantLib. `LazyObject` inherits from both `Observer` and `Observable`, for instance. But that forms a simple V shape: two independent parents, no shared ancestor at the leaf. `SabrInterpolatedSmileSection` is the first class encountered during binding where two base classes converge on the same virtual ancestors, closing the diamond.

In C++, virtual inheritance guarantees a single shared instance of each base class in the final object. `SabrInterpolatedSmileSection` has exactly one `Observable` sub-object and exactly one `Observer` sub-object, regardless of the diamonds.

C++ handles this correctly. pybind11 does not.

## The Naive Binding

The initial binding followed the standard pattern:

```cpp
py::class_<SabrInterpolatedSmileSection, SmileSection, LazyObject,
           ext::shared_ptr<SabrInterpolatedSmileSection>>(
    m, "SabrInterpolatedSmileSection", "...")
    .def(py::init<...>(), ...);
```

Build succeeds. Import the module:

```
Unable to load a custom holder type from a default-holder instance
```

The error appears at import time, not when constructing the object. The module cannot even load.

---

## Part I: The Failed Attempts

### Attempt 1: multiple_inheritance Flag

The first attempt followed pybind11's documented approach for multiple inheritance (MI, Multiple Inheritance):

```cpp
py::class_<SmileSection, PySmileSection, ext::shared_ptr<SmileSection>,
           Observer, Observable>(m, "SmileSection", "...")
    .attr("multiple_inheritance") = py::bool_(true);
```

pybind11's `py::multiple_inheritance` flag (and the equivalent `.attr("multiple_inheritance")` attribute) tells the runtime to create a Python type with the `Py_TPFLAGS_BASETYPE` and `Py_TPFLAGS_MULTIPLE_INHERITANCE` flags set. It adjusts how pybind11 computes the Python MRO (Method Resolution Order) and allows listing multiple base classes in the `py::class_` template.

Rebuild, reimport: **same error**. The `py::multiple_inheritance` flag handles Python-level MI but does not address the C++ holder compatibility problem that causes the "custom holder type" error. The issue is in pybind11's C++ type caster, not in Python's MRO.

### Attempt 2: Default Holder (No Explicit shared_ptr)

What if the holder declaration itself is the problem? Maybe omitting the explicit `shared_ptr` avoids the mismatch:

```cpp
py::class_<SabrInterpolatedSmileSection, SmileSection, LazyObject>(
    m, "SabrInterpolatedSmileSection", "...")
```

This fails at compile time with a different error:

```
Type does not have a non-default holder type while its base does
```

pybind11 requires that if a base class declares a `shared_ptr` holder, all derived classes must also declare one. The hierarchy is already committed to `shared_ptr` holders.

---

## Part II: The Partial Solutions

These approaches avoid the diamond entirely. They work, but each sacrifices something.

### Partial Solution 1: Dropping LazyObject

Declare only `SmileSection` as the base and let Python handle `LazyObject` separately:

```cpp
py::class_<SabrInterpolatedSmileSection, SmileSection,
           ext::shared_ptr<SabrInterpolatedSmileSection>>(
    m, "SabrInterpolatedSmileSection", "...")
```

This compiles. Import succeeds. But `isinstance(section, LazyObject)` returns `False`, and calling `recalculate()` (a `LazyObject` method) fails. The calibration feature that makes `SabrInterpolatedSmileSection` useful is inaccessible.

This is exactly what the official [QuantLib-SWIG](https://github.com/lballabio/QuantLib-SWIG) bindings do. In [volatilities.i](https://github.com/lballabio/QuantLib-SWIG/blob/master/SWIG/volatilities.i), `SabrInterpolatedSmileSection` is declared as inheriting from `SmileSection` only, silently dropping the `LazyObject` base that appears in the [C++ header](https://github.com/lballabio/QuantLib/blob/master/ql/termstructures/volatility/sabrinterpolatedsmilesection.hpp). The diamond is avoided by pretending half of it does not exist.

### Partial Solution 2: Implicit Conversion Workaround

A more elaborate approach: avoid declaring any base class in the `py::class_` template and instead use `py::implicitly_convertible` to restore polymorphism:

```cpp
// Define the class WITHOUT base classes in the template parameters
py::class_<SabrInterpolatedSmileSection,
           std::shared_ptr<SabrInterpolatedSmileSection>>
    sabr_section(m, "SabrInterpolatedSmileSection");

// Register implicit conversion so C++ functions expecting SmileSection accept it
py::implicitly_convertible<SabrInterpolatedSmileSection, SmileSection>();

// Bind constructors and SABR-specific methods
sabr_section.def(py::init<...>(), ...)
    .def("alpha", &SabrInterpolatedSmileSection::alpha)
    .def("beta", &SabrInterpolatedSmileSection::beta)
    // ...

// MANUALLY re-expose the SmileSection interface (inheritance is severed)
sabr_section.def("minStrike", &SabrInterpolatedSmileSection::minStrike)
    .def("maxStrike", &SabrInterpolatedSmileSection::maxStrike)
    .def("volatility", ...)
    .def("variance", ...)
    .def("recalculate", &SabrInterpolatedSmileSection::recalculate)
    .def("freeze", &SabrInterpolatedSmileSection::freeze);
```

In principle, this could work for C++ function dispatch: `shared_ptr<SabrInterpolatedSmileSection>` naturally converts to `shared_ptr<SmileSection>` in C++, so passing the object to C++ functions expecting `SmileSection` should succeed through the implicit conversion.

But the trade-offs are significant:

- `isinstance(obj, SmileSection)` returns `False`, breaking Python's type system
- `isinstance(obj, LazyObject)` also returns `False`
- Every `SmileSection` and `LazyObject` method must be manually re-bound, creating maintenance burden
- If QuantLib adds new virtual methods to `SmileSection`, the binding silently becomes incomplete
- Duck typing works (the methods exist), but explicit type checks in user code fail

For a project that aims to preserve the full QuantLib class hierarchy in Python, severing the inheritance was unacceptable.

---

## Part III: The Solution

### The Diagnosis

The error message "Unable to load a custom holder type from a default-holder instance" comes from pybind11's type caster in `cast.h`. It triggers when a type is being loaded through the conversion machinery and the holder types between parent and child are incompatible.

The classic pybind11 holder system (`py::class_<T, shared_ptr<T>>`) computes pointer offsets between `T` and its bases at compile time using `static_cast`. For single inheritance, this works. For diamond inheritance with virtual bases, the paths to `Observable` are ambiguous: `static_cast` cannot compute the correct offset because the offset varies depending on the concrete type. Only `dynamic_cast` can resolve virtual base offsets correctly, and pybind11's classic holder machinery does not use it.

### smart_holder

pybind11 3.0 introduced `py::classh` (short for "class with smart_holder"), an alternative holder system designed specifically for complex inheritance. Instead of compile-time `static_cast` offsets, `smart_holder` performs runtime pointer resolution equivalent to `dynamic_cast`.

The migration requires changing every class in the inheritance chain to `smart_holder`. This is "viral": a `smart_holder` child class cannot have a classic-holder parent. The `smart_holder` needs consistent holder semantics all the way up.

#### Step 1: Migrate the hierarchy

Every class from `Observable` through `SabrInterpolatedSmileSection` must use `py::classh`:

```cpp
// observable.cpp
py::classh<Observable, PyObservable>(m, "Observable", "...")

// observable.cpp (Observer section)
py::classh<Observer, PyObserver>(m, "Observer", "...")

// lazyobject.cpp
py::classh<LazyObject, PyLazyObject,
        Observer, Observable>(m, "LazyObject", "...")

// smilesection.cpp
py::classh<SmileSection, PySmileSection,
           Observer, Observable>(m, "SmileSection", "...")

// sabrinterpolatedsmilesection.cpp
py::classh<SabrInterpolatedSmileSection, SmileSection, LazyObject>(
    m, "SabrInterpolatedSmileSection", "...")
```

Note: `py::classh` does not require (or accept) an explicit holder type argument. The `smart_holder` is implicit.

#### Step 2: Add trampoline_self_life_support

Any trampoline class (used for Python subclassing) must inherit from `py::trampoline_self_life_support` when its binding uses `py::classh`. This ensures the correct reference counting between Python and C++ lifetimes:

```cpp
class PyObservable : public QuantLib::Observable,
                     public py::trampoline_self_life_support { ... };

class PyObserver : public QuantLib::Observer,
                   public py::trampoline_self_life_support { ... };

class PyLazyObject : public QuantLib::LazyObject,
                     public py::trampoline_self_life_support { ... };

class PySmileSection : public QuantLib::SmileSection,
                       public py::trampoline_self_life_support { ... };
```

#### Step 3: Migrate siblings

Any other class that inherits from `SmileSection` must also use `py::classh`, since its parent now uses `smart_holder`:

```cpp
// sabrsmilesection.cpp
py::classh<SabrSmileSection, SmileSection>(...)

// svismilesection.cpp
py::classh<SviSmileSection, SmileSection>(...)
```

After these changes, rebuild. Import the module:

```
Unable to load a custom holder type from a default-holder instance
```

**Still broken.** The entire hierarchy uses `smart_holder`. Every trampoline has `trampoline_self_life_support`. Every sibling is migrated. Yet the same error persists.

### The Hidden Culprit

The `SabrInterpolatedSmileSection` constructor accepts an optional `shared_ptr<EndCriteria>` parameter:

```cpp
.def(py::init<..., const ext::shared_ptr<EndCriteria>&, ...>(), ...)
```

`EndCriteria` was bound as:

```cpp
py::class_<EndCriteria> pyEndCriteria(m, "EndCriteria", "...");
```

No explicit holder. Every other binding in the project so far that uses `EndCriteria` passes it by `const` reference or by value, so the missing holder was never a problem. `SabrInterpolatedSmileSection` is the first and only class that takes `shared_ptr<EndCriteria>` as a constructor parameter, which is why the omission went undetected.

In pybind11 3.0, the default holder is `std::unique_ptr`. When the constructor tries to accept a `shared_ptr<EndCriteria>` argument, pybind11's type caster checks the registered holder for `EndCriteria`, finds `unique_ptr`, and refuses to convert from a "default-holder instance" to the "custom holder type" (`shared_ptr`) that the constructor expects.

The error message says "Unable to load a custom holder type from a default-holder instance." It describes the symptom precisely, but the "custom holder" it refers to is not `SabrInterpolatedSmileSection`'s holder (which is `smart_holder`). It is the `shared_ptr<EndCriteria>` in the constructor parameter.

The fix:

```cpp
py::class_<EndCriteria, ext::shared_ptr<EndCriteria>> pyEndCriteria(m, "EndCriteria", "...");
```

Adding the explicit `shared_ptr` holder to `EndCriteria` allows pybind11 to convert between `shared_ptr<EndCriteria>` and the Python object. This is a standard requirement when any C++ function takes or returns `shared_ptr<T>`: the pybind11 binding for `T` must declare `shared_ptr<T>` as its holder.

After this single-line change, all tests pass. `isinstance(section, SmileSection)` and `isinstance(section, LazyObject)` both return `True`. Calibration, parameter access, and all inherited methods work correctly.

### Why the Error Was Misleading

The holder mismatch error triggers during module initialization when pybind11 processes the `py::init<>()` constructor signature. It iterates over the parameter types, and when it encounters `shared_ptr<EndCriteria>`, it looks up `EndCriteria`'s registered holder. The mismatch between the default `unique_ptr` holder and the requested `shared_ptr` triggers the error.

But the error does not name `EndCriteria`. It names the class being registered (`SabrInterpolatedSmileSection`), because that is the context in which the check fails. This sent the investigation down the diamond inheritance path for hours before the actual one-line fix was discovered.

### The Two Fixes

The final solution required two independent changes: migrating the hierarchy to `py::classh` to enable runtime pointer resolution for the virtual diamond inheritance, and adding an explicit `shared_ptr` holder to `EndCriteria` so the constructor parameter converts correctly.

Both were necessary. Without `py::classh`, the diamond MI does not work regardless of `EndCriteria`. Without the `EndCriteria` holder fix, the constructor parameter fails to convert regardless of `smart_holder`.

The coincidence of needing both fixes simultaneously is what made this problem difficult to diagnose. Each fix was necessary but insufficient on its own, and the error message was identical for both root causes.

## The General Pattern

### When to use py::classh

Use `py::classh` (smart_holder) for any class that participates in diamond-shaped virtual inheritance:

```cpp
// If C inherits from both A and B, and A and B share a virtual base:
py::classh<Base>(m, "Base")
py::classh<A, Base>(m, "A")
py::classh<B, Base>(m, "B")
py::classh<C, A, B>(m, "C")
```

If one class goes smart, they all must go smart. `smart_holder` is viral up the chain.

### Holder declarations for shared_ptr parameters

Any class whose `shared_ptr` appears as a constructor or method parameter in another binding must declare its holder explicitly:

```cpp
// If any binding has: py::arg("x") where x is shared_ptr<T>
// Then T must be bound with:
py::class_<T, ext::shared_ptr<T>>(m, "T", ...)
```

This is true regardless of whether `smart_holder` is in use.

## See Also

- [sabrinterpolatedsmilesection.cpp](https://github.com/quantales/pyquantlib/blob/main/src/termstructures/volatility/sabrinterpolatedsmilesection.cpp) for the diamond MI binding
- [observable.cpp](https://github.com/quantales/pyquantlib/blob/main/src/patterns/observable.cpp) for the `py::classh` migration
- [endcriteria.cpp](https://github.com/quantales/pyquantlib/blob/main/src/math/optimization/endcriteria.cpp) for the holder fix
- [pybind11 smart_holder documentation](https://pybind11.readthedocs.io/en/latest/advanced/smart_holder.html) for the `py::classh` feature
