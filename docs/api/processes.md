# Processes Module

Stochastic processes for asset price dynamics.

## Black-Scholes Processes

### GeneralizedBlackScholesProcess

The most flexible Black-Scholes process — supports term structure handles.

```{eval-rst}
.. autoclass:: pyquantlib.GeneralizedBlackScholesProcess
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today
dc = ql.Actual365Fixed()

# Market data
spot = ql.SimpleQuote(100.0)
rate = ql.SimpleQuote(0.05)
vol = ql.SimpleQuote(0.20)

# Term structures
risk_free = ql.FlatForward(today, ql.QuoteHandle(rate), dc)
dividend = ql.FlatForward(today, 0.0, dc)
volatility = ql.BlackConstantVol(today, ql.TARGET(), ql.QuoteHandle(vol), dc)

# Create process
process = ql.GeneralizedBlackScholesProcess(
    ql.QuoteHandle(spot),
    ql.YieldTermStructureHandle(dividend),
    ql.YieldTermStructureHandle(risk_free),
    ql.BlackVolTermStructureHandle(volatility),
)

# Access process properties
print(process.x0())              # Initial value (spot)
print(process.riskFreeRate())    # Risk-free rate handle
print(process.dividendYield())   # Dividend yield handle
print(process.blackVolatility()) # Volatility handle
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

Stochastic volatility process.

```{eval-rst}
.. autoclass:: pyquantlib.HestonProcess
   :members:
   :undoc-members:
```

### Model Parameters

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `v0` | $v_0$ | Initial variance |
| `kappa` | $\kappa$ | Mean reversion speed |
| `theta` | $\theta$ | Long-term variance |
| `sigma` | $\sigma$ | Vol of vol |
| `rho` | $\rho$ | Correlation between spot and vol |

### Dynamics

$$dS_t = (r - q) S_t dt + \sqrt{v_t} S_t dW^S_t$$
$$dv_t = \kappa(\theta - v_t) dt + \sigma \sqrt{v_t} dW^v_t$$
$$\langle dW^S, dW^v \rangle = \rho dt$$

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

# Heston parameters
v0 = 0.04      # Initial variance (vol = 20%)
kappa = 1.0    # Mean reversion speed
theta = 0.04   # Long-term variance
sigma = 0.5    # Vol of vol
rho = -0.7     # Spot-vol correlation (typically negative for equities)

# Create Heston process
heston_process = ql.HestonProcess(
    ql.YieldTermStructureHandle(risk_free),
    ql.YieldTermStructureHandle(dividend),
    ql.QuoteHandle(spot),
    v0, kappa, theta, sigma, rho,
)

# Access parameters
print(heston_process.v0())
print(heston_process.kappa())
print(heston_process.theta())
print(heston_process.sigma())
print(heston_process.rho())
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
