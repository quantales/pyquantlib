# Models Module

## Heston

### HestonModel

```{eval-rst}
.. autoclass:: pyquantlib.HestonModel
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

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseTimeDependentHestonModel
```

### HestonModelHandle

```{eval-rst}
.. autoclass:: pyquantlib.HestonModelHandle
```

### BatesModel

```{eval-rst}
.. autoclass:: pyquantlib.BatesModel
```

Extends `HestonModel` with jump parameters:

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `lambda` | $\lambda$ | Jump intensity |
| `nu` | $\nu$ | Mean jump size |
| `delta` | $\delta$ | Jump size volatility |

```python
bates_process = ql.BatesProcess(
    risk_free, dividend, spot,
    0.04, 1.0, 0.04, 0.5, -0.7,  # v0, kappa, theta, sigma, rho
    0.1, -0.05, 0.1,              # lambda, nu, delta
)
model = ql.BatesModel(bates_process)
engine = ql.BatesEngine(model)
```

## Short Rate Models

### Vasicek

```{eval-rst}
.. autoclass:: pyquantlib.Vasicek
```

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `r0` | $r_0$ | Initial short rate |
| `a` | $a$ | Mean reversion speed |
| `b` | $b$ | Long-term mean rate |
| `sigma` | $\sigma$ | Volatility |

The Vasicek model follows the SDE: $dr_t = a(b - r_t)dt + \sigma dW_t$

```python
vasicek = ql.Vasicek(r0=0.05, a=0.3, b=0.03, sigma=0.01)
```

## Parameters

### Parameter

```{eval-rst}
.. autoclass:: pyquantlib.Parameter
```

### ConstantParameter

```{eval-rst}
.. autoclass:: pyquantlib.ConstantParameter
```

```{note}
Abstract base classes `CalibratedModel` and `CalibrationHelper` are available in `pyquantlib.base` for custom model implementations.
```
