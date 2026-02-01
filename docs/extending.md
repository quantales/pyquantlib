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

## Example: Custom Smile Section

The `pyquantlib.extensions` module contains `SviSmileSection`, a pure Python implementation of the SVI volatility smile. It subclasses `SmileSection` and implements the required virtual methods:

```python
import math
from pyquantlib.base import SmileSection

class SviSmileSection(SmileSection):
    """SVI smile section: w(k) = a + b*(rho*(k-m) + sqrt((k-m)^2 + sigma^2))"""

    def __init__(self, time_to_expiry, forward, svi_params):
        super().__init__()
        self._time = time_to_expiry
        self._forward = forward
        self._a, self._b, self._sigma, self._rho, self._m = svi_params

    def minStrike(self):
        return 0.0

    def maxStrike(self):
        return float("inf")

    def atmLevel(self):
        return self._forward

    def volatilityImpl(self, strike):
        k = math.log(strike / self._forward)
        w = self._a + self._b * (
            self._rho * (k - self._m)
            + math.sqrt((k - self._m) ** 2 + self._sigma ** 2)
        )
        return math.sqrt(max(w, 1e-10) / self._time)
```

Use it anywhere a `SmileSection` is expected:

```python
from pyquantlib.extensions import SviSmileSection

params = [0.04, 0.1, 0.3, -0.4, 0.0]  # [a, b, sigma, rho, m]
smile = SviSmileSection(1.0, 100.0, params)

print(f"ATM vol: {smile.volatility(100.0):.4f}")
print(f"90 strike: {smile.volatility(90.0):.4f}")
```

See `pyquantlib/extensions/svi_smile_section.py` for the complete implementation with parameter validation, and {doc}`examples/04_svi_smile` for usage examples.

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
- {doc}`examples/04_svi_smile` for a complete SVI smile example
- {doc}`examples/05_modified_kirk_engine` for a custom pricing engine example
- `include/pyquantlib/trampolines.h` for the full list of supported base classes
