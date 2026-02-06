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
| Term Structures | `YieldTermStructure`, `BlackVolTermStructure`, `SmileSection` |
| Processes | `StochasticProcess`, `StochasticProcess1D` |
| Models | `CalibratedModel` |
| Instruments | `Instrument` |
| Pricing Engines | `PricingEngine`, `GenericEngine`, `SpreadBlackScholesVanillaEngine` |

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

The custom quote can be used anywhere a `Quote` is expected:

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

## Pure Python Extensions

The `pyquantlib.extensions` module provides complete Python extension examples that can be used in production or as templates for custom implementations.

### SVI Smile Section

`SviSmileSection` implements the SVI (Stochastic Volatility Inspired) volatility parametrization. It subclasses `SmileSection` to provide a volatility smile that can be used with any QuantLib component expecting a smile section.

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

Usage:

```python
from pyquantlib.extensions import SviSmileSection

params = [0.04, 0.1, 0.3, -0.4, 0.0]  # [a, b, sigma, rho, m]
smile = SviSmileSection(1.0, 100.0, params)

print(f"ATM vol: {smile.volatility(100.0):.4f}")
print(f"90 strike: {smile.volatility(90.0):.4f}")
```

See [04_svi_smile.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/04_svi_smile.ipynb) for a complete example including comparison with the C++ implementation.

### Modified Kirk Engine

`ModifiedKirkEngine` implements the Modified Kirk approximation for spread option pricing. It subclasses `SpreadBlackScholesVanillaEngine` and demonstrates how to build a custom pricing engine in pure Python.

The modification adds a skew correction term from Alos & Leon (2015) that improves accuracy for high correlation cases.

```{important}
When subclassing pricing engines, **only override the calculation method with numeric parameters**, not the parameter extraction method. Let the C++ base class handle object lifetime management. See {doc}`design/python-subclassing` for details.
```

```python
from pyquantlib.base import SpreadBlackScholesVanillaEngine

class ModifiedKirkEngine(SpreadBlackScholesVanillaEngine):
    """Modified Kirk engine with skew correction for spread options."""

    def __init__(self, process1, process2, correlation):
        super().__init__(process1, process2, correlation)
        # C++ base class manages process lifetime - no need to store them

    def calculate(
        self,
        f1: float,          # Forward price of first asset
        f2: float,          # Forward price of second asset
        strike: float,      # Strike price
        optionType,         # Call or Put
        variance1: float,   # Variance of first asset
        variance2: float,   # Variance of second asset
        df: float,          # Discount factor
    ) -> float:
        """
        Calculate spread option price using Modified Kirk approximation.

        This method is called by the C++ base class after it extracts
        all parameters from the instrument. This avoids Python/C++
        object lifetime issues.
        """
        # Access correlation from base class property
        rho = self.correlation

        # Compute price using Modified Kirk formula with numeric parameters
        price = self._calculate_price(f1, f2, strike, optionType,
                                     variance1, variance2, df, rho)

        return price
```

Usage:

```python
import pyquantlib as ql
from pyquantlib.extensions import ModifiedKirkEngine

# Create spread option
payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 5.0)
spread_payoff = ql.SpreadBasketPayoff(payoff)
exercise = ql.EuropeanExercise(expiry)
option = ql.BasketOption(spread_payoff, exercise)

# Use custom engine
engine = ModifiedKirkEngine(process1, process2, correlation=0.95)
option.setPricingEngine(engine)
print(f"NPV: {option.NPV():.4f}")
```

See [05_modified_kirk_engine.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/05_modified_kirk_engine.ipynb) for a complete walkthrough including comparison with QuantLib's built-in `KirkEngine`.

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
5. **Minimize Python/C++ boundary crossings during execution**
   - ✓ **Do**: Override methods with simple types (numbers, enums, strings)
   - ✓ **Do**: Let C++ base class handle object access and lifetime management
   - ✗ **Don't**: Access C++ objects (handles, term structures, processes) from Python
   - ✗ **Don't**: Extract parameters yourself - let the base class do it

   **Why**: Temporary Python wrappers around C++ objects can cause dangling
   references and access violations. Keep C++ object access in C++, keep
   computation in Python.

   **Examples**:
   - Pricing engines: Override `calculate(f1, f2, ...)` not `calculate()`
   - Term structures: Override `discountImpl(time)` not `discount(date)`
   - Processes: Override `drift(t, x)` with numbers, not object accessors

   See {doc}`design/python-subclassing` for detailed explanation.

## See Also

- {doc}`api/extensions` for the complete API reference
- [04_svi_smile.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/04_svi_smile.ipynb) for the SVI smile section example
- [05_modified_kirk_engine.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/05_modified_kirk_engine.ipynb) for the custom pricing engine example
- `include/pyquantlib/trampolines.h` for the full list of supported base classes
