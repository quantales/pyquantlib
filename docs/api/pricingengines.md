# Pricing Engines Module

## Vanilla Engines

### AnalyticEuropeanEngine

Closed-form Black-Scholes pricing for European options.

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticEuropeanEngine
   :members:
   :undoc-members:
```

```python
import pyquantlib as ql

engine = ql.AnalyticEuropeanEngine(process)
option.setPricingEngine(engine)

print(f"NPV:   {option.NPV():.4f}")
print(f"Delta: {option.delta():.4f}")
print(f"Gamma: {option.gamma():.4f}")
print(f"Vega:  {option.vega():.4f}")
```

### AnalyticHestonEngine

Closed-form pricing for European options under Heston stochastic volatility.

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticHestonEngine
   :members:
   :undoc-members:
```

```python
heston_process = ql.HestonProcess(
    ql.YieldTermStructureHandle(risk_free),
    ql.YieldTermStructureHandle(dividend),
    ql.QuoteHandle(spot),
    v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
)
heston_model = ql.HestonModel(heston_process)
engine = ql.AnalyticHestonEngine(heston_model)
```

```{note}
`AnalyticHestonEngine` computes NPV only. Greeks under Heston require finite difference engines.
```

### BaroneAdesiWhaleyApproximationEngine

Barone-Adesi and Whaley (1987) quadratic approximation for American options.

```{eval-rst}
.. autoclass:: pyquantlib.BaroneAdesiWhaleyApproximationEngine
   :members:
   :undoc-members:
```

### BjerksundStenslandApproximationEngine

Bjerksund and Stensland (1993) approximation for American options.

```{eval-rst}
.. autoclass:: pyquantlib.BjerksundStenslandApproximationEngine
   :members:
   :undoc-members:
```

### BinomialVanillaEngine

Binomial tree pricing for vanilla options (European, American, Bermudan).

```{eval-rst}
.. autoclass:: pyquantlib.BinomialVanillaEngine
   :members:
   :undoc-members:
```

```python
engine = ql.BinomialVanillaEngine(process, "crr", 801)
```

Tree types: `jr`, `crr`, `eqp`, `trigeorgis`, `tian`, `lr`, `joshi`

### FdBlackScholesVanillaEngine

1D finite difference engine for vanilla options.

```{eval-rst}
.. autoclass:: pyquantlib.FdBlackScholesVanillaEngine
   :members:
   :undoc-members:
```

```python
engine = ql.FdBlackScholesVanillaEngine(
    process,
    tGrid=100,
    xGrid=100,
    schemeDesc=ql.FdmSchemeDesc.Douglas(),
)
```

### MCEuropeanEngine

Monte Carlo pricing for European vanilla options.

```{eval-rst}
.. autoclass:: pyquantlib.MCEuropeanEngine
   :members:
   :undoc-members:
```

```python
engine = ql.MCEuropeanEngine(
    process,
    timeSteps=100,
    requiredSamples=100000,
    seed=42,
)
option.setPricingEngine(engine)
print(f"NPV: {option.NPV():.4f}")
print(f"Error: {option.errorEstimate():.6f}")
```

### MCAmericanEngine

Monte Carlo pricing for American options using Longstaff-Schwartz least-squares regression.

```{eval-rst}
.. autoclass:: pyquantlib.MCAmericanEngine
   :members:
   :undoc-members:
```

```python
engine = ql.MCAmericanEngine(
    process,
    timeSteps=100,
    antitheticVariate=True,
    calibrationSamples=4096,
    requiredTolerance=0.02,
    seed=42,
)
```

## Basket Engines

### MCEuropeanBasketEngine

Monte Carlo pricing for European basket options.

```{eval-rst}
.. autoclass:: pyquantlib.MCEuropeanBasketEngine
   :members:
   :undoc-members:
```

### Fd2dBlackScholesVanillaEngine

2D finite difference engine for spread and basket options.

```{eval-rst}
.. autoclass:: pyquantlib.Fd2dBlackScholesVanillaEngine
   :members:
   :undoc-members:
```

### KirkEngine

Kirk approximation for spread options.

```{eval-rst}
.. autoclass:: pyquantlib.KirkEngine
   :members:
   :undoc-members:
```

### StulzEngine

Stulz approximation for two-asset options.

```{eval-rst}
.. autoclass:: pyquantlib.StulzEngine
   :members:
   :undoc-members:
```

## Functions

### Black-76 (Lognormal)

| Function | Description |
|----------|-------------|
| `blackFormula(optionType, strike, forward, stdDev, ...)` | Option price |
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
| `bachelierBlackFormula(optionType, strike, forward, stdDev, ...)` | Option price |
| `bachelierBlackFormulaImpliedVol(optionType, strike, forward, tte, price, ...)` | Implied vol |
| `bachelierBlackFormulaStdDevDerivative(strike, forward, stdDev, ...)` | Vega component |

```python
import pyquantlib as ql

forward = 100.0
strike = 100.0
vol = 0.20
T = 1.0
stdDev = vol * (T ** 0.5)

price = ql.blackFormula(ql.OptionType.Call, strike, forward, stdDev)
impliedStdDev = ql.blackFormulaImpliedStdDev(ql.OptionType.Call, strike, forward, price)
```

```{note}
The abstract `PricingEngine` base class is available in `pyquantlib.base` for custom engine implementations.
```
