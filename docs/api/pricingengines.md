# Pricing Engines Module

Pricing engines currently available in PyQuantLib.

## AnalyticEuropeanEngine

Closed-form Black-Scholes pricing for European options.

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticEuropeanEngine
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today

# Setup process (see Processes module)
# ... process = ql.GeneralizedBlackScholesProcess(...)

# Create engine
engine = ql.AnalyticEuropeanEngine(process)

# Price option
option = ql.VanillaOption(payoff, exercise)
option.setPricingEngine(engine)

print(f"NPV:   {option.NPV():.4f}")
print(f"Delta: {option.delta():.4f}")
print(f"Gamma: {option.gamma():.4f}")
print(f"Vega:  {option.vega():.4f}")
print(f"Theta: {option.theta():.4f}")
print(f"Rho:   {option.rho():.4f}")
```

## AnalyticHestonEngine

Closed-form pricing for European options under Heston stochastic volatility.

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticHestonEngine
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

# Setup Heston process and model
heston_process = ql.HestonProcess(
    ql.YieldTermStructureHandle(risk_free),
    ql.YieldTermStructureHandle(dividend),
    ql.QuoteHandle(spot),
    v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
)
heston_model = ql.HestonModel(heston_process)

# Create engine
engine = ql.AnalyticHestonEngine(heston_model)

option.setPricingEngine(engine)
print(f"Heston NPV: {option.NPV():.4f}")
```

```{note}
`AnalyticHestonEngine` computes NPV only. Greeks under Heston require finite difference engines (not yet bound).
```

## MCEuropeanEngine

Monte Carlo pricing for European vanilla options.

```{eval-rst}
.. autoclass:: pyquantlib.MCEuropeanEngine
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

# Monte Carlo with 100,000 paths
mc_engine = ql.MCEuropeanEngine(
    process,
    timeSteps=100,
    requiredSamples=100000,
    seed=42,
)

option.setPricingEngine(mc_engine)
print(f"MC NPV: {option.NPV():.4f}")
print(f"Error estimate: {option.errorEstimate():.6f}")
```

## MCEuropeanBasketEngine

Monte Carlo pricing for European basket options.

```{eval-rst}
.. autoclass:: pyquantlib.MCEuropeanBasketEngine
   :members:
   :undoc-members:
```

## Fd2dBlackScholesVanillaEngine

2D finite difference engine for spread and basket options.

```{eval-rst}
.. autoclass:: pyquantlib.Fd2dBlackScholesVanillaEngine
   :members:
   :undoc-members:
```

## KirkEngine

Kirk approximation for spread options.

```{eval-rst}
.. autoclass:: pyquantlib.KirkEngine
   :members:
   :undoc-members:
```

## StulzEngine

Stulz approximation for two-asset options.

```{eval-rst}
.. autoclass:: pyquantlib.StulzEngine
   :members:
   :undoc-members:
```

```{note}
The abstract `PricingEngine` base class is available in `pyquantlib.base` for custom engine implementations.
```
