# Processes Module

## Black-Scholes Processes

### GeneralizedBlackScholesProcess

```{eval-rst}
.. autoclass:: pyquantlib.GeneralizedBlackScholesProcess
```

```python
spot = ql.SimpleQuote(100.0)
risk_free = ql.FlatForward(today, 0.05, dc)
dividend = ql.FlatForward(today, 0.0, dc)
volatility = ql.BlackConstantVol(today, ql.TARGET(), 0.20, dc)

# Pythonic API: handles created internally
process = ql.GeneralizedBlackScholesProcess(spot, dividend, risk_free, volatility)

# Explicit handle construction
process = ql.GeneralizedBlackScholesProcess(
    ql.QuoteHandle(spot),
    ql.YieldTermStructureHandle(dividend),
    ql.YieldTermStructureHandle(risk_free),
    ql.BlackVolTermStructureHandle(volatility),
)
```

### BlackScholesProcess

```{eval-rst}
.. autoclass:: pyquantlib.BlackScholesProcess
```

### BlackScholesMertonProcess

```{eval-rst}
.. autoclass:: pyquantlib.BlackScholesMertonProcess
```

## Heston Process

### HestonProcess

```{eval-rst}
.. autoclass:: pyquantlib.HestonProcess
```

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `v0` | $v_0$ | Initial variance |
| `kappa` | $\kappa$ | Mean reversion speed |
| `theta` | $\theta$ | Long-term variance |
| `sigma` | $\sigma$ | Vol of vol |
| `rho` | $\rho$ | Correlation between spot and vol |

```python
heston_process = ql.HestonProcess(
    risk_free, dividend, spot,
    v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
)
```

### BatesProcess

```{eval-rst}
.. autoclass:: pyquantlib.BatesProcess
```

Extends `HestonProcess` with jump parameters:

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
```

## Multi-Asset Processes

### StochasticProcessArray

```{eval-rst}
.. autoclass:: pyquantlib.StochasticProcessArray
```

```{note}
Abstract base classes `StochasticProcess` and `StochasticProcess1D` are available in `pyquantlib.base` for custom process implementations.
```
