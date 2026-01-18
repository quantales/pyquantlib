# Processes Module

## Black-Scholes Processes

### GeneralizedBlackScholesProcess

The most flexible Black-Scholes process: supports term structure handles.

```{eval-rst}
.. autoclass:: pyquantlib.GeneralizedBlackScholesProcess
   :members:
   :undoc-members:
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

Black-Scholes process without dividends.

```{eval-rst}
.. autoclass:: pyquantlib.BlackScholesProcess
   :members:
   :undoc-members:
```

### BlackScholesMertonProcess

Black-Scholes-Merton process with continuous dividend yield.

```{eval-rst}
.. autoclass:: pyquantlib.BlackScholesMertonProcess
   :members:
   :undoc-members:
```

## Heston Process

### HestonProcess

Stochastic volatility process.

```{eval-rst}
.. autoclass:: pyquantlib.HestonProcess
   :members:
   :undoc-members:
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

## Multi-Asset Processes

### StochasticProcessArray

Array of correlated stochastic processes for basket options.

```{eval-rst}
.. autoclass:: pyquantlib.StochasticProcessArray
   :members:
   :undoc-members:
```

```{note}
Abstract base classes `StochasticProcess` and `StochasticProcess1D` are available in `pyquantlib.base` for custom process implementations.
```
