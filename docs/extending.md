# Extending PyQuantLib

PyQuantLib supports subclassing QuantLib abstract base classes in Python. This enables rapid prototyping of custom quotes, pricing engines, term structures, and more without writing C++.

## Available Base Classes

Abstract base classes live in `pyquantlib.base`, separate from the main namespace. This separation is intentional: ABCs are not meant to be instantiated directly, so placing them in a submodule makes their usage an explicit choice.

Base classes are organized by category:

| Category | Examples |
|----------|----------|
| Patterns | `Observer`, `Observable`, `LazyObject` |
| Market Data | `Quote` |
| Cash Flows | `CashFlow`, `Coupon` |
| Term Structures | `YieldTermStructure`, `BlackVolTermStructure` |
| Processes | `StochasticProcess`, `StochasticProcess1D` |
| Models | `CalibratedModel` |
| Instruments | `Instrument` |
| Pricing Engines | `PricingEngine`, `GenericEngine` |

To discover all available base classes:

```python
import pyquantlib.base as base
print([name for name in dir(base) if not name.startswith('_')])
```

## Example: Custom Quote

Create a custom quote that returns a time-varying value:

```python
import math
import time
from pyquantlib.base import Quote

class OscillatingQuote(Quote):
    """Quote that oscillates around a base value."""
    
    def __init__(self, base_value, amplitude=0.1):
        super().__init__()
        self._base = base_value
        self._amplitude = amplitude
        self._start = time.time()
    
    def value(self):
        elapsed = time.time() - self._start
        return self._base * (1 + self._amplitude * math.sin(elapsed))
    
    def isValid(self):
        return True
```

Use it anywhere a `Quote` is expected:

```python
import pyquantlib as ql

quote = OscillatingQuote(100.0, amplitude=0.05)
print(f"Current value: {quote.value()}")

# Use in a term structure
vol_surface = ql.BlackConstantVol(
    ql.Date(15, 6, 2025),
    ql.TARGET(),
    ql.QuoteHandle(quote),  # Custom quote works here
    ql.Actual365Fixed()
)
```

## Example: Custom Pricing Engine

The `pyquantlib.extensions` module contains an example of a custom pricing engine: `ModifiedKirkEngine` for spread options.

```python
from pyquantlib.extensions import ModifiedKirkEngine

# Create spread option
payoff = ql.PlainVanillaPayoff(ql.Option.Call, 5.0)
spread_payoff = ql.SpreadBasketPayoff(payoff)
exercise = ql.EuropeanExercise(expiry)
option = ql.BasketOption(spread_payoff, exercise)

# Use custom engine
engine = ModifiedKirkEngine(process1, process2, correlation=0.95)
option.setPricingEngine(engine)
print(f"NPV: {option.NPV():.4f}")
```

The engine subclasses `SpreadBlackScholesVanillaEngine` and implements the `calculate()` method:

```python
from pyquantlib.base import SpreadBlackScholesVanillaEngine

class ModifiedKirkEngine(SpreadBlackScholesVanillaEngine):
    def __init__(self, process1, process2, correlation):
        super().__init__(process1, process2, correlation)
        # Store parameters...
    
    def calculate(self):
        # Get instrument arguments
        args = self.getArguments()
        exercise = args.exercise
        payoff = args.payoff
        
        # Compute price...
        price = self._compute_price(...)
        
        # Set results
        results = self.getResults()
        results.value = price
```

See `examples/03_modified_kirk_engine.ipynb` for a complete walkthrough.

## How It Works

PyQuantLib uses pybind11 "trampoline" classes that intercept virtual method calls and redirect them to Python. When a base class is subclassed and a method is overridden, QuantLib's C++ code calls the Python implementation.

```
QuantLib C++ → Trampoline → Python method
```

This works for all virtual methods in the base classes listed above.

## Performance Considerations

Python method calls have overhead compared to C++. For best performance:

- Keep the number of Python callbacks minimal
- Do heavy computation in NumPy or vectorized operations
- Consider implementing performance-critical engines in C++ and binding them

For prototyping and moderate workloads, Python extensions work well.

## Guidelines

1. **Always call `super().__init__()`** in the constructor
2. **Implement all pure virtual methods** to avoid runtime errors
3. **Return correct types**: QuantLib expects specific return types
4. **Handle exceptions gracefully**: Exceptions in callbacks can cause issues

## See Also

- {doc}`api/extensions` for built-in Python extensions
- `examples/03_modified_kirk_engine.ipynb` for a complete engine example
- `include/pyquantlib/trampolines.h` for the full list of supported base classes
