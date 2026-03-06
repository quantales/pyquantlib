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

## Short-Rate Processes

### OrnsteinUhlenbeckProcess

```{eval-rst}
.. autoclass:: pyquantlib.OrnsteinUhlenbeckProcess
```

Mean-reverting Ornstein-Uhlenbeck process: $dx = a(r - x)\,dt + \sigma\,dW$.

```python
process = ql.OrnsteinUhlenbeckProcess(speed=0.5, volatility=0.01, x0=0.05, level=0.05)
```

### HullWhiteProcess

```{eval-rst}
.. autoclass:: pyquantlib.HullWhiteProcess
```

Hull-White short-rate process under the risk-neutral measure.

```python
process = ql.HullWhiteProcess(curve, a=0.1, sigma=0.01)
```

### HullWhiteForwardProcess

```{eval-rst}
.. autoclass:: pyquantlib.HullWhiteForwardProcess
```

Hull-White process under the T-forward measure. Adds `M_T(s, t, T)` and `B(t, T)` methods.

```python
process = ql.HullWhiteForwardProcess(curve, a=0.1, sigma=0.01)
process.setForwardMeasureTime(5.0)
```

## Jump-Diffusion Processes

### GeometricBrownianMotionProcess

```{eval-rst}
.. autoclass:: pyquantlib.GeometricBrownianMotionProcess
```

Geometric Brownian motion: $dS = \mu S\,dt + \sigma S\,dW$.

```python
process = ql.GeometricBrownianMotionProcess(initialValue=100.0, mu=0.05, sigma=0.2)
```

### Merton76Process

```{eval-rst}
.. autoclass:: pyquantlib.Merton76Process
```

Merton jump-diffusion process extending Black-Scholes with log-normal jumps.

```python
process = ql.Merton76Process(spot, dividend, risk_free, volatility,
                              jumpIntensity, logMeanJump, logJumpVolatility)
```

### SquareRootProcess

```{eval-rst}
.. autoclass:: pyquantlib.SquareRootProcess
```

CIR-type square root mean-reverting process: $dx = a(b - x)\,dt + \sigma\sqrt{x}\,dW$.

```python
process = ql.SquareRootProcess(b=0.04, a=1.0, sigma=0.2, x0=0.04)
```

### ExtendedOrnsteinUhlenbeckProcess

```{eval-rst}
.. autoclass:: pyquantlib.ExtendedOrnsteinUhlenbeckProcess
```

Extended Ornstein-Uhlenbeck process with time-dependent level $b(t)$.

```python
process = ql.ExtendedOrnsteinUhlenbeckProcess(
    speed=0.5, sigma=0.01, x0=0.05, b=lambda t: 0.05 + 0.01 * t
)
```

## Two-Factor Processes

### G2Process

```{eval-rst}
.. autoclass:: pyquantlib.G2Process
```

G2 two-factor short-rate stochastic process.

```python
process = ql.G2Process(a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
```

### G2ForwardProcess

```{eval-rst}
.. autoclass:: pyquantlib.G2ForwardProcess
```

G2 forward-measure two-factor short-rate process.

## Hybrid Processes

### HybridHestonHullWhiteProcess

```{eval-rst}
.. autoclass:: pyquantlib.HybridHestonHullWhiteProcess
```

Hybrid Heston + Hull-White three-factor stochastic process combining equity stochastic volatility with stochastic interest rates.

```python
hybrid = ql.HybridHestonHullWhiteProcess(
    heston_process, hw_forward_process,
    corrEquityShortRate=0.3,
    discretization=ql.HybridHestonHullWhiteProcess.BSMHullWhite,
)
```

## Multi-Asset Processes

### StochasticProcessArray

```{eval-rst}
.. autoclass:: pyquantlib.StochasticProcessArray
```

## Stochastic Local Volatility

### HestonSLVProcess

```{eval-rst}
.. autoclass:: pyquantlib.HestonSLVProcess
```

Heston stochastic local volatility process combining a Heston process with a leverage function (local vol surface).

```python
heston_process = ql.HestonProcess(
    risk_free, dividend, spot,
    v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
)
leverage_fct = ql.LocalConstantVol(today, 0.20, dc)

slv_process = ql.HestonSLVProcess(heston_process, leverage_fct, mixingFactor=1.0)
```

```{note}
Abstract base classes `StochasticProcess`, `StochasticProcess1D`, `ForwardMeasureProcess`, and `ForwardMeasureProcess1D` are available in `pyquantlib.base` for custom process implementations.
```
