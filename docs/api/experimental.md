# Experimental Module

Bindings for QuantLib's experimental features (`ql/experimental/`).

```{warning}
These features are from QuantLib's experimental namespace and may change in future releases.
```

## Volatility

### SviSmileSection

```{eval-rst}
.. autoclass:: pyquantlib.SviSmileSection
```

The SVI (Stochastic Volatility Inspired) model parametrizes total variance:

$$w(k) = a + b \left( \rho (k - m) + \sqrt{(k - m)^2 + \sigma^2} \right)$$

where $k = \log(K/F)$ is the log-moneyness.

**Parameters** (passed as vector `[a, b, sigma, rho, m]`):

| Parameter | Description | Constraint |
|-----------|-------------|------------|
| `a` | Vertical translation (level) | $a + b\sigma\sqrt{1-\rho^2} \geq 0$ |
| `b` | Slope | $b \geq 0$, $b(1+\lvert\rho\rvert) \leq 4$ |
| `sigma` | ATM curvature ($\sigma$) | $\sigma > 0$ |
| `rho` | Rotation/skew ($\rho$) | $-1 < \rho < 1$ |
| `m` | Horizontal translation | - |

```python
import pyquantlib as ql

# SVI parameters: [a, b, sigma, rho, m]
svi_params = [0.04, 0.1, 0.3, -0.4, 0.0]

# Create smile section (T=1y, F=100)
smile = ql.SviSmileSection(1.0, 100.0, svi_params)

# Query volatilities
print(smile.volatility(100.0))  # ATM vol
print(smile.volatility(110.0))  # OTM call vol

# Price options
call_price = smile.optionPrice(110.0, ql.OptionType.Call)
```

## Callable Bonds

### CallableBondVolatilityStructure

```{eval-rst}
.. autoclass:: pyquantlib.base.CallableBondVolatilityStructure
```

Abstract base class for callable-bond volatility term structures.

### CallableBondConstantVolatility

```{eval-rst}
.. autoclass:: pyquantlib.CallableBondConstantVolatility
```

```python
vol = ql.CallableBondConstantVolatility(today, 0.10, ql.Actual365Fixed())
# or with a Quote
vol = ql.CallableBondConstantVolatility(today, ql.SimpleQuote(0.10),
                                         ql.Actual365Fixed())
```

### TreeCallableFixedRateBondEngine

```{eval-rst}
.. autoclass:: pyquantlib.TreeCallableFixedRateBondEngine
```

### TreeCallableZeroCouponBondEngine

```{eval-rst}
.. autoclass:: pyquantlib.TreeCallableZeroCouponBondEngine
```

```python
hw_model = ql.HullWhite(curve_handle, 0.03, 0.01)
engine = ql.TreeCallableFixedRateBondEngine(hw_model, 100)
bond.setPricingEngine(engine)
print(bond.cleanPrice())
```

### BlackCallableFixedRateBondEngine

```{eval-rst}
.. autoclass:: pyquantlib.BlackCallableFixedRateBondEngine
```

### BlackCallableZeroCouponBondEngine

```{eval-rst}
.. autoclass:: pyquantlib.BlackCallableZeroCouponBondEngine
```

```python
# Black engine requires exactly one call/put date
vol = ql.CallableBondConstantVolatility(today, 0.10, dc)
engine = ql.BlackCallableFixedRateBondEngine(vol, discount_curve)
bond.setPricingEngine(engine)
print(bond.cleanPrice())
print(bond.impliedVolatility(target_price, curve, 1e-8, 200, 0.001, 0.50))
```

## Credit

### CdsOption

```{eval-rst}
.. autoclass:: pyquantlib.CdsOption
```

### BlackCdsOptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.BlackCdsOptionEngine
```

### SVI Helper Functions

```{eval-rst}
.. autofunction:: pyquantlib.sviTotalVariance
```

```{eval-rst}
.. autofunction:: pyquantlib.checkSviParameters
```

```python
# Compute total variance directly
k = 0.1  # log-moneyness
var = ql.sviTotalVariance(0.04, 0.1, 0.3, -0.4, 0.0, k)

# Validate parameters (raises on invalid)
ql.checkSviParameters(0.04, 0.1, 0.3, -0.4, 0.0, 1.0)
```
