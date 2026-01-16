# Pricing Engines Module

Pricing engines currently available in PyQuantLib.

## Black Formula Functions

Standalone functions for Black-76 (lognormal) and Bachelier (normal) option pricing.

### Black-76 (Lognormal)

| Function | Description |
|----------|-------------|
| `blackFormula(optionType, strike, forward, stdDev, discount=1.0, displacement=0.0)` | Option price |
| `blackFormulaImpliedStdDev(optionType, strike, forward, blackPrice, ...)` | Implied volatility × √T |
| `blackFormulaImpliedStdDevApproximation(...)` | Fast implied vol approximation |
| `blackFormulaStdDevDerivative(strike, forward, stdDev, ...)` | Vega / √T |
| `blackFormulaVolDerivative(strike, forward, stdDev, expiry, ...)` | Vega |
| `blackFormulaForwardDerivative(optionType, strike, forward, stdDev, ...)` | Delta (forward) |
| `blackFormulaCashItmProbability(optionType, strike, forward, stdDev, ...)` | N(d2) |
| `blackFormulaAssetItmProbability(optionType, strike, forward, stdDev, ...)` | N(d1) |

### Bachelier (Normal)

| Function | Description |
|----------|-------------|
| `bachelierBlackFormula(optionType, strike, forward, stdDev, discount=1.0)` | Option price |
| `bachelierBlackFormulaImpliedVol(optionType, strike, forward, tte, price, ...)` | Implied vol |
| `bachelierBlackFormulaStdDevDerivative(strike, forward, stdDev, ...)` | Vega component |

### Usage

```python
import pyquantlib as ql

# Black-76 call price
forward = 100.0
strike = 100.0
vol = 0.20
T = 1.0
stdDev = vol * (T ** 0.5)  # volatility × √T

price = ql.blackFormula(ql.OptionType.Call, strike, forward, stdDev)
print(f"Call price: {price:.4f}")

# Implied volatility
impliedStdDev = ql.blackFormulaImpliedStdDev(
    ql.OptionType.Call, strike, forward, price
)
impliedVol = impliedStdDev / (T ** 0.5)
print(f"Implied vol: {impliedVol:.2%}")

# Greeks
vega = ql.blackFormulaVolDerivative(strike, forward, stdDev, T)
print(f"Vega: {vega:.4f}")
```

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
