# The Reference Member Trap

*When a constructor parameter outlives its welcome.*

Most QuantLib classes store `shared_ptr` members by value. A few store them by reference. The distinction is invisible at the API level but creates a use-after-free bug when the class is constructed through pybind11.

## The Setup

`FdmCEVOp` is a finite-difference operator for the Constant Elasticity of Variance model. Its constructor takes a yield term structure:

```cpp
FdmCEVOp(const ext::shared_ptr<FdmMesher>& mesher,
          const ext::shared_ptr<YieldTermStructure>& rTS,
          Real f0, Real alpha, Real beta,
          Size direction);
```

Nothing unusual. Every FDM operator constructor looks like this. The binding follows the standard pattern:

```cpp
py::class_<FdmCEVOp, FdmLinearOpComposite, ext::shared_ptr<FdmCEVOp>>(
    m, "FdmCEVOp", "CEV FDM operator.")
    .def(py::init<const ext::shared_ptr<FdmMesher>&,
                   const ext::shared_ptr<YieldTermStructure>&,
                   Real, Real, Real, Size>(),
         py::arg("mesher"), py::arg("rTS"),
         py::arg("f0"), py::arg("alpha"), py::arg("beta"),
         py::arg("direction"));
```

This compiles. It imports. It constructs the object without error. It crashes later, when `setTime()` or `apply()` tries to dereference `rTS_`.

## The Symptom

```python
op = ql.FdmCEVOp(mesher, flat_curve, 100.0, 0.3, 0.5, 0)
op.setStep(0.01)
op.setTime(0.0, 1.0)  # Access violation or garbage values
```

The crash is not deterministic. Sometimes it works. Sometimes it reads garbage. Sometimes it segfaults. The classic signature of a dangling reference.

## The Cause

Look at the private members:

```cpp
class FdmCEVOp : public FdmLinearOpComposite {
    // ...
private:
    const ext::shared_ptr<YieldTermStructure>& rTS_;  // Reference!
    Size direction_;
    TripleBandLinearOp dxxMap_;
    TripleBandLinearOp mapT_;
};
```

`rTS_` is not a `shared_ptr<YieldTermStructure>`. It is a `const shared_ptr<YieldTermStructure>&` -- a reference to a shared_ptr. The constructor initializes it from its parameter:

```cpp
FdmCEVOp::FdmCEVOp(
    const ext::shared_ptr<FdmMesher>& mesher,
    const ext::shared_ptr<YieldTermStructure>& rTS,  // Parameter
    ...)
: rTS_(rTS),  // Binds reference to parameter
  ...
```

In pure C++ this is fine. The caller owns the `shared_ptr` and keeps it alive for the lifetime of the `FdmCEVOp`. The reference avoids an extra copy and a reference count increment. It is a micro-optimization.

In pybind11, it is a time bomb:

1. Python calls ``op = ql.FdmCEVOp(mesher, flat_curve, ...)``.
2. pybind11 converts ``flat_curve`` into a temporary ``shared_ptr<YTS>`` and passes it to the constructor.
3. The constructor runs. ``rTS_`` binds to the temporary.
4. The constructor returns. The temporary ``shared_ptr`` is destroyed.
5. ``rTS_`` now references deallocated memory.
6. A later call like ``op.setTime(0.0, 1.0)`` reads through the dangling reference -- undefined behavior.

pybind11 converts the Python `flat_curve` object into a `shared_ptr<YieldTermStructure>` and passes it to the constructor. The constructor stores a reference to this temporary. The temporary is destroyed when the constructor returns. `rTS_` survives, pointing at nothing.

## Why It Is Hard to Spot

The bug has three properties that make it insidious:

**It compiles without warnings.** The code is valid C++. The reference binds to a valid object during construction. No compiler or static analyzer flags it, because the problem is about object lifetimes across language boundaries, not about C++ semantics.

**It looks identical to safe patterns.** Compare `FdmCEVOp`'s constructor to `FdmSabrOp`:

```cpp
// FdmCEVOp - dangerous
FdmCEVOp(const ext::shared_ptr<FdmMesher>& mesher,
          const ext::shared_ptr<YieldTermStructure>& rTS, ...);
// Member: const shared_ptr<YTS>& rTS_;   ← reference

// FdmSabrOp - safe
FdmSabrOp(const ext::shared_ptr<FdmMesher>& mesher,
           const ext::shared_ptr<YieldTermStructure>& rTS, ...);
// Member: const shared_ptr<YTS> rTS_;    ← value
```

The constructor signatures are identical. Only the header's private section reveals the difference. One stores a value. The other stores a reference. The distinction is a single `&` character.

**It sometimes works.** If the memory previously occupied by the temporary happens to still contain valid data, the operator produces correct results. The bug only manifests when the memory is reused. In small test programs, the stack frame may not be overwritten before `setTime()` runs. In production code with more allocations between construction and use, the crash is more likely.

## The Fix

The goal: keep the `shared_ptr` alive for the lifetime of the `FdmCEVOp`, without modifying QuantLib source code.

The approach: heap-allocate a copy of the `shared_ptr` and tie its lifetime to the `FdmCEVOp` through a custom deleter.

```cpp
.def(py::init([](const ext::shared_ptr<FdmMesher>& mesher,
                 const ext::shared_ptr<YieldTermStructure>& rTS,
                 Real f0, Real alpha, Real beta, Size direction) {
    // 1. Copy the shared_ptr onto the heap
    auto rTSCopy = ext::make_shared<ext::shared_ptr<YieldTermStructure>>(rTS);

    // 2. Construct FdmCEVOp, passing the heap copy by reference
    //    rTS_ now references *rTSCopy, which lives on the heap
    auto op = ext::shared_ptr<FdmCEVOp>(
        new FdmCEVOp(mesher, *rTSCopy, f0, alpha, beta, direction),
        // 3. Custom deleter captures rTSCopy, preventing destruction
        //    until the FdmCEVOp itself is destroyed
        [rTSCopy](FdmCEVOp* p) { delete p; });
    return op;
}), ...)
```

Three things work together:

1. `make_shared<shared_ptr<YTS>>(rTS)` creates a heap-allocated `shared_ptr` that is a copy of `rTS`. This is a `shared_ptr` to a `shared_ptr` -- two levels of indirection, intentionally.

2. `*rTSCopy` dereferences the outer pointer, yielding a reference to the inner `shared_ptr<YTS>` on the heap. This reference is what `rTS_` binds to. Unlike the stack temporary, this heap object persists.

3. The custom deleter lambda captures `rTSCopy`. As long as the `FdmCEVOp`'s owning `shared_ptr` exists, `rTSCopy` exists, and the heap-allocated `shared_ptr<YTS>` it points to exists. When the `FdmCEVOp` is destroyed, the deleter runs, `rTSCopy` is released, and the yield term structure's reference count decrements normally.

The resulting ownership chain:

- The Python-side ``shared_ptr<FdmCEVOp>`` holds the ``FdmCEVOp`` object. Its custom deleter captures ``rTSCopy``.
- ``rTSCopy`` is a ``shared_ptr`` that owns a heap-allocated ``shared_ptr<YTS>``.
- ``FdmCEVOp::rTS_`` references that heap-allocated ``shared_ptr<YTS>``.
- When the Python holder's reference count reaches zero, the custom deleter runs, releasing ``rTSCopy``. The heap-allocated ``shared_ptr<YTS>`` is destroyed, decrementing the yield term structure's reference count. Everything tears down in the correct order.

## Alternatives Considered

**`py::keep_alive<>`** is pybind11's standard tool for preventing premature destruction. `py::keep_alive<1, 3>()` would tell pybind11 to prevent the third argument (rTS) from being garbage-collected while the first argument (self) exists. But `keep_alive` operates on the Python side. It keeps the Python object alive, which keeps the underlying `shared_ptr` alive. However, it does not keep the *specific temporary* `shared_ptr` that pybind11 created for the C++ constructor call alive. The reference member still dangles because it binds to the temporary, not to the Python object's internal storage.

**Modifying QuantLib** to change the member from `const shared_ptr<T>&` to `shared_ptr<T>` (dropping the reference) would fix the problem at its source. This is the correct long-term fix. `FdmCEVOp` is the only public FDM operator in QuantLib 1.40 with this pattern. It is likely an oversight rather than a deliberate optimization -- the `shared_ptr` copy costs a single atomic increment, and `setTime()` is called per time step where far heavier computation dominates.

**Storing a raw `shared_ptr` in the binding code** and passing it via `std::ref` was considered but rejected. `rTS_` expects a reference to a `shared_ptr`, and the `shared_ptr` must outlive the object. The heap-allocation approach is the only way to guarantee this without modifying the constructor's calling convention.

## Identifying Affected Classes

Grep QuantLib headers for reference-to-shared_ptr members:

```
shared_ptr<.*>&\s+\w+_;
```

In QuantLib 1.40, three hits appear:

| Location | Member | Risk |
|----------|--------|------|
| `FdmCEVOp` | `rTS_` | Exposed in public constructor; **must** workaround |
| `FdmBatesOp::IntegroIntegrand` | `interpl_` | Private inner class; `interpl_` binds to a member of the outer class, so it is safe as long as `FdmBatesOp` exists |
| `TrBDF2Scheme` | `trapezoidalScheme_` | References a member of `TrBDF2Scheme` itself; safe by construction |

Only `FdmCEVOp` requires the workaround. But the pattern could appear in future QuantLib releases, so any new binding should check the header's private section before writing a direct `py::init<>()`.

## The Broader Lesson

C++ binding layers create an impedance mismatch around object lifetimes. C++ constructors assume their callers manage argument lifetimes. pybind11 creates temporaries that live only for the duration of the call. Most of the time this is fine -- constructors copy or move their arguments into members. But a constructor that stores a reference to its argument creates a hidden contract: "keep this alive for me." pybind11 cannot honor contracts it does not know about.

The fix is ugly. Two levels of shared_ptr, a custom deleter, a lambda capture. But it is contained to a single binding function, invisible to the Python user, and correct. The alternative -- a clean binding that crashes in production -- is worse.

## See Also

- [fdmcevop.cpp](https://github.com/quantales/pyquantlib/blob/main/src/methods/finitedifferences/operators/fdmcevop.cpp) for the complete implementation
- [QuantLib FdmCEVOp header](https://github.com/lballabio/QuantLib/blob/master/ql/methods/finitedifferences/operators/fdmcevop.hpp) for the reference member declaration
