# Processes

Bindings for `StochasticProcess` and its subclasses: the SDE drivers fed to MC engines, FD engines, and (where applicable) calibrated models. Each process exposes the same minimal interface (`drift`, `diffusion`, `evolve`, `initialValues`, ...); concrete subclasses differ in the SDE they implement and the constructor parameters that pin it down.

## At a glance

| Family | Classes |
|---|---|
| Black-Scholes | {py:class}`pyquantlib.GeneralizedBlackScholesProcess`, {py:class}`pyquantlib.BlackScholesProcess`, {py:class}`pyquantlib.BlackScholesMertonProcess` |
| Heston / Bates | {py:class}`pyquantlib.HestonProcess`, {py:class}`pyquantlib.BatesProcess` |
| Short-rate | {py:class}`pyquantlib.OrnsteinUhlenbeckProcess`, {py:class}`pyquantlib.HullWhiteProcess`, {py:class}`pyquantlib.HullWhiteForwardProcess` |
| Jump / square-root | {py:class}`pyquantlib.GeometricBrownianMotionProcess`, {py:class}`pyquantlib.Merton76Process`, {py:class}`pyquantlib.SquareRootProcess`, {py:class}`pyquantlib.ExtendedOrnsteinUhlenbeckProcess` |
| Two-factor | {py:class}`pyquantlib.G2Process`, {py:class}`pyquantlib.G2ForwardProcess` |
| Hybrid | {py:class}`pyquantlib.HybridHestonHullWhiteProcess` |
| Multi-asset | {py:class}`pyquantlib.StochasticProcessArray` |
| Stochastic local vol | {py:class}`pyquantlib.HestonSLVProcess` |

```{note}
Abstract base classes `StochasticProcess`, `StochasticProcess1D`, `ForwardMeasureProcess`, and `ForwardMeasureProcess1D` are exposed under `pyquantlib.base` for custom process subclassing.
```

## Common patterns

### Build a Black-Scholes process

```python
import pyquantlib as ql

spot       = ql.SimpleQuote(100.0)
risk_free  = ql.FlatForward(today, 0.05, dc)
dividend   = ql.FlatForward(today, 0.0, dc)
volatility = ql.BlackConstantVol(today, ql.TARGET(), 0.20, dc)

# Pythonic: handles created internally.
process = ql.GeneralizedBlackScholesProcess(spot, dividend, risk_free, volatility)

# Explicit handle construction.
process = ql.GeneralizedBlackScholesProcess(
    ql.QuoteHandle(spot),
    ql.YieldTermStructureHandle(dividend),
    ql.YieldTermStructureHandle(risk_free),
    ql.BlackVolTermStructureHandle(volatility),
)
```

The two constructors accept the same inputs in different shapes; the binding wraps quotes / curves / vol surfaces in handles automatically when handed bare objects.

### Build a Heston process

```python
process = ql.HestonProcess(
    risk_free, dividend, spot,
    v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
)
```

The constructor argument order is `(v0, kappa, theta, sigma, rho)`. This is *not* the same order as `HestonModel.params()`, which returns `(theta, kappa, sigma, rho, v0)`; use kwargs to keep things unambiguous.

### Build a Heston-SLV process

```python
heston       = ql.HestonProcess(risk_free, dividend, spot,
                                v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7)
leverage_fct = ql.LocalConstantVol(today, 0.20, dc)
slv          = ql.HestonSLVProcess(heston, leverage_fct, mixingFactor=1.0)
```

The leverage function is any `LocalVolTermStructure`. `mixingFactor` blends pure local vol (factor 0) with pure Heston (factor 1).

## Reference

### Black-Scholes processes

```{eval-rst}
.. autoclass:: pyquantlib.GeneralizedBlackScholesProcess
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackScholesProcess
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackScholesMertonProcess
```

### Heston and Bates

```{eval-rst}
.. autoclass:: pyquantlib.HestonProcess
```

| Parameter | Symbol |
|---|---|
| `v0` | $v_0$ |
| `kappa` | $\kappa$ |
| `theta` | $\theta$ |
| `sigma` | $\sigma$ |
| `rho` | $\rho$ |

```{eval-rst}
.. autoclass:: pyquantlib.BatesProcess
```

`BatesProcess` extends Heston with three jump parameters:

| Parameter | Symbol |
|---|---|
| `lambda` | $\lambda$ |
| `nu` | $\nu$ |
| `delta` | $\delta$ |

### Short-rate processes

```{eval-rst}
.. autoclass:: pyquantlib.OrnsteinUhlenbeckProcess
```

SDE: $dx = a(r - x)\,dt + \sigma\,dW$.

```{eval-rst}
.. autoclass:: pyquantlib.HullWhiteProcess
```

Hull-White short-rate process under the risk-neutral measure.

```{eval-rst}
.. autoclass:: pyquantlib.HullWhiteForwardProcess
```

Hull-White process under the $T$-forward measure. Adds `M_T(s, t, T)` and `B(t, T)` methods.

```python
process = ql.HullWhiteForwardProcess(curve, a=0.1, sigma=0.01)
process.setForwardMeasureTime(5.0)
```

### Jump-diffusion and square-root processes

```{eval-rst}
.. autoclass:: pyquantlib.GeometricBrownianMotionProcess
```

SDE: $dS = \mu S\,dt + \sigma S\,dW$.

```{eval-rst}
.. autoclass:: pyquantlib.Merton76Process
```

Merton jump-diffusion: Black-Scholes plus log-normal jumps.

```{eval-rst}
.. autoclass:: pyquantlib.SquareRootProcess
```

SDE: $dx = a(b - x)\,dt + \sigma\sqrt{x}\,dW$.

```{eval-rst}
.. autoclass:: pyquantlib.ExtendedOrnsteinUhlenbeckProcess
```

Extended Ornstein-Uhlenbeck with time-dependent level $b(t)$.

```python
process = ql.ExtendedOrnsteinUhlenbeckProcess(
    speed=0.5, sigma=0.01, x0=0.05,
    b=lambda t: 0.05 + 0.01 * t,
)
```

### Two-factor processes

```{eval-rst}
.. autoclass:: pyquantlib.G2Process
```

```{eval-rst}
.. autoclass:: pyquantlib.G2ForwardProcess
```

### Hybrid processes

```{eval-rst}
.. autoclass:: pyquantlib.HybridHestonHullWhiteProcess
```

```python
hybrid = ql.HybridHestonHullWhiteProcess(
    heston_process, hw_forward_process,
    corrEquityShortRate=0.3,
    discretization=ql.HybridHestonHullWhiteProcess.BSMHullWhite,
)
```

### Multi-asset processes

```{eval-rst}
.. autoclass:: pyquantlib.StochasticProcessArray
```

### Stochastic local volatility

```{eval-rst}
.. autoclass:: pyquantlib.HestonSLVProcess
```

## See also

- {doc}`/concepts/stochastic-processes`: the process / engine wiring and what each family covers
- {doc}`models`: calibrated models built on top of these processes (`HestonModel`, `HullWhite`, `G2`, ...)
- {doc}`pricingengines`: engines that consume these processes
