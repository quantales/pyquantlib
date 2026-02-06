# The Protected Member Problem

*When inheritance meets access control.*

Python's `self.correlation` looks simple. One dot, one attribute access. But behind this innocent syntax lies a clever trick that bridges C++'s access control with Python's dynamic dispatch. When QuantLib's protected members meet pybind11's lambda bindings, standard approaches fail. The solution? A helper struct that exploits C++ inheritance rules to make the inaccessible accessible.

## The Setup

While implementing `ModifiedKirkEngine` as a Python extension, the calculation method needed access to the correlation parameter stored in the C++ base class:

```python
class ModifiedKirkEngine(ql.base.SpreadBlackScholesVanillaEngine):
    def calculate(self, f1, f2, strike, optionType, variance1, variance2, df):
        rho = self.correlation  # Need this value!

        # Modified Kirk formula uses correlation
        sigma_kirk = math.sqrt(
            sigma1**2 - 2.0 * rho * sigma1 * sigma2 * w + (sigma2 * w)**2
        )
        # ...
```

Simple enough in Python. But how does `self.correlation` get bound to the C++ `rho_` member?

## The Naive Attempt

The first instinct is to expose the member directly in the pybind11 binding:

```cpp
py::class_<SpreadBlackScholesVanillaEngine>(m, "SpreadBlackScholesVanillaEngine")
    .def_property_readonly("correlation", [](const SpreadBlackScholesVanillaEngine& self) {
        return self.rho_;  // Access the protected member
    });
```

Compile this and:

```
error: 'rho_' is a protected member of 'QuantLib::SpreadBlackScholesVanillaEngine'
    return self.rho_;
                ^
```

The compiler refuses. But wait: `rho_` is **protected**, not private. Derived classes should be able to access it, right?

## The Protected Paradox

Here's what makes this confusing. In **pure C++**, a derived class has no problem accessing protected members:

```cpp
class MyEngine : public SpreadBlackScholesVanillaEngine {
public:
    Real calculate(...) const override {
        Real corr = rho_;  // Works fine!
        // Use correlation in calculation
    }
};
```

This compiles without complaint. The derived class is **inside the inheritance hierarchy**, so it has access to protected members.

But the pybind11 lambda is **not inside the class hierarchy**. It's a free function that receives a `const SpreadBlackScholesVanillaEngine&` parameter. From the compiler's perspective, the lambda is an **outsider** trying to peek at protected data.

```cpp
// Lambda is NOT a member function
[](const SpreadBlackScholesVanillaEngine& self) {
    return self.rho_;  // Outsider access - forbidden!
}
```

Even though the lambda is part of the binding code that **creates** the class interface, it doesn't have the access rights of a member function.

## Understanding Access Context

The difference comes down to **where the code runs**:

| Context | Access to `protected` | Why |
|---------|----------------------|-----|
| Derived class member | Allowed | Inside the inheritance hierarchy |
| Friend function | Allowed | Explicitly granted access |
| Lambda in binding | Forbidden | Outside the class, not a friend |
| Free function | Forbidden | No special relationship to class |

C++ access control is checked at **compile time** based on the **lexical context** of the code. A lambda defined outside the class has no special privileges, even if it's "doing work for" the class.

## The Helper Struct Solution

The trick is to create a derived struct **whose sole purpose is to access the protected member**:

```cpp
// Helper struct - IS a derived class
struct SpreadBlackScholesVanillaEngineHelper : SpreadBlackScholesVanillaEngine {
    using SpreadBlackScholesVanillaEngine::SpreadBlackScholesVanillaEngine;

    static Real get_correlation(const SpreadBlackScholesVanillaEngine& self) {
        // Cast to our helper type
        return static_cast<const SpreadBlackScholesVanillaEngineHelper&>(self).rho_;
    }
};
```

This works because:

1. `SpreadBlackScholesVanillaEngineHelper` **is a derived class** → can access protected `rho_`
2. The `get_correlation` method is **inside the class scope** → has inheritance privileges
3. The cast is safe because the helper struct adds no data members → same memory layout
4. The static method can be used as a function pointer in bindings

Now the binding works:

```cpp
py::class_<SpreadBlackScholesVanillaEngine>(m, "SpreadBlackScholesVanillaEngine")
    .def_property_readonly("correlation",
        &SpreadBlackScholesVanillaEngineHelper::get_correlation,
        "Correlation between the two processes");
```

From Python:

```python
engine = ModifiedKirkEngine(process1, process2, 0.95)
rho = engine.correlation  # Works!
```

## Why the Cast Is Safe

The critical line is:

```cpp
return static_cast<const SpreadBlackScholesVanillaEngineHelper&>(self).rho_;
```

This cast looks dangerous, but it's actually safe because:

1. **No added data members**: The helper struct adds **only** methods, no new data
2. **Same memory layout**: `sizeof(Helper) == sizeof(Base)`
3. **Standard layout**: Both types have the same object representation
4. **Pointer compatibility**: A `Base*` and `Derived*` point to the same address

The helper struct is essentially a **transparent wrapper** that exists only to provide member function context for accessing protected members.

## The General Pattern

This technique generalizes to any protected member:

```cpp
// Template for accessing protected members
struct MyClassHelper : MyClass {
    using MyClass::MyClass;  // Inherit constructors

    // For protected data members
    static ReturnType get_member(const MyClass& self) {
        return static_cast<const MyClassHelper&>(self).protected_member_;
    }

    // For protected methods
    static ReturnType call_method(const MyClass& self, Args... args) {
        return static_cast<const MyClassHelper&>(self).protectedMethod(args...);
    }
};

// Bind it
.def_property_readonly("member", &MyClassHelper::get_member)
.def("method", &MyClassHelper::call_method)
```

## When NOT to Use This

Before reaching for the helper struct, consider alternatives:

### 1. Public Getters Exist

If the C++ class provides public accessors, use them directly:

```cpp
class SomeClass {
protected:
    double value_;
public:
    double value() const { return value_; }  // Public getter
};

// Binding - no helper needed
.def_property_readonly("value", &SomeClass::value)
```

### 2. Friend Function Approach

For classes you control, make the binding code a friend:

```cpp
namespace bindings {
    double get_value(const MyClass& self) { return self.value_; }
}

class MyClass {
    friend double bindings::get_value(const MyClass&);
private:
    double value_;
};
```

This works but requires modifying the C++ source.

### 3. Refactor to Public

If many protected members need exposure, consider whether they should be public:

```cpp
// Before: Many protected members
class Engine {
protected:
    double param1_, param2_, param3_;
};

// After: Public interface
class Engine {
public:
    double param1() const { return param1_; }
    double param2() const { return param2_; }
    double param3() const { return param3_; }
private:
    double param1_, param2_, param3_;
};
```

This is cleaner long-term but not always possible with third-party libraries.

## Why QuantLib Uses Protected Members

QuantLib's design philosophy favors **inheritance over getters**:

```cpp
// QuantLib style: Protected data, C++ inheritance
class SpreadBlackScholesVanillaEngine {
protected:
    Real rho_;  // Derived classes access directly
};

class KirkEngine : public SpreadBlackScholesVanillaEngine {
    Real calculate(...) {
        return kirk_formula(rho_, ...);  // Direct access
    }
};
```

Benefits in C++:
- **Less boilerplate**: No getter methods needed
- **Efficient**: No function call overhead (pre-inlining)
- **Clear intent**: Protected signals "for derived classes"

This pattern is common in **C++ class hierarchies designed for inheritance**, where the assumption is that subclassing happens in C++, not Python.

When binding such libraries to Python, the helper struct bridges the gap between C++'s compile-time access control and Python's runtime attribute access.

## Usage in PyQuantLib

PyQuantLib uses this pattern for `SpreadBlackScholesVanillaEngine` to expose the protected `rho_` (correlation) member to Python subclasses.

The same technique can be applied to other QuantLib classes with protected members, such as:
- `YieldTermStructure::referenceDate_`
- `StochasticProcess::discretization_`
- Any other protected member that Python implementations need to access

## The Lesson

C++ access control is **context-dependent**. What works in a derived class member function fails in a lambda or free function, even if both are conceptually "doing the same thing."

The helper struct exploits inheritance to provide the necessary context. It's a compile-time trick that:
- **Respects** C++'s access rules (no casting away `private`)
- **Uses** standard inheritance (no undefined behavior)
- **Enables** Python subclasses to access protected state
- **Maintains** the original class's encapsulation guarantees

This pattern is a **standard technique** in pybind11 bindings for class hierarchies designed with C++ inheritance in mind. Understanding it unlocks the ability to bind sophisticated C++ libraries that use protected members as part of their public inheritance interface.

## See Also

- {doc}`python-subclassing` for the full context of why `ModifiedKirkEngine` needed the correlation value
- [pybind11 documentation on classes](https://pybind11.readthedocs.io/en/stable/classes.html) for other binding patterns
