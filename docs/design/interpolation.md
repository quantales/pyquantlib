# The Interpolation Binding Saga

*A tale of lifetimes and iterators.*

Binding C++ to Python is usually straightforward: wrap a class, expose some methods, and move on. But sometimes, a C++ design pattern fundamentally clashes with Python's memory model.

In QuantLib, that nemesis is **Interpolation**.

This article documents the journey to bind `QuantLib::Interpolation`. It describes the three failed attempts that taught us hard lessons about memory management, and the four working solutions we discovered, culminating in the "Stateful Deleter" pattern used today.

## The Core Conflict

QuantLib's interpolation classes are designed to be lightweight **views**. They do not own their data.

```cpp
// C++
std::vector<double> x = {1.0, 2.0};
std::vector<double> y = {10.0, 20.0};

// The interpolation stores iterators to x and y.
// It assumes x and y will outlive it!
LinearInterpolation interp(x.begin(), x.end(), y.begin());
```

Python, however, is **value-based**. Users expect to pass a list and forget about it:

```python
# Python
interp = ql.LinearInterpolation([1.0, 2.0], [10.0, 20.0])
# The lists are temporary! They die immediately after this line.
```

If we bind the constructor directly, the Python list is converted to a temporary C++ `std::vector`, iterators are extracted, and then the vector is destroyed. The interpolation is left holding **dangling iterators**---pointers to memory that no longer exists.

---

## Part I: The Failed Attempts

We tried to solve this "dangling iterator" problem in three ways that seemed logical but failed.

### Attempt 1: The `py::keep_alive` Hope

*The "Maybe Python can save us" approach.*

The thought: if we tell pybind11 to keep the arguments alive, the data will not die.

```cpp
.def(py::init([](const std::vector<Real>& x, const std::vector<Real>& y) {
    return new LinearInterpolation(x.begin(), x.end(), y.begin());
}), py::keep_alive<1, 2>(), py::keep_alive<1, 3>()); // Keep x and y alive?
```

**Why it failed:** `py::keep_alive` keeps the *Python object* alive. But `std::vector<Real>` is a **C++ temporary** created during the conversion from Python list to C++. The Python object lives, but the C++ vector holding the actual doubles is destroyed as soon as the constructor returns.

### Attempt 2: The Lambda Capture

*The "Closure" approach.*

We tried to trick the compiler by capturing the vectors in a lambda or a dummy function to extend their life.

```cpp
.def(py::init([](std::vector<Real> x, std::vector<Real> y) {
    auto x_ptr = std::make_shared<std::vector<Real>>(x);
    auto interp = new LinearInterpolation(x_ptr->begin(), ...);

    // Attempt to stash x_ptr somewhere...
    py::cpp_function prevent_gc([x_ptr](){});
    return interp;
}));
```

**Why it failed:** The closure itself has no owner. As soon as the lambda returns, the closure is destroyed, the `shared_ptr` refcount drops to zero, and the data vanishes.

### Attempt 3: The Naive Wrapper

*The "Box" approach.*

We created a C++ wrapper class to hold the data and the interpolation.

```cpp
class Wrapper {
    std::vector<Real> x_, y_;
    ext::shared_ptr<LinearInterpolation> interp_;
public:
    Wrapper(std::vector<Real> x, ...) : x_(x), ... {
        interp_ = make_shared<LinearInterpolation>(x_.begin(), ...);
    }
};

// In binding:
.def(py::init([](std::vector<Real> x, ...) {
    auto wrapper = new Wrapper(x, y);
    return wrapper->interp_; // Return the interpolation
}));
```

**Why it failed:** We returned `wrapper->interp_` to Python. Python received the Interpolation object but knew nothing about the `Wrapper`. The `Wrapper` (and the vectors inside it) went out of scope immediately. The interpolation was once again an orphan.

---

## Part II: The Working Solutions

Through trial and error, we found four ways to actually solve this. We present them in increasing order of sophistication.

### Solution 1: Inheritance + Injection

*The "Internal" approach.*

Instead of using `LinearInterpolation`, we create a subclass that owns the data and manually constructs the internal implementation logic.

```cpp
class PyLinearInterpolation : public Interpolation {
    std::vector<Real> x_, y_; // Data owned here
public:
    PyLinearInterpolation(const std::vector<Real>& x, const std::vector<Real>& y)
    : x_(x), y_(y) {
        // Manually instantiate the impl using internal detail headers
        impl_ = ext::shared_ptr<Impl>(
            new detail::LinearInterpolationImpl(x_.begin(), x_.end(), y_.begin())
        );
    }
};
```

**Verdict:** Robust. It works.

**Drawback:** It relies on `detail` headers (`quantlib/math/interpolations/linearinterpolation.hpp`). If QuantLib refactors its internals, this breaks.

### Solution 2: Composition

*The "SWIG" approach.*

This is the approach used by QuantLib-SWIG. We create a `SafeInterpolation` class that wraps the data and the object, and expose *that* to Python.

```cpp
class SafeInterpolation {
    std::vector<Real> x_, y_;
    LinearInterpolation f_;
public:
    SafeInterpolation(x, y) : x_(x), y_(y), f_(x_.begin(), ...) {}
    Real operator()(Real x) { return f_(x); } // Proxy call
};
```

**Verdict:** Safe.

**Drawback:** The Python object is of type `SafeInterpolation`, not `QuantLib::Interpolation`. `isinstance(obj, ql.Interpolation)` fails. We also have to manually re-bind every method (`primitive`, `derivative`, etc.).

### Solution 3: Handle Assignment

*The "Hybrid" approach.*

`QuantLib::Interpolation` is just a handle (a smart pointer wrapper). We can inherit from it, store the data, create a temporary standard interpolation, and assign it to ourselves.

```cpp
class PyLinearInterpolation : public Interpolation {
    std::vector<Real> x_, y_;
public:
    PyLinearInterpolation(x, y) : x_(x), y_(y) {
        // Create temp using our stable member data
        LinearInterpolation temp(x_.begin(), x_.end(), y_.begin());
        // Assign the implementation handle to *this
        this->impl_ = temp.impl_;
    }
};
```

**Verdict:** Excellent. Clean C++, no internal headers.

**Drawback:** We still have to define a `Py...` class for every interpolation type.

---

## Part III: The Ultimate Solution

### Solution 4: The Stateful Deleter

*The ultimate approach.*

This is the solution we chose. It relies on a powerful feature of `std::shared_ptr`: **Custom Deleters**.

A `shared_ptr` can store a custom "deleter" object alongside the pointer. This deleter is destroyed only when the `shared_ptr` refcount hits zero. We can use this to store the data *inside the deleter*.

#### The Mechanism

1. Define a `Holder` struct that contains the `std::vector`s.
2. Use `std::vector`'s **move semantics**. The C++ standard guarantees that moving a vector does *not* invalidate iterators to its elements.
3. Store the `Holder` inside the `shared_ptr` that we return to Python.

#### The Implementation

```cpp
// The Secret Sauce
struct InterpolationDataHolder {
    std::vector<Real> x, y;
    void operator()(LinearInterpolation* p) const { delete p; }
};

// The Binding
.def(py::init([](std::vector<Real> x, std::vector<Real> y) {
    // 1. Move data into a holder
    InterpolationDataHolder holder{std::move(x), std::move(y)};

    // 2. Create Interpolation using pointers to holder's data
    // (Move semantics guarantee these iterators stay valid)
    auto* p = new LinearInterpolation(holder.x.begin(), ...);

    // 3. Return shared_ptr with the holder AS the deleter
    // The data now lives in the shared_ptr control block!
    return ext::shared_ptr<LinearInterpolation>(p, std::move(holder));
}))
```

#### Why This is the Winner

1. **Type Purity:** Python sees a pure `QuantLib::LinearInterpolation`. No `PyLinear` subclasses, no `Safe` wrappers.
2. **Polymorphism:** The object is fully polymorphic in C++. It can be passed to any C++ function expecting an `Interpolation`.
3. **Safety:** The data is tied to the object's lifetime. It is impossible to delete the data while the object is alive.

### Bonus: The Generic Factory

Since this logic is identical for almost all interpolation types (`Linear`, `LogLinear`, `Cubic`, etc.), we packaged Solution 4 into a generic template helper:

```cpp
// usage in module.cpp
pyql::bind_interpolation_class<LinearInterpolation>(m, "LinearInterpolation");
pyql::bind_interpolation_class<CubicInterpolation>(m, "CubicInterpolation");
```

This gave us the best of all worlds: rigorous memory safety, native C++ types, and clean, readable binding code.

