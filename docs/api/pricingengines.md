# Pricing engines

Bindings for the engine layer that turns instruments into prices. Every engine implements the same `PricingEngine` interface and is attached to an instrument with `setPricingEngine()`. PyQuantLib exposes around 120 concrete engines covering analytic formulas, finite-difference grids, Monte Carlo simulation, binomial trees, and lattice methods, organised by the instrument family they price.

See {doc}`/concepts/pricing-engines` for the instrument / engine separation, {doc}`/cookbook/compare-engines` for the same-instrument-three-engines pattern, and {doc}`/cookbook/mc-engine-kwargs` for MC engine kwargs in practice.

## At a glance

### European vanilla options

| Group | Engines |
|---|---|
| Black-Scholes analytic | {py:class}`pyquantlib.AnalyticEuropeanEngine`, {py:class}`pyquantlib.IntegralEngine`, {py:class}`pyquantlib.AnalyticDividendEuropeanEngine`, {py:class}`pyquantlib.CashDividendEuropeanEngine` |
| Heston / Bates analytic | {py:class}`pyquantlib.AnalyticHestonEngine`, {py:class}`pyquantlib.AnalyticPTDHestonEngine`, {py:class}`pyquantlib.AnalyticPDFHestonEngine`, {py:class}`pyquantlib.HestonExpansionEngine`, {py:class}`pyquantlib.COSHestonEngine`, {py:class}`pyquantlib.ExponentialFittingHestonEngine`, {py:class}`pyquantlib.BatesEngine` |
| Stochastic-rate / hybrid | {py:class}`pyquantlib.AnalyticBSMHullWhiteEngine`, {py:class}`pyquantlib.AnalyticHestonHullWhiteEngine`, {py:class}`pyquantlib.AnalyticH1HWEngine`, {py:class}`pyquantlib.AnalyticBlackVasicekEngine` |
| CEV / SABR | {py:class}`pyquantlib.AnalyticCEVEngine`, {py:class}`pyquantlib.CEVCalculator`, {py:class}`pyquantlib.FdSabrVanillaEngine`, {py:class}`pyquantlib.FdCEVVanillaEngine` |
| Finite difference | {py:class}`pyquantlib.FdBlackScholesVanillaEngine`, {py:class}`pyquantlib.FdHestonVanillaEngine`, {py:class}`pyquantlib.FdBatesVanillaEngine`, {py:class}`pyquantlib.FdHestonHullWhiteVanillaEngine`, {py:class}`pyquantlib.FdOrnsteinUhlenbeckVanillaEngine`, {py:class}`pyquantlib.FdBlackScholesShoutEngine`, {py:class}`pyquantlib.FdSimpleBSSwingEngine` |
| Monte Carlo | {py:class}`pyquantlib.MCEuropeanEngine`, {py:class}`pyquantlib.MCEuropeanHestonEngine`, {py:class}`pyquantlib.MCEuropeanGJRGARCHEngine` |
| Tree | {py:class}`pyquantlib.BinomialVanillaEngine` |
| Digitals | {py:class}`pyquantlib.AnalyticDigitalAmericanEngine`, {py:class}`pyquantlib.AnalyticDigitalAmericanKOEngine`, {py:class}`pyquantlib.MCDigitalEngine` |

### American vanilla options

| Group | Engines |
|---|---|
| Analytic approximations | {py:class}`pyquantlib.BaroneAdesiWhaleyApproximationEngine`, {py:class}`pyquantlib.BjerksundStenslandApproximationEngine`, {py:class}`pyquantlib.JuQuadraticApproximationEngine`, {py:class}`pyquantlib.QdFpAmericanEngine`, {py:class}`pyquantlib.QdPlusAmericanEngine` |
| Finite difference | {py:class}`pyquantlib.FdBlackScholesVanillaEngine` (with `AmericanExercise`), {py:class}`pyquantlib.FdHestonVanillaEngine` |
| Tree | {py:class}`pyquantlib.BinomialVanillaEngine` |
| Monte Carlo | {py:class}`pyquantlib.MCAmericanEngine` |

### Basket / spread / multi-asset

| Group | Engines |
|---|---|
| Spread (analytic) | {py:class}`pyquantlib.KirkEngine`, {py:class}`pyquantlib.StulzEngine`, {py:class}`pyquantlib.PearsonSpreadEngine`, {py:class}`pyquantlib.GaussianCopulaSpreadEngine` |
| Basket (analytic) | {py:class}`pyquantlib.ChoiBasketEngine`, {py:class}`pyquantlib.SingleFactorBsmBasketEngine` |
| Basket (FD / MC) | {py:class}`pyquantlib.Fd2dBlackScholesVanillaEngine`, {py:class}`pyquantlib.FdndimBlackScholesVanillaEngine`, {py:class}`pyquantlib.MCEuropeanBasketEngine`, {py:class}`pyquantlib.MCAmericanBasketEngine`, {py:class}`pyquantlib.MCLDEuropeanBasketEngine` |

### Swaptions

| Group | Engines |
|---|---|
| Black / Bachelier | {py:class}`pyquantlib.BlackSwaptionEngine`, {py:class}`pyquantlib.BachelierSwaptionEngine` |
| Tree / lattice | {py:class}`pyquantlib.TreeSwaptionEngine` |
| Analytic short-rate | {py:class}`pyquantlib.JamshidianSwaptionEngine`, {py:class}`pyquantlib.G2SwaptionEngine` |
| Finite difference | {py:class}`pyquantlib.FdHullWhiteSwaptionEngine`, {py:class}`pyquantlib.FdG2SwaptionEngine` |
| Gaussian 1-D | {py:class}`pyquantlib.Gaussian1dSwaptionEngine`, {py:class}`pyquantlib.Gaussian1dJamshidianSwaptionEngine`, {py:class}`pyquantlib.Gaussian1dNonstandardSwaptionEngine`, {py:class}`pyquantlib.Gaussian1dFloatFloatSwaptionEngine` |

### Barrier options

| Group | Engines |
|---|---|
| Black-Scholes analytic | {py:class}`pyquantlib.AnalyticBarrierEngine`, {py:class}`pyquantlib.AnalyticDoubleBarrierEngine`, {py:class}`pyquantlib.AnalyticBinaryBarrierEngine`, {py:class}`pyquantlib.AnalyticDoubleBarrierBinaryEngine`, {py:class}`pyquantlib.AnalyticPartialTimeBarrierOptionEngine`, {py:class}`pyquantlib.AnalyticSoftBarrierEngine`, {py:class}`pyquantlib.AnalyticTwoAssetBarrierEngine` |
| FD / tree / MC | {py:class}`pyquantlib.FdBlackScholesBarrierEngine`, {py:class}`pyquantlib.FdBlackScholesRebateEngine`, {py:class}`pyquantlib.BinomialBarrierEngine`, {py:class}`pyquantlib.MCBarrierEngine`, {py:class}`pyquantlib.MCDoubleBarrierEngine` |
| Heston | {py:class}`pyquantlib.FdHestonBarrierEngine`, {py:class}`pyquantlib.FdHestonDoubleBarrierEngine`, {py:class}`pyquantlib.FdHestonRebateEngine` |

### Asian options

| Group | Engines |
|---|---|
| Geometric (analytic) | {py:class}`pyquantlib.AnalyticContinuousGeometricAveragePriceAsianEngine`, {py:class}`pyquantlib.AnalyticDiscreteGeometricAveragePriceAsianEngine`, {py:class}`pyquantlib.AnalyticDiscreteGeometricAverageStrikeAsianEngine` |
| Arithmetic (approx) | {py:class}`pyquantlib.TurnbullWakemanAsianEngine`, {py:class}`pyquantlib.ContinuousArithmeticAsianLevyEngine`, {py:class}`pyquantlib.ChoiAsianEngine` |
| FD / MC | {py:class}`pyquantlib.FdBlackScholesAsianEngine`, {py:class}`pyquantlib.MCDiscreteArithmeticAPEngine`, {py:class}`pyquantlib.MCDiscreteArithmeticASEngine`, {py:class}`pyquantlib.MCDiscreteGeometricAPEngine`, {py:class}`pyquantlib.MCDiscreteArithmeticAPHestonEngine`, {py:class}`pyquantlib.MCDiscreteGeometricAPHestonEngine` |

### Other options

| Group | Engines |
|---|---|
| Lookback | {py:class}`pyquantlib.AnalyticContinuousFloatingLookbackEngine`, {py:class}`pyquantlib.AnalyticContinuousFixedLookbackEngine`, {py:class}`pyquantlib.AnalyticContinuousPartialFloatingLookbackEngine`, {py:class}`pyquantlib.AnalyticContinuousPartialFixedLookbackEngine` |
| Cliquet | {py:class}`pyquantlib.AnalyticCliquetEngine` |
| Compound / chooser | {py:class}`pyquantlib.AnalyticCompoundOptionEngine`, {py:class}`pyquantlib.AnalyticSimpleChooserEngine`, {py:class}`pyquantlib.AnalyticComplexChooserEngine` |
| Margrabe | {py:class}`pyquantlib.AnalyticEuropeanMargrabeEngine`, {py:class}`pyquantlib.AnalyticAmericanMargrabeEngine` |
| Forward-start | {py:class}`pyquantlib.ForwardEuropeanEngine`, {py:class}`pyquantlib.ForwardPerformanceEuropeanEngine` |
| Quanto | {py:class}`pyquantlib.QuantoVanillaEngine` |

### Caps, floors, and bond / credit / swap engines

| Group | Engines |
|---|---|
| Caps / floors | {py:class}`pyquantlib.BlackCapFloorEngine`, {py:class}`pyquantlib.BachelierCapFloorEngine`, {py:class}`pyquantlib.AnalyticCapFloorEngine`, {py:class}`pyquantlib.TreeCapFloorEngine`, {py:class}`pyquantlib.Gaussian1dCapFloorEngine` |
| YoY inflation | {py:class}`pyquantlib.YoYInflationBlackCapFloorEngine`, {py:class}`pyquantlib.YoYInflationUnitDisplacedBlackCapFloorEngine`, {py:class}`pyquantlib.YoYInflationBachelierCapFloorEngine` |
| Bonds / convertibles | {py:class}`pyquantlib.DiscountingBondEngine`, {py:class}`pyquantlib.BinomialConvertibleEngine` |
| Credit | {py:class}`pyquantlib.MidPointCdsEngine`, {py:class}`pyquantlib.IsdaCdsEngine` |
| Swaps | {py:class}`pyquantlib.DiscountingSwapEngine`, {py:class}`pyquantlib.DiscountingConstNotionalCrossCurrencySwapEngine` |
| FX forwards | {py:class}`pyquantlib.DiscountingFxForwardEngine` |
| Futures | {py:class}`pyquantlib.DiscountingPerpetualFuturesEngine` |
| Variance swaps | {py:class}`pyquantlib.ReplicatingVarianceSwapEngine` |

### Calculators and free functions

| Group | What |
|---|---|
| Calculators | {py:class}`pyquantlib.BlackCalculator`, {py:class}`pyquantlib.BachelierCalculator`, {py:class}`pyquantlib.BondFunctions` |
| Black-76 free functions | `blackFormula`, `blackFormulaImpliedStdDev`, `blackFormulaImpliedStdDevApproximation`, `blackFormulaStdDevDerivative`, `blackFormulaVolDerivative`, `blackFormulaForwardDerivative`, `blackFormulaCashItmProbability`, `blackFormulaAssetItmProbability` |
| Bachelier free functions | `bachelierBlackFormula`, `bachelierBlackFormulaImpliedVol`, `bachelierBlackFormulaStdDevDerivative` |

```{note}
The abstract `PricingEngine` base class is exposed under `pyquantlib.base` for custom engine subclassing. See {doc}`/extending` for an end-to-end example.
```

## Common patterns

### Attach an analytic engine to a vanilla option

```python
import pyquantlib as ql

engine = ql.AnalyticEuropeanEngine(process)
option.setPricingEngine(engine)

print(f"NPV:   {option.NPV():.4f}")
print(f"Delta: {option.delta():.4f}")
print(f"Gamma: {option.gamma():.4f}")
print(f"Vega:  {option.vega():.4f}")
```

### Run an MC pricing with kwargs

```python
engine = ql.MCEuropeanEngine(
    process,
    timeSteps=1,
    requiredSamples=100_000,
    seed=42,
)
option.setPricingEngine(engine)
print(option.NPV())
```

See {doc}`/cookbook/mc-engine-kwargs` and {doc}`/cookbook/mc-convergence`.

### Price an American put with FD

```python
fd = ql.FdBlackScholesVanillaEngine(process, tGrid=200, xGrid=200)
american.setPricingEngine(fd)
print(american.NPV())
```

The same engine prices European exercise; the `FdmAmericanStepCondition` is wired in automatically when the option's exercise is `AmericanExercise`. See {doc}`/cookbook/american-fd`.

### Build a Heston pricing pipeline

```python
heston_process = ql.HestonProcess(
    rf_handle, dq_handle, spot_handle,
    v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
)
heston_model = ql.HestonModel(heston_process)
engine       = ql.AnalyticHestonEngine(heston_model)
option.setPricingEngine(engine)
```

The Heston model + engine pair is the input to calibration. See {doc}`/cookbook/heston-calibration`.

### Discount-curve engines for fixed-income

```python
bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))
swap.setPricingEngine(ql.DiscountingSwapEngine(curve_handle))
cap.setPricingEngine(ql.BlackCapFloorEngine(curve_handle, vol))
cds.setPricingEngine(ql.MidPointCdsEngine(default_curve, 0.4, discount_curve))
```

## Vanilla engines

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticEuropeanEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.IntegralEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticHestonEngine
```

```{note}
`AnalyticHestonEngine` computes NPV only. Greeks under Heston require finite-difference engines.
```

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticBlackVasicekEngine
```

European option pricing with stochastic Vasicek interest rates.

```python
vasicek = ql.Vasicek(r0=0.05, a=0.3, b=0.05, sigma=0.01)
engine  = ql.AnalyticBlackVasicekEngine(process, vasicek, correlation=0.5)
```

```{eval-rst}
.. autoclass:: pyquantlib.BatesEngine
```

```python
bates_process = ql.BatesProcess(
    risk_free, dividend, spot,
    0.04, 1.0, 0.04, 0.5, -0.7,    # Heston params
    0.1, -0.05, 0.1,                # Jump params
)
model  = ql.BatesModel(bates_process)
engine = ql.BatesEngine(model)
```

```{eval-rst}
.. autoclass:: pyquantlib.COSHestonEngine
```

Fourier-cosine series expansion for fast Heston pricing.

```python
engine = ql.COSHestonEngine(heston_model, L=16, N=200)
```

```{eval-rst}
.. autoclass:: pyquantlib.ExponentialFittingHestonEngine
```

Exponentially-fitted Gauss-Laguerre quadrature for Heston.

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticPTDHestonEngine
```

Piecewise time-dependent Heston.

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticPDFHestonEngine
```

PDF-based Heston engine for arbitrary European payoffs.

```{eval-rst}
.. autoclass:: pyquantlib.HestonExpansionEngine
```

Heston engine based on analytic expansions (LPP2, LPP3, Forde).

```python
engine = ql.HestonExpansionEngine(model, ql.HestonExpansionFormula.LPP3)
```

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticHestonHullWhiteEngine
```

Heston model with Hull-White stochastic interest rates.

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticH1HWEngine
```

H1-HW approximation including equity-rate correlation.

```python
engine = ql.AnalyticH1HWEngine(heston_model, hull_white_model, rhoSr=0.3)
```

```{eval-rst}
.. autoclass:: pyquantlib.BaroneAdesiWhaleyApproximationEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.BjerksundStenslandApproximationEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.BinomialVanillaEngine
```

```python
engine = ql.BinomialVanillaEngine(process, "crr", 801)
```

Tree types: `jr`, `crr`, `eqp`, `trigeorgis`, `tian`, `lr`, `joshi`.

```{eval-rst}
.. autoclass:: pyquantlib.FdBlackScholesVanillaEngine
```

```python
engine = ql.FdBlackScholesVanillaEngine(
    process, tGrid=100, xGrid=100,
    schemeDesc=ql.FdmSchemeDesc.Douglas(),
)
```

```{eval-rst}
.. autoclass:: pyquantlib.FdHestonVanillaEngine
```

Supports European and American exercise. The `MakeFdHestonVanillaEngine` builder gives a keyword-argument interface; multiple-strike caching reuses the FD solve across nearby strikes.

```python
engine = ql.FdHestonVanillaEngine(heston_model, tGrid=100, xGrid=100, vGrid=50)
engine.enableMultipleStrikesCaching([90.0, 100.0, 110.0])

# Alternate builder
engine = ql.MakeFdHestonVanillaEngine(heston_model, tGrid=100, xGrid=100, vGrid=50)
```

```{eval-rst}
.. autoclass:: pyquantlib.FdBatesVanillaEngine
```

Partial-integro FD engine for the Bates model (Heston + jumps).

```{eval-rst}
.. autoclass:: pyquantlib.FdSabrVanillaEngine
```

```python
engine = ql.FdSabrVanillaEngine(f0, alpha, beta, nu, rho, discount_curve)
```

```{eval-rst}
.. autoclass:: pyquantlib.FdCEVVanillaEngine
```

```python
engine = ql.FdCEVVanillaEngine(f0, alpha, beta, discount_curve)
```

```{eval-rst}
.. autoclass:: pyquantlib.FdBlackScholesShoutEngine
```

FD engine for shout options (holder can lock in current intrinsic value).

```{eval-rst}
.. autoclass:: pyquantlib.FdSimpleBSSwingEngine
```

FD Black-Scholes engine for {py:class}`pyquantlib.VanillaSwingOption`.

```{eval-rst}
.. autoclass:: pyquantlib.FdHestonHullWhiteVanillaEngine
```

```python
engine = ql.FdHestonHullWhiteVanillaEngine(
    heston_model, hw_process, corrEquityShortRate=0.3,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.FdOrnsteinUhlenbeckVanillaEngine
```

```python
ou_process = ql.OrnsteinUhlenbeckProcess(speed=0.5, volatility=0.01)
engine     = ql.FdOrnsteinUhlenbeckVanillaEngine(ou_process, discount_curve)
```

```{eval-rst}
.. autoclass:: pyquantlib.MCEuropeanEngine
```

```python
engine = ql.MCEuropeanEngine(
    process, timeSteps=100, requiredSamples=100_000, seed=42,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.MCAmericanEngine
```

```python
engine = ql.MCAmericanEngine(
    process,
    timeSteps=100, antitheticVariate=True,
    calibrationSamples=4096, requiredTolerance=0.02,
    seed=42,
)
```

```{eval-rst}
.. autofunction:: pyquantlib.MCEuropeanHestonEngine
```

```{eval-rst}
.. autofunction:: pyquantlib.MCEuropeanGJRGARCHEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticCEVEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.CEVCalculator
```

Standalone CEV option value calculator.

```python
calc = ql.CEVCalculator(f0, alpha, beta)
print(calc.value(ql.Call, 100.0, 1.0))
```

```{eval-rst}
.. autoclass:: pyquantlib.QdFpAmericanEngine
```

```{warning}
`QdFpAmericanEngine.calculate()` may crash on Windows. Use an alternative American engine if needed.
```

```{eval-rst}
.. autoclass:: pyquantlib.JuQuadraticApproximationEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.QdPlusAmericanEngine

.. autoclass:: pyquantlib.QdPlusAmericanEngineSolverType
   :members:
   :undoc-members:
```

### Digitals

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticDigitalAmericanEngine
.. autoclass:: pyquantlib.AnalyticDigitalAmericanKOEngine
.. autofunction:: pyquantlib.MCDigitalEngine
```

### Dividend engines

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticDividendEuropeanEngine
.. autoclass:: pyquantlib.CashDividendEuropeanEngine

.. autoclass:: pyquantlib.CashDividendModel
   :members:
   :undoc-members:
```

Semi-analytic European engine with cash dividends (Healy 2021). Supports `Spot` and `Escrowed` dividend models.

```python
dividends = [ql.FixedDividend(2.0, ex_date)]
engine    = ql.CashDividendEuropeanEngine(process, dividends, ql.CashDividendModel.Spot)
```

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticBSMHullWhiteEngine
```

## Basket engines

```{eval-rst}
.. autoclass:: pyquantlib.MCEuropeanBasketEngine
.. autoclass:: pyquantlib.Fd2dBlackScholesVanillaEngine
.. autoclass:: pyquantlib.KirkEngine
.. autoclass:: pyquantlib.StulzEngine
.. autoclass:: pyquantlib.ChoiBasketEngine
```

Choi (2018) analytic engine for average and spread basket options.

```{eval-rst}
.. autoclass:: pyquantlib.SingleFactorBsmBasketEngine
```

Single-factor BSM approximation for average basket options.

```{eval-rst}
.. autofunction:: pyquantlib.MCAmericanBasketEngine
```

Monte Carlo American basket engine using Longstaff-Schwartz regression.

```{eval-rst}
.. autoclass:: pyquantlib.FdndimBlackScholesVanillaEngine
```

N-dimensional finite-difference Black-Scholes basket engine.

```{eval-rst}
.. autoclass:: pyquantlib.MCLDEuropeanBasketEngine
```

### Spread options

```{eval-rst}
.. autoclass:: pyquantlib.PearsonSpreadEngine
```

Pearson (1995) engine, evaluating the spread option through a single numerical integration.
`integrationTolerance`, `maxIntegrationIterations`, and `nStd` control the quadrature and its
truncation range. Like {py:class}`pyquantlib.KirkEngine` it derives from
{py:class}`pyquantlib.base.SpreadBlackScholesVanillaEngine`, so it takes two processes and
their correlation.

```{eval-rst}
.. autoclass:: pyquantlib.GaussianCopulaSpreadEngine
```

Prices the spread through nested Gauss-Hermite quadrature over a Gaussian copula, taking the
marginals from each process including any smile. `nPoints` sets the quadrature points per
dimension.

```python
# Two forward processes and their correlation
p1 = ql.BlackProcess(ql.QuoteHandle(ql.SimpleQuote(100.0)), rate, vol1)
p2 = ql.BlackProcess(ql.QuoteHandle(ql.SimpleQuote(96.0)), rate, vol2)

payoff = ql.SpreadBasketPayoff(ql.PlainVanillaPayoff(ql.OptionType.Call, 3.0))
option = ql.BasketOption(payoff, ql.EuropeanExercise(maturity))

option.setPricingEngine(ql.GaussianCopulaSpreadEngine(p1, p2, 0.5))
print(option.NPV())
```

## Swaption engines

```{eval-rst}
.. autoclass:: pyquantlib.BlackSwaptionEngine
```

```python
engine = ql.BlackSwaptionEngine(curve, 0.20)
```

```{eval-rst}
.. autoclass:: pyquantlib.BachelierSwaptionEngine
```

```python
engine = ql.BachelierSwaptionEngine(curve, 0.005)
```

```{eval-rst}
.. autoclass:: pyquantlib.TreeSwaptionEngine
```

```python
model  = ql.HullWhite(curve, a=0.1, sigma=0.01)
engine = ql.TreeSwaptionEngine(model, timeSteps=100)
```

```{eval-rst}
.. autoclass:: pyquantlib.JamshidianSwaptionEngine
```

Analytic engine using Jamshidian's bond-option decomposition.

```python
model  = ql.HullWhite(curve, a=0.1, sigma=0.01)
engine = ql.JamshidianSwaptionEngine(model)
```

```{eval-rst}
.. autoclass:: pyquantlib.G2SwaptionEngine
```

```python
model  = ql.G2(curve, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
engine = ql.G2SwaptionEngine(model, range=6.0, intervals=200)
```

```{eval-rst}
.. autoclass:: pyquantlib.FdHullWhiteSwaptionEngine
```

```python
engine = ql.FdHullWhiteSwaptionEngine(model, tGrid=100, xGrid=100)
```

```{eval-rst}
.. autoclass:: pyquantlib.FdG2SwaptionEngine
```

```python
engine = ql.FdG2SwaptionEngine(model, tGrid=100, xGrid=50, yGrid=50)
```

```{eval-rst}
.. autoclass:: pyquantlib.Gaussian1dSwaptionEngine
```

Numerical-integration engine. Supports European and Bermudan exercise.

```python
model  = ql.Gsr(curve, [ql.Date(15, 1, 2025)], [0.01], 0.01)
engine = ql.Gaussian1dSwaptionEngine(model, integrationPoints=64)
```

```{eval-rst}
.. autoclass:: pyquantlib.Gaussian1dJamshidianSwaptionEngine
```

Jamshidian decomposition for Gaussian 1-D models. European exercise only.

```{eval-rst}
.. autoclass:: pyquantlib.Gaussian1dNonstandardSwaptionEngine
```

Period-varying notionals and strikes.

```{eval-rst}
.. autoclass:: pyquantlib.Gaussian1dFloatFloatSwaptionEngine
```

## Barrier engines

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticBarrierEngine
```

Analytic Black-Scholes pricing using Haug's formulas.

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticDoubleBarrierEngine
```

Ikeda-Kunitomo series.

```python
engine = ql.AnalyticDoubleBarrierEngine(process, series=5)
```

```{eval-rst}
.. autoclass:: pyquantlib.FdBlackScholesBarrierEngine
.. autoclass:: pyquantlib.FdBlackScholesRebateEngine
.. autoclass:: pyquantlib.AnalyticDoubleBarrierBinaryEngine
```

Hui's analytic double-barrier binary (one-touch).

```{eval-rst}
.. autofunction:: pyquantlib.MCBarrierEngine
.. autofunction:: pyquantlib.MCDoubleBarrierEngine
.. autoclass:: pyquantlib.AnalyticBinaryBarrierEngine
.. autofunction:: pyquantlib.BinomialBarrierEngine
```

```python
engine = ql.BinomialBarrierEngine(process, "crr", 200)
engine = ql.BinomialBarrierEngine(process, "crr", 200, discretization="dermankani")
```

```{eval-rst}
.. autoclass:: pyquantlib.FdHestonBarrierEngine
.. autoclass:: pyquantlib.FdHestonDoubleBarrierEngine
.. autoclass:: pyquantlib.FdHestonRebateEngine
.. autoclass:: pyquantlib.AnalyticPartialTimeBarrierOptionEngine
.. autoclass:: pyquantlib.AnalyticSoftBarrierEngine
.. autoclass:: pyquantlib.AnalyticTwoAssetBarrierEngine
```

## Asian engines

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticContinuousGeometricAveragePriceAsianEngine
.. autoclass:: pyquantlib.AnalyticDiscreteGeometricAveragePriceAsianEngine
.. autoclass:: pyquantlib.TurnbullWakemanAsianEngine
```

Moment-matching approximation for discrete arithmetic average price Asians.

```{eval-rst}
.. autoclass:: pyquantlib.MCDiscreteArithmeticAPEngine
```

```python
engine = ql.MCDiscreteArithmeticAPEngine(
    process, requiredSamples=100_000, seed=42, controlVariate=True,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.ChoiAsianEngine
.. autoclass:: pyquantlib.AnalyticDiscreteGeometricAverageStrikeAsianEngine
.. autoclass:: pyquantlib.ContinuousArithmeticAsianLevyEngine
.. autoclass:: pyquantlib.FdBlackScholesAsianEngine
.. autofunction:: pyquantlib.MCDiscreteArithmeticASEngine
.. autofunction:: pyquantlib.MCDiscreteGeometricAPEngine
.. autofunction:: pyquantlib.MCDiscreteArithmeticAPHestonEngine
.. autofunction:: pyquantlib.MCDiscreteGeometricAPHestonEngine
```

## Lookback engines

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticContinuousFloatingLookbackEngine
.. autoclass:: pyquantlib.AnalyticContinuousFixedLookbackEngine
.. autoclass:: pyquantlib.AnalyticContinuousPartialFloatingLookbackEngine
.. autoclass:: pyquantlib.AnalyticContinuousPartialFixedLookbackEngine
```

```python
payoff   = ql.FloatingTypePayoff(ql.Call)
exercise = ql.EuropeanExercise(expiry)
option   = ql.ContinuousFloatingLookbackOption(100.0, payoff, exercise)
option.setPricingEngine(ql.AnalyticContinuousFloatingLookbackEngine(process))
```

## Cliquet engines

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticCliquetEngine
```

## Compound, chooser, exchange engines

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticCompoundOptionEngine
.. autoclass:: pyquantlib.AnalyticSimpleChooserEngine
.. autoclass:: pyquantlib.AnalyticComplexChooserEngine
.. autoclass:: pyquantlib.AnalyticEuropeanMargrabeEngine
```

Two BSM processes plus a correlation parameter.

```python
engine = ql.AnalyticEuropeanMargrabeEngine(process1, process2, 0.5)
```

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticAmericanMargrabeEngine
```

## Forward-start engines

```{eval-rst}
.. autoclass:: pyquantlib.ForwardEuropeanEngine
.. autoclass:: pyquantlib.ForwardPerformanceEuropeanEngine
```

```python
option = ql.ForwardVanillaOption(1.0, reset_date, payoff, exercise)
option.setPricingEngine(ql.ForwardEuropeanEngine(process))
```

## Quanto engines

```{eval-rst}
.. autoclass:: pyquantlib.QuantoVanillaEngine
```

Currency-adjusted Black-Scholes. Accepts explicit handles or raw objects (hidden handles).

```python
engine = ql.QuantoVanillaEngine(process, foreign_rate, fx_vol, correlation)
option.setPricingEngine(engine)
print(option.NPV(), option.qvega(), option.qrho(), option.qlambda())
```

## Cap / floor engines

```{eval-rst}
.. autoclass:: pyquantlib.BlackCapFloorEngine
```

Lognormal volatility: a flat volatility, a quote, or an optionlet volatility structure
(for example a {py:class}`pyquantlib.StrippedOptionletAdapter` or a
{py:class}`pyquantlib.SpreadedOptionletVolatility`).

```python
engine = ql.BlackCapFloorEngine(curve, 0.20)
engine = ql.BlackCapFloorEngine(curve, optionlet_vol)
```

```{eval-rst}
.. autoclass:: pyquantlib.BachelierCapFloorEngine
```

Normal volatility: a flat volatility, a quote, or an optionlet volatility structure.

```python
engine = ql.BachelierCapFloorEngine(curve, 0.005)
engine = ql.BachelierCapFloorEngine(curve, normal_optionlet_vol)
```

The two-argument forms take either two handles or two plain objects; mixing a handle with a
plain object is not supported.

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticCapFloorEngine
```

Analytic engine for affine short-rate models (Hull-White, CIR, G2++).

```{eval-rst}
.. autoclass:: pyquantlib.TreeCapFloorEngine
```

Lattice-based for short-rate models.

```{eval-rst}
.. autoclass:: pyquantlib.Gaussian1dCapFloorEngine
```

```python
model  = ql.Gsr(curve, [ql.Date(15, 1, 2025)], [0.01], 0.01)
engine = ql.Gaussian1dCapFloorEngine(model, integrationPoints=64)
```

## YoY inflation cap / floor engines

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationBlackCapFloorEngine
   :members:
   :undoc-members:
```

```python
engine = ql.YoYInflationBlackCapFloorEngine(yoy_index, yoy_vol_handle, curve_handle)
```

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationUnitDisplacedBlackCapFloorEngine
   :members:
   :undoc-members:

.. autoclass:: pyquantlib.YoYInflationBachelierCapFloorEngine
   :members:
   :undoc-members:
```

## Bond engines

```{eval-rst}
.. autoclass:: pyquantlib.DiscountingBondEngine
```

```python
engine = ql.DiscountingBondEngine(curve_handle)
bond.setPricingEngine(engine)
print(bond.cleanPrice())
```

## Convertible bond engines

```{eval-rst}
.. autoclass:: pyquantlib.BinomialConvertibleEngine
```

Tsiveriotis-Fernandes binomial lattice. Tree types: `jr`, `crr`, `eqp`, `trigeorgis`, `tian`, `lr`, `joshi`. Optional `creditSpread` parameter.

```python
engine = ql.BinomialConvertibleEngine(process, "crr", 801)
engine = ql.BinomialConvertibleEngine(process, "crr", 801, creditSpread=spread)
```

## Credit engines

```{eval-rst}
.. autoclass:: pyquantlib.MidPointCdsEngine
```

```python
engine = ql.MidPointCdsEngine(default_curve, 0.4, discount_curve)
```

```{eval-rst}
.. autoclass:: pyquantlib.IsdaCdsEngine
```

ISDA-standard CDS engine.

| Enum | Values |
|---|---|
| `IsdaNumericalFix` | `IsdaNone`, `Taylor` |
| `IsdaAccrualBias` | `HalfDayBias`, `NoBias` |
| `IsdaForwardsInCouponPeriod` | `Flat`, `Piecewise` |

## Swap engines

```{eval-rst}
.. autoclass:: pyquantlib.DiscountingSwapEngine
```

```{eval-rst}
.. autoclass:: pyquantlib.DiscountingConstNotionalCrossCurrencySwapEngine
```

Prices the constant-notional cross-currency swap family. Each leg is discounted on the curve
for its own currency, foreign-currency amounts are converted at the spot FX quote, and the
resulting NPV is expressed in the domestic currency. The quote is given as domestic units per
unit of foreign currency, quoted for settlement on the NPV date.

```python
usd_curve = ql.FlatForward(today, 0.045, ql.Actual365Fixed())
eur_curve = ql.FlatForward(today, 0.025, ql.Actual365Fixed())
spot_fx   = ql.SimpleQuote(1.05)   # USD per EUR

engine = ql.DiscountingConstNotionalCrossCurrencySwapEngine(
    ql.USDCurrency(), usd_curve,
    ql.EURCurrency(), eur_curve,
    spot_fx,
)
swap.setPricingEngine(engine)
print(swap.NPV())            # in USD
print(swap.inCcyLegNPV(0))   # in the currency of leg 0
```

`npvDate` and `settlementDate` default to the evaluation date, and `spotFXSettleDate` defaults
to the NPV date. `includeSettlementDateFlows` accepts `None` to defer to the global setting.

## FX forward engines

```{eval-rst}
.. autoclass:: pyquantlib.DiscountingFxForwardEngine
```

Prices an `FxForward` by discounting the two currency cash flows. Requires yield curves for both currencies and a spot FX quote.

```python
eur_curve = ql.FlatForward(today, 0.03, ql.Actual365Fixed())
usd_curve = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
spot_fx   = ql.SimpleQuote(1.08)   # EUR/USD spot

engine = ql.DiscountingFxForwardEngine(eur_curve, usd_curve, spot_fx)
fwd.setPricingEngine(engine)
print(fwd.NPV(), fwd.fairForwardRate())
```

## Futures engines

```{eval-rst}
.. autoclass:: pyquantlib.DiscountingPerpetualFuturesEngine
   :members:
```

Prices a {py:class}`pyquantlib.PerpetualFutures` contract following Ackerer, Hugonnier, and Jermann (2024). The funding schedule is supplied as parallel sequences of times, funding rates, and interest-rate differentials; `fundingInterpType` selects how they are interpolated between the given times.

```python
engine = ql.DiscountingPerpetualFuturesEngine(
    domestic_curve, foreign_curve, spot,
    fundingTimes=[0.25, 0.5, 1.0],
    fundingRates=[0.01, 0.012, 0.015],
    interestRateDiffs=[0.02, 0.02, 0.02],
)
perp.setPricingEngine(engine)
```

`maxT` bounds the integration horizon for the perpetual payoff and defaults to 60 years. Cost grows roughly fourfold per doubling, and the price usually converges well before it: in the example above, `maxT=5` matches the default to full double precision in 0.05 s against 11 s.

## Bond functions

```{eval-rst}
.. autoclass:: pyquantlib.BondFunctions
```

Static functions for bond analytics.

| Function | Returns |
|---|---|
| `cleanPrice(bond, rate)` | Clean price from yield |
| `dirtyPrice(bond, rate)` | Dirty price from yield |
| `bps(bond, rate)` | Basis-point sensitivity |
| `bondYield(bond, cleanPrice, dc, comp, freq)` | Yield from clean price |
| `duration(bond, rate, type)` | Duration (Modified, Macaulay, or Simple) |
| `convexity(bond, rate)` | Convexity |
| `basisPointValue(bond, rate)` | Basis-point value |
| `yieldValueBasisPoint(bond, rate)` | Yield value of a basis point |
| `zSpread(bond, cleanPrice, curve, dc, comp, freq)` | Z-spread |

```python
rate = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
print(ql.BondFunctions.cleanPrice(bond, rate))
print(ql.BondFunctions.duration(bond, rate, ql.DurationType.Modified))
print(ql.BondFunctions.convexity(bond, rate))
```

## Variance swap engines

```{eval-rst}
.. autoclass:: pyquantlib.ReplicatingVarianceSwapEngine
```

## Calculators

```{eval-rst}
.. autoclass:: pyquantlib.BlackCalculator
```

Black 1976 pricing and Greeks.

```python
calc = ql.BlackCalculator(payoff, forward, stdDev, discount)
print(calc.value(), calc.delta(spot), calc.gamma(spot), calc.vega(T))
```

```{eval-rst}
.. autoclass:: pyquantlib.BachelierCalculator
```

Bachelier (normal-volatility) pricing and Greeks. Same API as `BlackCalculator`.

## Free functions

### Black-76 (lognormal)

| Function | Returns |
|---|---|
| `blackFormula(optionType, strike, forward, stdDev, ...)` | Option price |
| `blackFormulaImpliedStdDev(optionType, strike, forward, blackPrice, ...)` | Implied $\sigma \sqrt{T}$ |
| `blackFormulaImpliedStdDevApproximation(...)` | Fast implied-vol approximation |
| `blackFormulaStdDevDerivative(strike, forward, stdDev, ...)` | $\partial$ price / $\partial \sigma\sqrt{T}$ |
| `blackFormulaVolDerivative(strike, forward, stdDev, expiry, ...)` | Vega |
| `blackFormulaForwardDerivative(optionType, strike, forward, stdDev, ...)` | Forward delta |
| `blackFormulaCashItmProbability(optionType, strike, forward, stdDev, ...)` | $N(d_2)$ |
| `blackFormulaAssetItmProbability(optionType, strike, forward, stdDev, ...)` | $N(d_1)$ |

### Bachelier (normal)

| Function | Returns |
|---|---|
| `bachelierBlackFormula(optionType, strike, forward, stdDev, ...)` | Option price |
| `bachelierBlackFormulaImpliedVol(optionType, strike, forward, tte, price, ...)` | Implied vol |
| `bachelierBlackFormulaStdDevDerivative(strike, forward, stdDev, ...)` | Vega component |

```python
forward, strike = 100.0, 100.0
vol, T = 0.20, 1.0
stdDev = vol * (T ** 0.5)

price          = ql.blackFormula(ql.OptionType.Call, strike, forward, stdDev)
impliedStdDev  = ql.blackFormulaImpliedStdDev(ql.OptionType.Call, strike, forward, price)
```

## See also

- {doc}`/concepts/pricing-engines`: instrument / engine separation and the bridge pattern
- {doc}`/concepts/finite-difference`: meshers, operators, schemes, and step conditions
- {doc}`/concepts/random-numbers`: the layered Rng / Rsg / Brownian-bridge architecture
- {doc}`processes`: stochastic processes consumed by these engines
- {doc}`models`: calibrated models consumed by short-rate, Heston, and Gaussian-1D engines
- {doc}`/cookbook/compare-engines`: same option, three engines
- {doc}`/cookbook/mc-engine-kwargs`: MC engine kwargs in practice
- {doc}`/cookbook/american-fd`: American option via FD
