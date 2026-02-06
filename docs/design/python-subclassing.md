# The Python Subclassing Challenge

*When parameter extraction meets the GC.*

Python subclassing of C++ base classes seems straightforward. Inherit from the base, override the calculation method, and it's done. But accessing C++ objects from Python during execution enters a minefield of object lifetime issues.

This is the story of `ModifiedKirkEngine`, a Python subclass that caused **Windows access violations** despite working code. The journey revealed hard lessons about Python/C++ boundary crossings, pybind11 trampolines, and the perils of temporary object wrappers.

## The Setup

The goal was to implement the Modified Kirk approximation for spread options as a Python extension:

```python
class ModifiedKirkEngine(ql.base.SpreadBlackScholesVanillaEngine):
    def __init__(self, process1, process2, correlation):
        super().__init__(process1, process2, correlation)

    def calculate(self):
        # Extract parameters and price the option
        ...
```

The C++ base class `SpreadBlackScholesVanillaEngine` already handles the plumbing. The implementation just needs to override the pricing logic with the Modified Kirk formula. Simple, right?

## The Crash

```
tests/test_modifiedkirkengine.py::test_pricing_integration
Windows fatal exception: access violation
```

The test created processes, built an engine, and called `option.NPV()`. Boom. Immediate crash.

## The Investigation

Adding debug logging revealed something strange:

```python
def calculate(self):
    print("1. Getting processes...")
    process1 = self.process1
    process2 = self.process2
    print("2. Got processes")

    S1 = process1.x0()
    S2 = process2.x0()
    print(f"3. S1={S1}, S2={S2}")

    r1 = process1.riskFreeRate().currentLink()
    print("4. Got r1")
    # ... all 29 steps complete successfully ...
    print("29. SUCCESS!")
    results.value = price
```

The logs showed:
```
29. SUCCESS!
Segmentation fault
```

The entire calculation finished! The crash happened **after** the method returned, during cleanup.

## The Root Cause

The problem wasn't in the calculation. It was in how parameter extraction was being done:

```python
# This line looks innocent but is deadly:
r1 = process1.riskFreeRate().currentLink()
```

Here's what happens:

1. `process1.riskFreeRate()` returns a Python wrapper around a C++ `Handle<YieldTermStructure>`
2. This wrapper is a **temporary object** created on the spot
3. `.currentLink()` is called on this temporary, returning a reference to the underlying term structure
4. The temporary wrapper is destroyed at the end of the expression
5. The reference `r1` is now pointing to memory managed by a deleted Python object

When the method finishes and Python's garbage collector runs, it tries to clean up these dangling references. The C++ objects they point to may already be destroyed, or the destruction order causes double-frees. Either way: **access violation**.

## The Architecture Revelation

Looking at the C++ base class revealed the proper design:

```cpp
// QuantLib's SpreadBlackScholesVanillaEngine::calculate()
void SpreadBlackScholesVanillaEngine::calculate() const {
    // Extract ALL parameters here, in C++
    const Real f1 = process1_->stateVariable()->value()
        / process1_->riskFreeRate()->discount(maturityDate)
        * process1_->dividendYield()->discount(maturityDate);

    const Real f2 = process2_->stateVariable()->value() ...
    const Real variance1 = process1_->blackVolatility()->blackVariance(...);
    const Real variance2 = process2_->blackVolatility()->blackVariance(...);

    // Then call the pricing calculation with pure numbers
    results_.value = calculate(f1, f2, strike, optionType, variance1, variance2, df);
}
```

The base class has **two** `calculate` methods:
- `void calculate() const` - Extracts parameters (implemented in C++)
- `Real calculate(f1, f2, ...) const` - Performs pricing (pure virtual)

Derived classes like `KirkEngine` only override the second method:

```cpp
class KirkEngine : public SpreadBlackScholesVanillaEngine {
    Real calculate(Real f1, Real f2, Real strike, ...) const override {
        // Just do math with the numbers
        return price;
    }
};
```

The C++ base handles all object access and lifetime management. The derived class only does pure computation with numeric parameters. **No Python/C++ boundary crossings during calculation.**

## The Original Mistake

Our Python implementation was doing the opposite:

```python
class ModifiedKirkEngine(ql.base.SpreadBlackScholesVanillaEngine):
    def calculate(self):  # Overriding the WRONG method!
        # Reimplementing parameter extraction in Python
        process1 = self.process1
        S1 = process1.x0()
        r1 = process1.riskFreeRate().currentLink()  # Temporary hell
        ...
```

This approach was:
1. Overriding the no-argument `calculate()` (the extraction method)
2. Reimplementing all the parameter extraction in Python
3. Creating temporary Python wrappers for every C++ object access
4. Suffering the consequences

## The Fix

### Part 1: Fix the Trampoline

The pybind11 trampoline was allowing Python to override the wrong method:

```cpp
// BEFORE: Both methods could be overridden
class PySpreadBlackScholesVanillaEngine : public SpreadBlackScholesVanillaEngine {
    void calculate() const override {
        PYBIND11_OVERRIDE(void, SpreadBlackScholesVanillaEngine, calculate,);
    }

    Real calculate(...) const override {
        PYBIND11_OVERRIDE_PURE(Real, SpreadBlackScholesVanillaEngine, calculate, ...);
    }
};
```

The override for the no-arg version was removed:

```cpp
// AFTER: Only the calculation method can be overridden
class PySpreadBlackScholesVanillaEngine : public SpreadBlackScholesVanillaEngine {
    // Removed: No override for void calculate()
    // This ensures C++ base implementation is always used

    Real calculate(...) const override {
        PYBIND11_OVERRIDE_PURE(Real, SpreadBlackScholesVanillaEngine, calculate, ...);
    }
};
```

Now when `option.NPV()` is called:
1. C++ calls `engine->calculate()` (no args)
2. This **always** uses the C++ base class implementation
3. Which extracts parameters safely in C++
4. Then calls the 7-argument `calculate(f1, f2, ...)`
5. Which Python has overridden
6. Python receives pure numbers, does math, returns a number
7. C++ stores the result

No Python/C++ object access during the calculation. No temporary wrappers. No lifetime issues.

### Part 2: Simplify the Python Implementation

The Python class now only overrides the calculation:

```python
class ModifiedKirkEngine(ql.base.SpreadBlackScholesVanillaEngine):
    def __init__(self, process1, process2, correlation):
        super().__init__(process1, process2, correlation)
        # C++ manages the processes - no need to store them

    def calculate(
        self,
        f1: float,      # All parameters are pure numbers
        f2: float,
        strike: float,
        optionType: ql.OptionType,
        variance1: float,
        variance2: float,
        df: float,
    ) -> float:
        # Pure Python calculation, no C++ object access
        sigma1 = math.sqrt(variance1)
        sigma2 = math.sqrt(variance2)

        # Modified Kirk formula...
        rho = self.correlation  # Access property (safe)
        sigma_kirk = math.sqrt(
            sigma1**2 - 2.0 * rho * sigma1 * sigma2 * w + (sigma2 * w)**2
        )

        # Return the price
        return ql.blackFormula(optionType, K_eff, f1, sigma_modified, df)
```

Clean separation:
- **C++ extracts** → Handles all object lifetime complexity
- **Python calculates** → Works with pure numbers, returns result

## The One Property We Needed

The Python implementation needs access to `correlation`. We exposed it as a read-only property:

```cpp
struct SpreadBlackScholesVanillaEngineHelper : SpreadBlackScholesVanillaEngine {
    static Real get_correlation(const SpreadBlackScholesVanillaEngine& self) {
        return static_cast<const SpreadBlackScholesVanillaEngineHelper&>(self).rho_;
    }
};

.def_property_readonly("correlation",
    &SpreadBlackScholesVanillaEngineHelper::get_correlation,
    "Correlation between the two processes");
```

This is safe because it returns a simple `Real`, not a reference to a managed object.

## Why This Pattern is the Winner

1. **Safety:** All C++ object lifetime management stays in C++. No dangling references, no access violations.

2. **Simplicity:** Python code is pure computation. No need to understand C++ handle semantics or object lifetime rules.

3. **Performance:** Minimal Python/C++ boundary crossings. Parameters are extracted once in C++, calculation happens in Python with numbers.

4. **Correctness:** The C++ base class does parameter extraction the same way for all engines. Consistent behavior.

5. **Maintainability:** Python developers can focus on the pricing logic. They don't need to be C++ experts.

## The Lesson

When subclassing C++ classes in Python with pybind11:

**Let C++ do what C++ does best** (object lifetime, memory management, resource handling)

**Let Python do what Python does best** (high-level logic, algorithms, formulas)

Accessing C++ objects from Python during complex operations creates lifetime issues. The data should cross the boundary once, as simple types (numbers, enums, strings), then computation happens purely in Python.

The trampoline pattern should enforce this separation. Python should not override methods that involve object management. Only the high-level computational methods should be exposed for override.

## Testing the Fix

After the fix:
```
tests/test_modifiedkirkengine.py::test_pricing_integration PASSED
NPV = 2.3438472642728536 ✓
No access violations ✓
Clean execution ✓
```

The Modified Kirk engine now works perfectly, pricing spread options with the enhanced formula while respecting the proper boundaries between C++ and Python.
