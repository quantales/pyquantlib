# The Cross-Translation-Unit Holder Problem

*When compile-time type resolution meets separate files.*

A method binding that compiles cleanly in one file but explodes with a cryptic static_assert in another. An error message that names the correct type but refuses to accept it. A fix that works for one class but not its neighbor. This is the story of how pybind11's holder type system breaks down across translation unit boundaries, and why the simplest return type is sometimes the wrong one.

## The Setup

Binding QuantLib's `SwapIndex` class required exposing a method that returns the underlying swap instrument:

```cpp
class SwapIndex : public InterestRateIndex {
public:
    ext::shared_ptr<VanillaSwap> underlyingSwap(const Date& fixingDate) const;
    // ...
};
```

`SwapIndex` lives in `src/indexes/swapindex.cpp`. `VanillaSwap` is bound in `src/instruments/vanillaswap.cpp`. Two separate files, two separate translation units.

## The Naive Binding

The straightforward approach:

```cpp
// swapindex.cpp
.def("underlyingSwap", &SwapIndex::underlyingSwap,
     py::arg("fixingDate"),
     "Returns the underlying swap for a given fixing date.")
```

This mirrors every other method binding in the project. Compiles cleanly for dozens of similar patterns. Build it:

```
error C2338: static_assert failed:
  'Holder classes are only supported for custom types'
```

## The Wrong Turn

The error message points at pybind11's type caster for `shared_ptr<VanillaSwap>`. Maybe the compiler needs to see the full `VanillaSwap` definition? The include is missing.

```cpp
#include <ql/instruments/vanillaswap.hpp>  // Add full definition
```

Rebuild: **same error**.

The `VanillaSwap` class definition is fully visible. The compiler knows its size, its members, its inheritance. But pybind11 still rejects it.

## A Partial Fix Deepens the Mystery

The same session involved binding `OvernightIndexedSwap`, which has a similar method:

```cpp
ext::shared_ptr<OvernightIndex> overnightIndex() const;
```

`OvernightIndex` is also bound in a different file (`iborindex.cpp`). Same pattern, same error. But adding `#include <ql/indexes/iborindex.hpp>` to `overnightindexedswap.cpp` made that particular error **disappear**.

One include fixed `OvernightIndexedSwap`. The same approach did not fix `SwapIndex`. Two methods with the same pattern, two different outcomes. The asymmetry was the real clue.

## The Root Cause

pybind11 maintains a global registry of bound types. When a class is registered with `py::class_<T, Holder<T>>`, pybind11 records how to convert between `T`, `Holder<T>`, and Python objects. This registration happens at **runtime** during module initialization.

But the type *caster* for holder types uses **compile-time** template specialization. When the compiler encounters a function returning `shared_ptr<VanillaSwap>`, it instantiates `pybind11::detail::type_caster<shared_ptr<VanillaSwap>>`. This caster checks at compile time whether `VanillaSwap` has been declared as a pybind11-bound type in the current translation unit.

In `vanillaswap.cpp`, the `py::class_<VanillaSwap, ...>` declaration is visible. The caster knows the type. In `swapindex.cpp`, it is not. The caster sees `VanillaSwap` as an unknown type and triggers the static_assert.

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│  swapindex.cpp              │     │  vanillaswap.cpp            │
│                             │     │                             │
│  underlyingSwap() returns   │     │  py::class_<VanillaSwap,    │
│  shared_ptr<VanillaSwap>    │     │    FixedVsFloatingSwap,     │
│                             │     │    shared_ptr<VanillaSwap>> │
│  Compiler: "VanillaSwap     │     │                             │
│   is not a registered       │     │  Registration happens       │
│   pybind11 type here"       │     │  HERE, at runtime           │
│                             │     │                             │
│  static_assert FAILS        │     │  static_assert PASSES       │
└─────────────────────────────┘     └─────────────────────────────┘
```

Why did the `OvernightIndex` include fix work but `VanillaSwap` did not? Because `OvernightIndex` is declared inside `iborindex.hpp` together with pybind11-compatible traits that the compiler could resolve. The specific conditions under which the compile-time check passes or fails depend on header inclusion order, template instantiation timing, and which intermediate types are visible. It is not reliably predictable.

## The Fix

The solution: defer type resolution from compile time to runtime using `py::cast()`.

```cpp
.def("underlyingSwap", [](const SwapIndex& self, const Date& fixingDate)
         -> py::object {
         return py::cast(self.underlyingSwap(fixingDate));
     },
     py::arg("fixingDate"),
     "Returns the underlying swap for a given fixing date.")
```

Three changes work together:

1. **Lambda wrapper** intercepts the return value before pybind11's automatic type conversion
2. **`py::cast()`** performs the `shared_ptr<VanillaSwap>` to Python conversion at **runtime**, when all types across all translation units are already registered in the global registry
3. **`-> py::object`** tells pybind11 the return type is a generic Python object, bypassing the compile-time holder type check entirely

At runtime, `py::cast()` looks up `VanillaSwap` in the global type registry, finds the registration from `vanillaswap.cpp`, and performs the conversion correctly. The Python user receives a fully typed `VanillaSwap` object with all its methods available.

## The Trade-off

This pattern is a pragmatic compromise:

| Aspect | Direct binding | `py::cast()` pattern |
|--------|---------------|---------------------|
| Compile-time type safety | Full | None (returns `py::object`) |
| Runtime behavior | Correct | Correct |
| Stub type hints | Specific type | `object` |
| Performance | Direct conversion | Extra registry lookup |
| Cross-TU support | Fails | Works |

The performance overhead is negligible. The loss of compile-time safety is the real cost. But since pybind11 bindings are not typically type-checked at the C++ level anyway (Python is the consumer), this trade-off is acceptable.

The stub type hints showing `object` instead of `VanillaSwap` is the most visible impact. A custom stubgen post-processing step could fix this if precise return types become important.

## Alternatives Considered

Two other approaches could avoid the problem entirely:

**Combine related bindings into one translation unit.** If `SwapIndex` and `VanillaSwap` lived in the same `.cpp` file, the compiler would see both `py::class_<>` registrations. No lambda, no `py::cast()`, full compile-time safety. The cost: abandoning the 1:1 file mapping convention that keeps the codebase navigable. Knowing that `ql/instruments/vanillaswap.hpp` maps to `src/instruments/vanillaswap.cpp` is worth preserving as the binding count grows.

**Forward-declare pybind11 type registrations in a shared header.** If pybind11 offered a way to declare "this type will be registered elsewhere," the caster could defer its check. But pybind11's type system has no such mechanism. The `py::class_<>` declaration is both the registration and the compile-time signal, and it cannot be split.

The `py::cast()` pattern is the pragmatic middle ground: keep the files separate, accept the minor runtime indirection.

## The General Pattern

Any method returning `shared_ptr<T>` where `T` is registered in a different translation unit needs this treatment:

```cpp
// Instead of:
.def("method", &Class::method)

// Use:
.def("method", [](const Class& self, args...) -> py::object {
    return py::cast(self.method(args...));
}, py::arg("arg1"), ...)
```

In PyQuantLib, this pattern appears in three places:

- `SwapIndex::underlyingSwap()` returns `shared_ptr<VanillaSwap>` (bound in `vanillaswap.cpp`)
- `OvernightIndexedSwapIndex::overnightIndex()` returns `shared_ptr<OvernightIndex>` (bound in `iborindex.cpp`)
- `OvernightIndexedSwap::overnightIndex()` returns `shared_ptr<OvernightIndex>` (bound in `iborindex.cpp`)

## When This Does Not Apply

Most method bindings do not need this pattern:

- **Return types bound in the same file**: The compiler sees the `py::class_<>` declaration. Direct binding works.
- **Primitive return types**: `int`, `double`, `std::string` have built-in casters. No registration needed.
- **Void methods**: Nothing to convert.
- **Types passed as arguments**: pybind11 resolves argument types differently. The issue is specific to return type conversion.

## The Structural Tension

This problem is a direct consequence of two reasonable design choices pulling in opposite directions:

1. **pybind11's compile-time type resolution** provides zero-overhead conversions and catches type errors early. It assumes the types a function returns are visible in the same compilation context.

2. **PyQuantLib's separate binding files convention** (one `.cpp` per QuantLib class) keeps the codebase organized and reduces compilation coupling. It assumes each file is self-contained.

The tension is inherent. Any pybind11 project that splits bindings across files and has methods returning types from other files will encounter this. The alternative of putting all bindings in one file would eliminate the problem but create a monolithic compilation unit that defeats the purpose of modular organization.

The `py::cast()` pattern resolves the tension by moving one specific operation from compile time to runtime, exactly where pybind11's global type registry lives. It is not elegant, but it is honest about where the type information actually resides.

## See Also

- [swapindex.cpp](https://github.com/quantales/pyquantlib/blob/main/src/indexes/swapindex.cpp) for the complete implementation
- [overnightindexedswap.cpp](https://github.com/quantales/pyquantlib/blob/main/src/instruments/overnightindexedswap.cpp) for another instance
- [pybind11 type caster documentation](https://pybind11.readthedocs.io/en/stable/advanced/cast/index.html) for how type resolution works
