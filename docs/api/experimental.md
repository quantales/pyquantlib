# Experimental

Bindings for QuantLib's `ql/experimental/` namespace: features that are functional but whose interfaces may change in future QuantLib releases. PyQuantLib mirrors them as-is.

```{warning}
The classes on this page live in QuantLib's experimental namespace. Their constructor signatures and observable behaviour can shift with a QuantLib version bump.
```

## At a glance

| Class | Role |
|---|---|
| {py:class}`pyquantlib.SviSmileSection` | C++ SVI smile section. Pure-Python equivalent in {py:class}`pyquantlib.extensions.SviSmileSection`. |
| {py:class}`pyquantlib.CallableBondConstantVolatility` | Flat short-rate volatility structure used by callable-bond pricing engines. |
| {py:class}`pyquantlib.TreeCallableFixedRateBondEngine` / `...ZeroCouponBondEngine` | Lattice-based engines for callable bonds (drives a short-rate tree off the model and curve). |
| {py:class}`pyquantlib.BlackCallableFixedRateBondEngine` / `...ZeroCouponBondEngine` | Black-formula engines for callable bonds with exactly one call/put date. |
| {py:class}`pyquantlib.CdsOption` | Credit-default-swap option instrument. |
| {py:class}`pyquantlib.BlackCdsOptionEngine` | Black-formula engine for CDS options. |

## Common patterns

### Build an SVI smile section

```python
import pyquantlib as ql

# SVI parameter vector: [a, b, sigma, rho, m]
svi_params = [0.04, 0.1, 0.3, -0.4, 0.0]
smile = ql.SviSmileSection(1.0, 100.0, svi_params)

print(smile.volatility(100.0))                       # ATM vol
print(smile.volatility(110.0))                       # OTM call vol
print(smile.optionPrice(110.0, ql.OptionType.Call))  # Black-76 call price
```

The SVI parameterisation models *total variance*

$$w(k) = a + b \left( \rho (k - m) + \sqrt{(k - m)^2 + \sigma^2} \right)$$

where $k = \log(K / F)$ is log-moneyness.

| Parameter | Role | Binding-validated constraint |
|---|---|---|
| `a` | Vertical level | $a + b \sigma \sqrt{1 - \rho^2} \geq 0$ |
| `b` | Slope at the wings | $b \geq 0$, $b (1 + \lvert \rho \rvert) \leq 4$ |
| `sigma` | ATM curvature | $\sigma > 0$ |
| `rho` | Skew / rotation | $-1 < \rho < 1$ |
| `m` | Horizontal shift | (no constraint) |

The constructor and `ql.checkSviParameters(...)` validate these. Pass `validate=False` to skip the checks.

### Price a callable bond with a tree engine

```python
hw_model = ql.HullWhite(curve_handle, 0.03, 0.01)
engine   = ql.TreeCallableFixedRateBondEngine(hw_model, 100)   # 100 tree steps
bond.setPricingEngine(engine)
print(bond.cleanPrice())
```

### Price a callable bond with the Black engine

```python
vol    = ql.CallableBondConstantVolatility(today, 0.10, ql.Actual365Fixed())
engine = ql.BlackCallableFixedRateBondEngine(vol, discount_curve)
bond.setPricingEngine(engine)
print(bond.cleanPrice())
print(bond.impliedVolatility(target_price, curve, 1e-8, 200, 0.001, 0.50))
```

The Black engine assumes a single call or put date; for multiple call/put dates use a tree engine.

## Reference

### Volatility

```{eval-rst}
.. autoclass:: pyquantlib.SviSmileSection
```

```{eval-rst}
.. autofunction:: pyquantlib.sviTotalVariance
```

```{eval-rst}
.. autofunction:: pyquantlib.checkSviParameters
```

### Callable bonds

```{eval-rst}
.. autoclass:: pyquantlib.base.CallableBondVolatilityStructure
```

```{eval-rst}
.. autoclass:: pyquantlib.CallableBondConstantVolatility
```

```{eval-rst}
.. autoclass:: pyquantlib.TreeCallableFixedRateBondEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.TreeCallableZeroCouponBondEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackCallableFixedRateBondEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackCallableZeroCouponBondEngine
```

### Credit

```{eval-rst}
.. autoclass:: pyquantlib.CdsOption
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackCdsOptionEngine
```

## See also

- {doc}`extensions`: pure-Python `SviSmileSection` equivalent and `ModifiedKirkEngine`
- {doc}`models`: `HullWhite` and other short-rate models used by the tree-callable engines
