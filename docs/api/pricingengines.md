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

### COSHestonEngine

```{eval-rst}
.. autoclass:: pyquantlib.COSHestonEngine
```

Fourier-cosine series expansion for fast Heston pricing.

```python
engine = ql.COSHestonEngine(heston_model, L=16, N=200)
```

### ExponentialFittingHestonEngine

```{eval-rst}
.. autoclass:: pyquantlib.ExponentialFittingHestonEngine
```

Exponentially-fitted Gauss-Laguerre quadrature for Heston pricing.

### AnalyticPTDHestonEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticPTDHestonEngine
```

Analytic engine for piecewise time-dependent Heston models.

### AnalyticPDFHestonEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticPDFHestonEngine
```

PDF-based Heston engine for arbitrary European payoffs.

### HestonExpansionEngine

```{eval-rst}
.. autoclass:: pyquantlib.HestonExpansionEngine
```

Heston engine based on analytic expansions (LPP2, LPP3, Forde).

```python
engine = ql.HestonExpansionEngine(model, ql.HestonExpansionFormula.LPP3)
```

### AnalyticHestonHullWhiteEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticHestonHullWhiteEngine
```

Heston model with Hull-White stochastic interest rates.

```python
engine = ql.AnalyticHestonHullWhiteEngine(heston_model, hull_white_model)
```

### AnalyticH1HWEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticH1HWEngine
```

H1-HW approximation including equity-rate correlation.

```python
engine = ql.AnalyticH1HWEngine(heston_model, hull_white_model, rhoSr=0.3)
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

### FdHestonVanillaEngine

```{eval-rst}
.. autoclass:: pyquantlib.FdHestonVanillaEngine
```

Finite-differences Heston vanilla option engine. Supports European and American exercise.

```python
engine = ql.FdHestonVanillaEngine(heston_model, tGrid=100, xGrid=100, vGrid=50)
option.setPricingEngine(engine)

# Multiple-strike caching for efficiency
engine.enableMultipleStrikesCaching([90.0, 100.0, 110.0])
```

The `MakeFdHestonVanillaEngine` builder provides a keyword-argument interface:

```python
engine = ql.MakeFdHestonVanillaEngine(heston_model, tGrid=100, xGrid=100, vGrid=50)
```

### FdBatesVanillaEngine

```{eval-rst}
.. autoclass:: pyquantlib.FdBatesVanillaEngine
```

Partial integro finite-differences engine for the Bates model (Heston + jumps).

```python
engine = ql.FdBatesVanillaEngine(bates_model, tGrid=100, xGrid=100, vGrid=50)
```

### FdSabrVanillaEngine

```{eval-rst}
.. autoclass:: pyquantlib.FdSabrVanillaEngine
```

Finite-differences SABR vanilla option engine. Takes model parameters directly.

```python
engine = ql.FdSabrVanillaEngine(f0, alpha, beta, nu, rho, discount_curve)
```

### FdCEVVanillaEngine

```{eval-rst}
.. autoclass:: pyquantlib.FdCEVVanillaEngine
```

Finite-differences CEV (constant elasticity of variance) vanilla option engine.

```python
engine = ql.FdCEVVanillaEngine(f0, alpha, beta, discount_curve)
```

### FdBlackScholesShoutEngine

```{eval-rst}
.. autoclass:: pyquantlib.FdBlackScholesShoutEngine
```

Finite-differences engine for shout options (holder can lock in current intrinsic value).

```python
engine = ql.FdBlackScholesShoutEngine(process, tGrid=100, xGrid=100)
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

### JuQuadraticApproximationEngine

```{eval-rst}
.. autoclass:: pyquantlib.JuQuadraticApproximationEngine
```

### QdPlusAmericanEngine

```{eval-rst}
.. autoclass:: pyquantlib.QdPlusAmericanEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.QdPlusAmericanEngineSolverType
   :members:
   :undoc-members:
```

### AnalyticDigitalAmericanEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticDigitalAmericanEngine
```

### AnalyticDigitalAmericanKOEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticDigitalAmericanKOEngine
```

### MCDigitalEngine

```{eval-rst}
.. autofunction:: pyquantlib.MCDigitalEngine
```

### AnalyticDividendEuropeanEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticDividendEuropeanEngine
```

### AnalyticBSMHullWhiteEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticBSMHullWhiteEngine
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

### BlackSwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.BlackSwaptionEngine
```

Black-formula (lognormal volatility) swaption engine.

```python
engine = ql.BlackSwaptionEngine(curve, 0.20)
swaption.setPricingEngine(engine)
print(swaption.NPV())
```

### BachelierSwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.BachelierSwaptionEngine
```

Bachelier (normal volatility) swaption engine.

```python
engine = ql.BachelierSwaptionEngine(curve, 0.005)
swaption.setPricingEngine(engine)
print(swaption.NPV())
```

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

### Gaussian1dSwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.Gaussian1dSwaptionEngine
```

Gaussian 1-D model swaption engine with numerical integration. Supports European and Bermudan exercise.

```python
model = ql.Gsr(curve, [ql.Date(15, 1, 2025)], [0.01], 0.01)
engine = ql.Gaussian1dSwaptionEngine(model, integrationPoints=64)
swaption.setPricingEngine(engine)
print(swaption.NPV())
```

### Gaussian1dJamshidianSwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.Gaussian1dJamshidianSwaptionEngine
```

Jamshidian decomposition swaption engine for Gaussian 1-D models. European exercise only.

```python
engine = ql.Gaussian1dJamshidianSwaptionEngine(model)
swaption.setPricingEngine(engine)
```

### Gaussian1dNonstandardSwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.Gaussian1dNonstandardSwaptionEngine
```

Gaussian 1-D model engine for nonstandard swaptions (period-varying notionals and strikes).

### Gaussian1dFloatFloatSwaptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.Gaussian1dFloatFloatSwaptionEngine
```

Gaussian 1-D model engine for float-float swaptions.

## Barrier Engines

### AnalyticBarrierEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticBarrierEngine
```

Analytic pricing using Haug's formulas.

```python
engine = ql.AnalyticBarrierEngine(process)
```

### AnalyticDoubleBarrierEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticDoubleBarrierEngine
```

Analytic double barrier engine using Ikeda-Kunitomo series.

```python
engine = ql.AnalyticDoubleBarrierEngine(process, series=5)
```

### FdBlackScholesBarrierEngine

```{eval-rst}
.. autoclass:: pyquantlib.FdBlackScholesBarrierEngine
```

Finite-differences barrier option engine.

```python
engine = ql.FdBlackScholesBarrierEngine(process, tGrid=100, xGrid=100)
```

## Asian Engines

### AnalyticContinuousGeometricAveragePriceAsianEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticContinuousGeometricAveragePriceAsianEngine
```

### AnalyticDiscreteGeometricAveragePriceAsianEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticDiscreteGeometricAveragePriceAsianEngine
```

### TurnbullWakemanAsianEngine

```{eval-rst}
.. autoclass:: pyquantlib.TurnbullWakemanAsianEngine
```

Moment-matching approximation for discrete arithmetic average price Asian options.

```python
engine = ql.TurnbullWakemanAsianEngine(process)
```

### MCDiscreteArithmeticAPEngine

```{eval-rst}
.. autoclass:: pyquantlib.MCDiscreteArithmeticAPEngine
```

Monte Carlo engine for discrete arithmetic average price Asian options.

```python
engine = ql.MCDiscreteArithmeticAPEngine(
    process, requiredSamples=100000, seed=42, controlVariate=True,
)
```

## Lookback Engines

### AnalyticContinuousFloatingLookbackEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticContinuousFloatingLookbackEngine
```

### AnalyticContinuousFixedLookbackEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticContinuousFixedLookbackEngine
```

### AnalyticContinuousPartialFloatingLookbackEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticContinuousPartialFloatingLookbackEngine
```

### AnalyticContinuousPartialFixedLookbackEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticContinuousPartialFixedLookbackEngine
```

```python
payoff = ql.FloatingTypePayoff(ql.Call)
exercise = ql.EuropeanExercise(expiry)
option = ql.ContinuousFloatingLookbackOption(100.0, payoff, exercise)
option.setPricingEngine(ql.AnalyticContinuousFloatingLookbackEngine(process))
print(option.NPV())
```

## Cliquet Engines

### AnalyticCliquetEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticCliquetEngine
```

```python
engine = ql.AnalyticCliquetEngine(process)
cliquet.setPricingEngine(engine)
print(cliquet.NPV())
```

## Exotic Engines

### AnalyticCompoundOptionEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticCompoundOptionEngine
```

### AnalyticSimpleChooserEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticSimpleChooserEngine
```

### AnalyticComplexChooserEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticComplexChooserEngine
```

### AnalyticEuropeanMargrabeEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticEuropeanMargrabeEngine
```

Takes two Black-Scholes-Merton processes and a correlation parameter.

```python
engine = ql.AnalyticEuropeanMargrabeEngine(process1, process2, 0.5)
option.setPricingEngine(engine)
```

### AnalyticAmericanMargrabeEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticAmericanMargrabeEngine
```

## Forward-Start Engines

### ForwardEuropeanEngine

```{eval-rst}
.. autoclass:: pyquantlib.ForwardEuropeanEngine
```

### ForwardPerformanceEuropeanEngine

```{eval-rst}
.. autoclass:: pyquantlib.ForwardPerformanceEuropeanEngine
```

```python
option = ql.ForwardVanillaOption(1.0, reset_date, payoff, exercise)
option.setPricingEngine(ql.ForwardEuropeanEngine(process))
print(option.NPV())
```

## Quanto Engines

### QuantoVanillaEngine

```{eval-rst}
.. autoclass:: pyquantlib.QuantoVanillaEngine
```

Quanto European option engine (currency-adjusted Black-Scholes). Accepts explicit Handle arguments or raw objects (hidden handles).

```python
engine = ql.QuantoVanillaEngine(
    process, foreign_rate, fx_vol, correlation,
)
option.setPricingEngine(engine)
print(option.NPV(), option.qvega(), option.qrho(), option.qlambda())
```

## Cap/Floor Engines

### BlackCapFloorEngine

```{eval-rst}
.. autoclass:: pyquantlib.BlackCapFloorEngine
```

Black-formula cap/floor engine (lognormal volatility).

```python
engine = ql.BlackCapFloorEngine(curve, 0.20)
cap.setPricingEngine(engine)
print(cap.NPV())
```

### BachelierCapFloorEngine

```{eval-rst}
.. autoclass:: pyquantlib.BachelierCapFloorEngine
```

Bachelier (normal volatility) cap/floor engine.

```python
engine = ql.BachelierCapFloorEngine(curve, 0.005)
cap.setPricingEngine(engine)
print(cap.NPV())
```

### AnalyticCapFloorEngine

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticCapFloorEngine
```

Analytic cap/floor engine for affine short-rate models (Hull-White, CIR, G2++).

### TreeCapFloorEngine

```{eval-rst}
.. autoclass:: pyquantlib.TreeCapFloorEngine
```

Lattice-based cap/floor engine for short-rate models.

### Gaussian1dCapFloorEngine

```{eval-rst}
.. autoclass:: pyquantlib.Gaussian1dCapFloorEngine
```

Gaussian 1-D model cap/floor engine with numerical integration.

```python
model = ql.Gsr(curve, [ql.Date(15, 1, 2025)], [0.01], 0.01)
engine = ql.Gaussian1dCapFloorEngine(model, integrationPoints=64)
cap.setPricingEngine(engine)
print(cap.NPV())
```

## YoY Inflation Cap/Floor Engines

### YoYInflationBlackCapFloorEngine

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationBlackCapFloorEngine
   :members:
   :undoc-members:
```

Black-formula engine for YoY inflation caps and floors (lognormal volatility).

```python
engine = ql.YoYInflationBlackCapFloorEngine(yoy_index, yoy_vol_handle, curve_handle)
cap.setPricingEngine(engine)
print(cap.NPV())
```

### YoYInflationUnitDisplacedBlackCapFloorEngine

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationUnitDisplacedBlackCapFloorEngine
   :members:
   :undoc-members:
```

Unit-displaced Black-formula engine for YoY inflation caps and floors.

### YoYInflationBachelierCapFloorEngine

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationBachelierCapFloorEngine
   :members:
   :undoc-members:
```

Bachelier (normal volatility) engine for YoY inflation caps and floors.

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

## Convertible Bond Engines

### BinomialConvertibleEngine

```{eval-rst}
.. autoclass:: pyquantlib.BinomialConvertibleEngine
```

Tsiveriotis-Fernandes binomial lattice engine for convertible bonds.

```python
engine = ql.BinomialConvertibleEngine(process, "crr", 801)
bond.setPricingEngine(engine)
print(bond.NPV())
```

Tree types: `jr`, `crr`, `eqp`, `trigeorgis`, `tian`, `lr`, `joshi`

Also accepts an optional `creditSpread` parameter:

```python
engine = ql.BinomialConvertibleEngine(process, "crr", 801, creditSpread=spread)
```

## Credit Engines

### MidPointCdsEngine

```{eval-rst}
.. autoclass:: pyquantlib.MidPointCdsEngine
```

Mid-point CDS pricing engine.

```python
engine = ql.MidPointCdsEngine(default_curve, 0.4, discount_curve)
cds.setPricingEngine(engine)
print(cds.NPV())
```

### IsdaCdsEngine

```{eval-rst}
.. autoclass:: pyquantlib.IsdaCdsEngine
```

ISDA-standard CDS pricing engine.

```python
engine = ql.IsdaCdsEngine(default_curve, 0.4, discount_curve)
cds.setPricingEngine(engine)
print(cds.NPV())
```

| Enum | Values |
|------|--------|
| `IsdaNumericalFix` | `IsdaNone`, `Taylor` |
| `IsdaAccrualBias` | `HalfDayBias`, `NoBias` |
| `IsdaForwardsInCouponPeriod` | `Flat`, `Piecewise` |

## Swap Engines

### DiscountingSwapEngine

```{eval-rst}
.. autoclass:: pyquantlib.DiscountingSwapEngine
```

## Bond Functions

### BondFunctions

```{eval-rst}
.. autoclass:: pyquantlib.BondFunctions
```

Static functions for bond analytics.

| Function | Description |
|----------|-------------|
| `cleanPrice(bond, rate)` | Clean price from yield |
| `dirtyPrice(bond, rate)` | Dirty price from yield |
| `bps(bond, rate)` | Basis point sensitivity |
| `bondYield(bond, cleanPrice, dc, comp, freq)` | Yield from clean price |
| `duration(bond, rate, type)` | Duration (Modified, Macaulay, or Simple) |
| `convexity(bond, rate)` | Convexity |
| `basisPointValue(bond, rate)` | Basis point value |
| `yieldValueBasisPoint(bond, rate)` | Yield value of a basis point |
| `zSpread(bond, cleanPrice, curve, dc, comp, freq)` | Z-spread |

```python
rate = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
print(ql.BondFunctions.cleanPrice(bond, rate))
print(ql.BondFunctions.duration(bond, rate, ql.DurationType.Modified))
print(ql.BondFunctions.convexity(bond, rate))
```

## Variance Swap Engines

### ReplicatingVarianceSwapEngine

```{eval-rst}
.. autoclass:: pyquantlib.ReplicatingVarianceSwapEngine
```

## Calculators

### BlackCalculator

```{eval-rst}
.. autoclass:: pyquantlib.BlackCalculator
```

Black 1976 pricing and Greeks calculator. Provides delta, gamma, theta, vega, rho, and more.

```python
calc = ql.BlackCalculator(payoff, forward, stdDev, discount)
print(calc.value(), calc.delta(spot), calc.gamma(spot), calc.vega(T))
```

### BachelierCalculator

```{eval-rst}
.. autoclass:: pyquantlib.BachelierCalculator
```

Bachelier (normal-volatility) pricing and Greeks calculator. Same API as `BlackCalculator`.

```python
calc = ql.BachelierCalculator(payoff, forward, stdDev, discount)
print(calc.value(), calc.delta(spot), calc.gamma(spot), calc.vega(T))
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
