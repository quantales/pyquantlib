# Pricing Engines Module

## Vanilla Engines

### AnalyticEuropeanEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticEuropeanEngine
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

### IntegralEngine

```{eval-rst}
.. autoclass:: pyquantlib.IntegralEngine
```

### AnalyticHestonEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticHestonEngine
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

### AnalyticBlackVasicekEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticBlackVasicekEngine
```

European option pricing with stochastic Vasicek interest rates.

```python
vasicek = ql.Vasicek(r0=0.05, a=0.3, b=0.05, sigma=0.01)
engine = ql.AnalyticBlackVasicekEngine(process, vasicek, correlation=0.5)
```

### BatesEngine

```{eval-rst}
.. autoclass:: pyquantlib.BatesEngine
```

```python
bates_process = ql.BatesProcess(
    risk_free, dividend, spot,
    0.04, 1.0, 0.04, 0.5, -0.7,  # Heston params
    0.1, -0.05, 0.1,              # Jump params
)
model = ql.BatesModel(bates_process)
engine = ql.BatesEngine(model)
```

### BaroneAdesiWhaleyApproximationEngine

```{eval-rst}
.. autoclass:: pyquantlib.BaroneAdesiWhaleyApproximationEngine
```

### BjerksundStenslandApproximationEngine

```{eval-rst}
.. autoclass:: pyquantlib.BjerksundStenslandApproximationEngine
```

### BinomialVanillaEngine

```{eval-rst}
.. autoclass:: pyquantlib.BinomialVanillaEngine
```

```python
engine = ql.BinomialVanillaEngine(process, "crr", 801)
```

Tree types: `jr`, `crr`, `eqp`, `trigeorgis`, `tian`, `lr`, `joshi`

### FdBlackScholesVanillaEngine

```{eval-rst}
.. autoclass:: pyquantlib.FdBlackScholesVanillaEngine
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

```{eval-rst}
.. autoclass:: pyquantlib.MCEuropeanEngine
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

```{eval-rst}
.. autoclass:: pyquantlib.MCAmericanEngine
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

### QdFpAmericanEngine

```{eval-rst}
.. autoclass:: pyquantlib.QdFpAmericanEngine
```

High-performance American option engine based on QD+ fixed-point iteration.

```python
engine = ql.QdFpAmericanEngine(process)
```

```{warning}
`QdFpAmericanEngine.calculate()` may crash on Windows. Use alternative American engines if needed.
```

## Basket Engines

### MCEuropeanBasketEngine

```{eval-rst}
.. autoclass:: pyquantlib.MCEuropeanBasketEngine
```

### Fd2dBlackScholesVanillaEngine

```{eval-rst}
.. autoclass:: pyquantlib.Fd2dBlackScholesVanillaEngine
```

### KirkEngine

```{eval-rst}
.. autoclass:: pyquantlib.KirkEngine
```

### StulzEngine

```{eval-rst}
.. autoclass:: pyquantlib.StulzEngine
```

## Swaption Engines

### TreeSwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.TreeSwaptionEngine
```

Numerical lattice engine for swaptions using short-rate models.

```python
model = ql.HullWhite(curve, a=0.1, sigma=0.01)
engine = ql.TreeSwaptionEngine(model, timeSteps=100)
swaption.setPricingEngine(engine)
```

### JamshidianSwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.JamshidianSwaptionEngine
```

Analytic swaption engine using Jamshidian's bond option decomposition.

```python
model = ql.HullWhite(curve, a=0.1, sigma=0.01)
engine = ql.JamshidianSwaptionEngine(model)
swaption.setPricingEngine(engine)
```

### G2SwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.G2SwaptionEngine
```

Swaption engine for the G2++ two-factor model.

```python
model = ql.G2(curve, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
engine = ql.G2SwaptionEngine(model, range=6.0, intervals=200)
swaption.setPricingEngine(engine)
```

### FdHullWhiteSwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.FdHullWhiteSwaptionEngine
```

Finite-differences swaption engine for the Hull-White model.

```python
model = ql.HullWhite(curve, a=0.1, sigma=0.01)
engine = ql.FdHullWhiteSwaptionEngine(model, tGrid=100, xGrid=100)
swaption.setPricingEngine(engine)
```

### FdG2SwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.FdG2SwaptionEngine
```

Finite-differences swaption engine for the G2++ two-factor model.

```python
model = ql.G2(curve, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
engine = ql.FdG2SwaptionEngine(model, tGrid=100, xGrid=50, yGrid=50)
swaption.setPricingEngine(engine)
```

## Bond Engines

### DiscountingBondEngine

```{eval-rst}
.. autoclass:: pyquantlib.DiscountingBondEngine
```

```python
engine = ql.DiscountingBondEngine(curve_handle)
bond.setPricingEngine(engine)
print(bond.cleanPrice())
```

## Swap Engines

### DiscountingSwapEngine

```{eval-rst}
.. autoclass:: pyquantlib.DiscountingSwapEngine
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
