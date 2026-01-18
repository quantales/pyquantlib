# Models Module

## Heston

### HestonModel

The Heston stochastic volatility model.

```{eval-rst}
.. autoclass:: pyquantlib.HestonModel
   :members:
   :undoc-members:
```

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `v0` | $v_0$ | Initial variance |
| `kappa` | $\kappa$ | Mean reversion speed |
| `theta` | $\theta$ | Long-term variance |
| `sigma` | $\sigma$ | Volatility of variance (vol of vol) |
| `rho` | $\rho$ | Correlation between spot and variance |

```python
heston_process = ql.HestonProcess(
    ql.YieldTermStructureHandle(risk_free),
    ql.YieldTermStructureHandle(dividend),
    ql.QuoteHandle(spot),
    v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
)
model = ql.HestonModel(heston_process)

engine = ql.AnalyticHestonEngine(model)
option.setPricingEngine(engine)
```

### PiecewiseTimeDependentHestonModel

Heston model with time-dependent parameters.

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseTimeDependentHestonModel
   :members:
   :undoc-members:
```

### HestonModelHandle

Handle for Heston model (for lazy evaluation).

```{eval-rst}
.. autoclass:: pyquantlib.HestonModelHandle
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

```{note}
Abstract base classes `CalibratedModel` and `CalibrationHelper` are available in `pyquantlib.base` for custom model implementations.
```
