# Models Module

Pricing models for derivatives valuation.

## Heston Model

The Heston stochastic volatility model.

```{eval-rst}
.. autoclass:: pyquantlib.HestonModel
   :members:
   :undoc-members:
```

### Model Parameters

The Heston model describes the evolution of an asset with stochastic volatility:

$$dS_t = (r - q) S_t dt + \sqrt{v_t} S_t dW^S_t$$
$$dv_t = \kappa(\theta - v_t) dt + \sigma \sqrt{v_t} dW^v_t$$

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `v0` | $v_0$ | Initial variance |
| `kappa` | $\kappa$ | Mean reversion speed |
| `theta` | $\theta$ | Long-term variance |
| `sigma` | $\sigma$ | Volatility of variance (vol of vol) |
| `rho` | $\rho$ | Correlation between spot and variance |

### Usage

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today
dc = ql.Actual365Fixed()

# Market data
spot = ql.SimpleQuote(100.0)
risk_free = ql.FlatForward(today, 0.05, dc)
dividend = ql.FlatForward(today, 0.02, dc)

# Create Heston process
heston_process = ql.HestonProcess(
    ql.YieldTermStructureHandle(risk_free),
    ql.YieldTermStructureHandle(dividend),
    ql.QuoteHandle(spot),
    v0=0.04,      # Initial variance
    kappa=1.0,    # Mean reversion
    theta=0.04,   # Long-term variance
    sigma=0.5,    # Vol of vol
    rho=-0.7,     # Correlation
)

# Create model
model = ql.HestonModel(heston_process)

# Access parameters
print(model.v0())
print(model.kappa())
print(model.theta())
print(model.sigma())
print(model.rho())
```

## HestonModelHandle

Handle for Heston model (for lazy evaluation).

```{eval-rst}
.. autoclass:: pyquantlib.HestonModelHandle
   :members:
   :undoc-members:
```

## PiecewiseTimeDependentHestonModel

Heston model with time-dependent parameters.

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseTimeDependentHestonModel
   :members:
   :undoc-members:
```

## Parameters

### Parameter

Base class for model parameters.

```{eval-rst}
.. autoclass:: pyquantlib.Parameter
   :members:
   :undoc-members:
```

### ConstantParameter

A constant (time-independent) parameter.

```{eval-rst}
.. autoclass:: pyquantlib.ConstantParameter
   :members:
   :undoc-members:
```

## Using Heston with Pricing Engines

```python
import pyquantlib as ql

# Setup (assumes process and model from above)
payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
option = ql.VanillaOption(payoff, exercise)

# Analytic Heston engine
engine = ql.AnalyticHestonEngine(model)
option.setPricingEngine(engine)

print(f"Heston NPV: {option.NPV():.4f}")
```

```{note}
Abstract base classes `CalibratedModel` and `CalibrationHelper` are available in `pyquantlib.base` for custom model implementations.
```
