# Term structures

Bindings for the four families of term-structure objects: yield curves (and the rate helpers and bootstrap algorithms that build them), volatility surfaces (Black, local, swaption, optionlet, smile sections, SABR variants), credit / default-probability curves, and inflation curves. Each family has the same shape: a hierarchy of abstract bases under `pyquantlib.base`, concrete implementations in the top-level `pyquantlib` namespace, plus matching `*Handle` and `Relinkable*Handle` smart-pointer wrappers.

## At a glance

### Yield curves

| Group | Classes |
|---|---|
| Flat / interpolated | {py:class}`pyquantlib.FlatForward`, {py:class}`pyquantlib.ZeroCurve`, {py:class}`pyquantlib.DiscountCurve`, {py:class}`pyquantlib.ForwardCurve` |
| Spread / implied / composite | {py:class}`pyquantlib.ZeroSpreadedTermStructure`, {py:class}`pyquantlib.ForwardSpreadedTermStructure`, {py:class}`pyquantlib.ImpliedTermStructure`, {py:class}`pyquantlib.UltimateForwardTermStructure`, {py:class}`pyquantlib.CompositeZeroYieldStructure`, {py:class}`pyquantlib.QuantoTermStructure` |
| Piecewise (iterative bootstrap) | {py:class}`pyquantlib.PiecewiseLogLinearDiscount`, {py:class}`pyquantlib.PiecewiseLinearDiscount`, {py:class}`pyquantlib.PiecewiseCubicDiscount`, {py:class}`pyquantlib.PiecewiseLinearZero`, {py:class}`pyquantlib.PiecewiseCubicZero`, {py:class}`pyquantlib.PiecewiseSimpleZero`, {py:class}`pyquantlib.PiecewiseLinearForward`, {py:class}`pyquantlib.PiecewiseBackwardFlatForward`, {py:class}`pyquantlib.PiecewiseLogCubicDiscount`, {py:class}`pyquantlib.PiecewiseKrugerLogDiscount` |
| Global bootstrap | {py:class}`pyquantlib.PiecewiseLogLinearDiscountGlobal`, {py:class}`pyquantlib.PiecewiseLinearZeroGlobal`, {py:class}`pyquantlib.PiecewiseBackwardFlatForwardGlobal`, {py:class}`pyquantlib.MultiCurve` |
| Fitted (parametric) | {py:class}`pyquantlib.FittedBondDiscountCurve`, {py:class}`pyquantlib.NelsonSiegelFitting`, {py:class}`pyquantlib.SvenssonFitting`, {py:class}`pyquantlib.ExponentialSplinesFitting`, {py:class}`pyquantlib.CubicBSplinesFitting`, {py:class}`pyquantlib.SimplePolynomialFitting`, {py:class}`pyquantlib.SpreadFittingMethod` |
| Rate helpers | {py:class}`pyquantlib.DepositRateHelper`, {py:class}`pyquantlib.FraRateHelper`, {py:class}`pyquantlib.SwapRateHelper`, {py:class}`pyquantlib.OISRateHelper`, {py:class}`pyquantlib.MultipleResetsSwapRateHelper`, {py:class}`pyquantlib.FuturesRateHelper`, {py:class}`pyquantlib.OvernightIndexFutureRateHelper`, {py:class}`pyquantlib.SofrFutureRateHelper`, {py:class}`pyquantlib.BondHelper`, {py:class}`pyquantlib.FixedRateBondHelper` |
| Handles | {py:class}`pyquantlib.YieldTermStructureHandle`, {py:class}`pyquantlib.RelinkableYieldTermStructureHandle` |
| Enums | {py:class}`pyquantlib.Pillar` |

### Volatility surfaces

| Group | Classes |
|---|---|
| Black vol | {py:class}`pyquantlib.BlackConstantVol`, {py:class}`pyquantlib.BlackVarianceSurface`, {py:class}`pyquantlib.PiecewiseBlackVarianceSurface`, {py:class}`pyquantlib.BlackVolatilitySurfaceDelta`, {py:class}`pyquantlib.HestonBlackVolSurface` |
| Smile sections | {py:class}`pyquantlib.FlatSmileSection`, {py:class}`pyquantlib.SabrSmileSection`, {py:class}`pyquantlib.SabrInterpolatedSmileSection`, {py:class}`pyquantlib.NoArbSabrSmileSection`, {py:class}`pyquantlib.NoArbSabrInterpolatedSmileSection`, {py:class}`pyquantlib.NoArbSabrModel`, {py:class}`pyquantlib.KahaleSmileSection` |
| SABR free functions | {py:func}`pyquantlib.sabrVolatility`, {py:func}`pyquantlib.shiftedSabrVolatility`, {py:func}`pyquantlib.validateSabrParameters` |
| Local vol | {py:class}`pyquantlib.LocalConstantVol`, {py:class}`pyquantlib.LocalVolSurface`, {py:class}`pyquantlib.FixedLocalVolSurface`, {py:class}`pyquantlib.NoExceptLocalVolSurface` |
| Andreasen-Huge | {py:class}`pyquantlib.AndreasenHugeVolatilityInterpl`, {py:class}`pyquantlib.AndreasenHugeVolatilityAdapter`, {py:class}`pyquantlib.AndreasenHugeLocalVolAdapter` |
| Swaption | {py:class}`pyquantlib.ConstantSwaptionVolatility`, {py:class}`pyquantlib.SwaptionVolatilityMatrix`, {py:class}`pyquantlib.SwaptionVolatilityCube`, {py:class}`pyquantlib.SabrSwaptionVolatilityCube`, {py:class}`pyquantlib.ZabrSwaptionVolatilityCube`, {py:class}`pyquantlib.SpreadedSwaptionVolatility` |
| Optionlet | {py:class}`pyquantlib.ConstantOptionletVolatility`, {py:class}`pyquantlib.CapFloorTermVolSurface`, {py:class}`pyquantlib.OptionletStripper1`, {py:class}`pyquantlib.StrippedOptionletAdapter` |
| YoY inflation optionlet | {py:class}`pyquantlib.ConstantYoYOptionletVolatility` |
| Handles | {py:class}`pyquantlib.BlackVolTermStructureHandle`, {py:class}`pyquantlib.RelinkableBlackVolTermStructureHandle`, {py:class}`pyquantlib.LocalVolTermStructureHandle`, {py:class}`pyquantlib.RelinkableLocalVolTermStructureHandle`, {py:class}`pyquantlib.SwaptionVolatilityStructureHandle`, {py:class}`pyquantlib.RelinkableSwaptionVolatilityStructureHandle`, {py:class}`pyquantlib.OptionletVolatilityStructureHandle`, {py:class}`pyquantlib.RelinkableOptionletVolatilityStructureHandle`, {py:class}`pyquantlib.YoYOptionletVolatilitySurfaceHandle`, {py:class}`pyquantlib.RelinkableYoYOptionletVolatilitySurfaceHandle` |

### Credit and inflation

| Group | Classes |
|---|---|
| Credit | {py:class}`pyquantlib.FlatHazardRate`, {py:class}`pyquantlib.SpreadCdsHelper`, {py:class}`pyquantlib.UpfrontCdsHelper`, {py:class}`pyquantlib.PiecewiseLogLinearSurvival`, {py:class}`pyquantlib.PiecewiseFlatHazardRate`, {py:class}`pyquantlib.PiecewiseBackwardFlatHazard`, {py:class}`pyquantlib.DefaultProbabilityTermStructureHandle`, {py:class}`pyquantlib.RelinkableDefaultProbabilityTermStructureHandle` |
| Inflation curves | {py:class}`pyquantlib.ZeroInflationCurve`, {py:class}`pyquantlib.YoYInflationCurve`, {py:class}`pyquantlib.PiecewiseZeroInflationCurve`, {py:class}`pyquantlib.PiecewiseYoYInflationCurve` |
| Inflation helpers | {py:class}`pyquantlib.ZeroCouponInflationSwapHelper`, {py:class}`pyquantlib.YearOnYearInflationSwapHelper` |
| Seasonality | {py:class}`pyquantlib.MultiplicativePriceSeasonality`, {py:class}`pyquantlib.KerkhofSeasonality` |
| Inflation handles | {py:class}`pyquantlib.ZeroInflationTermStructureHandle`, {py:class}`pyquantlib.RelinkableZeroInflationTermStructureHandle`, {py:class}`pyquantlib.YoYInflationTermStructureHandle`, {py:class}`pyquantlib.RelinkableYoYInflationTermStructureHandle` |
| Inflation utilities | {py:func}`pyquantlib.inflationPeriod` |

```{note}
Abstract base classes (`YieldTermStructure`, `BlackVolTermStructure`, `LocalVolTermStructure`, `SmileSection`, `DefaultProbabilityTermStructure`, `RateHelper`, `RelativeDateRateHelper`, `FittingMethod`, `SwaptionVolatilityStructure`, `SwaptionVolatilityDiscrete`, `OptionletVolatilityStructure`, `CapFloorTermVolatilityStructure`, `StrippedOptionletBase`, `OptionletStripper`, `InflationTermStructure`, `ZeroInflationTermStructure`, `YoYInflationTermStructure`, `Seasonality`, `ZeroInflationHelper`, `YoYInflationHelper`, `YoYOptionletVolatilitySurface`) live under `pyquantlib.base` for `isinstance` checks and custom subclassing.
```

## Common patterns

### Wrap a curve in a handle and use it

```python
import pyquantlib as ql

curve  = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
handle = ql.YieldTermStructureHandle(curve)

# Most constructors that "want a curve" actually want a handle.
process = ql.GeneralizedBlackScholesProcess(spot, dq_handle, handle, vol_handle)
```

`Relinkable*Handle` adds `linkTo(new_curve)` on top, useful for scenarios that swap entire structures rather than just numbers; see {doc}`/cookbook/scenario-analysis`.

### Bootstrap a piecewise yield curve

```python
helpers = [
    ql.DepositRateHelper(0.032, euribor6m),
    ql.SwapRateHelper(0.04, ql.Period(5, ql.Years), ql.TARGET(),
                       ql.Annual, ql.Unadjusted,
                       ql.Thirty360(ql.Thirty360.BondBasis), euribor6m),
]

curve = ql.PiecewiseLogLinearDiscount(today, helpers, ql.Actual365Fixed())
print(curve.discount(1.0), curve.nodes())
```

`PiecewiseLogLinearDiscount` is one of nine `Piecewise*` variants; the name encodes (interpolation, what's interpolated). All share the same constructor and helper interface. See {doc}`/cookbook/bootstrap-yield-curve`.

### Build a Black variance surface from a vol grid

```python
vol_mat = ql.Matrix(len(strikes), len(expiries))
for i, row in enumerate(vols):
    for j, v in enumerate(row):
        vol_mat[i, j] = v

surface = ql.BlackVarianceSurface(today, calendar, expiries, strikes, vol_mat, dc)
surface.enableExtrapolation()

print(surface.blackVol(today + ql.Period("9M"), 95.0))
```

See {doc}`/cookbook/vol-surface` for the full pattern.

### Strip optionlet vols from a cap / floor surface

```python
surface = ql.CapFloorTermVolSurface(
    2, ql.TARGET(), ql.ModifiedFollowing,
    option_tenors, strikes, vol_matrix, ql.Actual365Fixed(),
)

stripper = ql.OptionletStripper1(surface, euribor6m, discount=ts_handle)
adapter  = ql.StrippedOptionletAdapter(stripper)
optionlet_vol = ql.OptionletVolatilityStructureHandle(adapter)
```

`OptionletStripper1` solves for caplet vols that re-price each cap; `StrippedOptionletAdapter` exposes the result as a standard `OptionletVolatilityStructure`.

### Bootstrap a default-probability curve from CDS spreads

```python
helpers = [
    ql.SpreadCdsHelper(spread, tenor, 1, ql.TARGET(),
                        ql.Quarterly, ql.Following,
                        ql.DateGeneration.TwentiethIMM,
                        ql.Actual360(), 0.4, discount_curve)
    for spread, tenor in zip(spreads, tenors)
]
curve = ql.PiecewiseLogLinearSurvival(today, helpers, ql.Actual365Fixed())
print(curve.survivalProbability(1.0), curve.nodes())
```

## Yield curves reference

### Flat curve

```{eval-rst}
.. autoclass:: pyquantlib.FlatForward
```

```python
flat = ql.FlatForward(today, 0.05, dc)
print(flat.discount(1.0))

# Hidden handle from a quote, for live updates
rate = ql.SimpleQuote(0.05)
flat = ql.FlatForward(today, rate, dc)
rate.setValue(0.06)
```

### Yield handles

```{eval-rst}
.. autoclass:: pyquantlib.YieldTermStructureHandle
.. autoclass:: pyquantlib.RelinkableYieldTermStructureHandle
```

### Rate helpers

```{eval-rst}
.. autoclass:: pyquantlib.Pillar
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.base.RateHelper
   :members:
```

```{eval-rst}
.. autoclass:: pyquantlib.base.RelativeDateRateHelper
```

Base for `DepositRateHelper`, `FraRateHelper`, `SwapRateHelper`, and `OISRateHelper`. Schedule re-derived when `Settings.evaluationDate` changes.

```{eval-rst}
.. autoclass:: pyquantlib.DepositRateHelper
```

```python
helper = ql.DepositRateHelper(0.032, ql.Euribor6M(curve_handle))
```

```{eval-rst}
.. autoclass:: pyquantlib.FraRateHelper
```

```python
helper = ql.FraRateHelper(0.035, 3, euribor6m)   # 3x9 FRA
```

```{eval-rst}
.. autoclass:: pyquantlib.SwapRateHelper
```

```python
helper = ql.SwapRateHelper(
    0.04, ql.Period(5, ql.Years), ql.TARGET(),
    ql.Annual, ql.Unadjusted,
    ql.Thirty360(ql.Thirty360.BondBasis), euribor6m,
)
swap = helper.swap()
```

```{eval-rst}
.. autoclass:: pyquantlib.OISRateHelper
```

```python
helper = ql.OISRateHelper(
    2, ql.Period(1, ql.Years), 0.035, overnight_index,
    averagingMethod=ql.RateAveraging.Type.Simple,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.MultipleResetsSwapRateHelper
```

Bootstrap helper for multiple-resets swap quotes. Accepts a fixed rate as a `float`, `QuoteHandle`, or `SimpleQuote` (hidden-handle convenience).

```python
helper = ql.MultipleResetsSwapRateHelper(
    0.04, ql.Period(2, ql.Years), overnight_index,
    resetsPerCoupon=2,
    averagingMethod=ql.RateAveraging.Type.Compound,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.FuturesRateHelper
   :members:
```

Bootstrap helper for IborIndex futures prices. The price is a quoted futures price (100 minus the rate), supplied as a `float` or a `QuoteHandle`, with an optional convexity adjustment. `type` selects the date rule from {py:class}`pyquantlib.Futures`.

```python
helper = ql.FuturesRateHelper(97.5, ql.Date(17, 9, 2025), euribor3m)

helper = ql.FuturesRateHelper(97.5, ql.Date(17, 9, 2025), 3,
                              ql.TARGET(), ql.ModifiedFollowing, True,
                              ql.Actual360())
```

```{eval-rst}
.. autoclass:: pyquantlib.OvernightIndexFutureRateHelper
   :members:
```

```{eval-rst}
.. autoclass:: pyquantlib.SofrFutureRateHelper
```

`OvernightIndexFutureRateHelper` bootstraps over overnight compounding futures between an explicit value date and delivery date. `SofrFutureRateHelper` derives from it and computes those dates from a reference month, year, and frequency, following the CME SOFR contract definition.

```python
helper = ql.SofrFutureRateHelper(97.0, ql.September, 2025, ql.Quarterly)
```

```{note}
When the reference period starts in the past, the overnight index history must be populated with `addFixing` before the helper can be used.
```

```{eval-rst}
.. autoclass:: pyquantlib.BondHelper
```

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateBondHelper
```

```python
helper = ql.FixedRateBondHelper(
    101.0, 3, 100.0, schedule, [0.04],
    ql.Thirty360(ql.Thirty360.BondBasis),
)
bond = helper.bond()
```

### Interpolated yield curves

```{eval-rst}
.. autoclass:: pyquantlib.ZeroCurve
```

```python
curve = ql.ZeroCurve(dates, rates, ql.Actual365Fixed())
print(curve.zeroRate(target_date, dc, ql.Continuous).rate())
```

```{eval-rst}
.. autoclass:: pyquantlib.DiscountCurve
```

```{eval-rst}
.. autoclass:: pyquantlib.ForwardCurve
```

### Spread / implied / composite curves

```{eval-rst}
.. autoclass:: pyquantlib.ZeroSpreadedTermStructure
.. autoclass:: pyquantlib.ForwardSpreadedTermStructure
.. autoclass:: pyquantlib.ImpliedTermStructure
.. autoclass:: pyquantlib.UltimateForwardTermStructure
.. autoclass:: pyquantlib.CompositeZeroYieldStructure
.. autoclass:: pyquantlib.QuantoTermStructure
```

```python
import operator

base    = ql.FlatForward(today, 0.03, dc)
spread  = ql.SimpleQuote(0.005)
spreaded = ql.ZeroSpreadedTermStructure(base, spread)
spread.setValue(0.01)

implied = ql.ImpliedTermStructure(base, today + ql.Period("6M"))
ufr     = ql.UltimateForwardTermStructure(base, llfr_quote, ufr_quote,
                                            ql.Period(20, ql.Years), alpha=0.1)
composite = ql.CompositeZeroYieldStructure(curve1, curve2, operator.add)
```

### Piecewise yield curves

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseLogLinearDiscount
.. autoclass:: pyquantlib.PiecewiseLinearDiscount
.. autoclass:: pyquantlib.PiecewiseCubicDiscount
.. autoclass:: pyquantlib.PiecewiseLinearZero
.. autoclass:: pyquantlib.PiecewiseCubicZero
.. autoclass:: pyquantlib.PiecewiseSimpleZero
.. autoclass:: pyquantlib.PiecewiseLinearForward
.. autoclass:: pyquantlib.PiecewiseBackwardFlatForward
.. autoclass:: pyquantlib.PiecewiseLogCubicDiscount
.. autoclass:: pyquantlib.PiecewiseKrugerLogDiscount
```

`PiecewiseFlatForward` is an alias for `PiecewiseBackwardFlatForward`. `PiecewiseLogCubicDiscount` uses monotonic log-cubic interpolation of discount factors; `PiecewiseKrugerLogDiscount` uses the Kruger log-cubic method, which is convexity-preserving but not monotonicity-constrained.

### Global-bootstrap piecewise curves

`GlobalBootstrap` solves for all nodes simultaneously instead of iteratively. Useful when instruments depend on each other or when iterative bootstrap fails to converge.

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseLogLinearDiscountGlobal
.. autoclass:: pyquantlib.PiecewiseLinearZeroGlobal
.. autoclass:: pyquantlib.PiecewiseBackwardFlatForwardGlobal
```

```python
curve = ql.PiecewiseLogLinearDiscountGlobal(
    today, helpers, ql.Actual365Fixed(),
    accuracy=1e-12, instrumentWeights=[1.0] * len(helpers),
)
```

```{eval-rst}
.. autoclass:: pyquantlib.MultiCurve
```

Manages a set of curves that form a dependency cycle, bootstrapping them simultaneously.

```python
int_3m = ql.RelinkableYieldTermStructureHandle()
int_6m = ql.RelinkableYieldTermStructureHandle()

curve_3m = ql.PiecewiseLogLinearDiscountGlobal(today, helpers_3m, dc, accuracy=1e-10)
curve_6m = ql.PiecewiseLogLinearDiscountGlobal(today, helpers_6m, dc, accuracy=1e-10)

mc      = ql.MultiCurve(accuracy=1e-10)
ext_3m  = mc.addBootstrappedCurve(int_3m, curve_3m)
ext_6m  = mc.addBootstrappedCurve(int_6m, curve_6m)
```

### Fitted bond discount curves

```{eval-rst}
.. autoclass:: pyquantlib.FittedBondDiscountCurve
```

```python
curve = ql.FittedBondDiscountCurve(today, helpers, dc, ql.NelsonSiegelFitting())
```

#### Fitting methods

```{eval-rst}
.. autoclass:: pyquantlib.NelsonSiegelFitting
.. autoclass:: pyquantlib.SvenssonFitting
.. autoclass:: pyquantlib.ExponentialSplinesFitting
.. autoclass:: pyquantlib.CubicBSplinesFitting
.. autoclass:: pyquantlib.SimplePolynomialFitting
.. autoclass:: pyquantlib.SpreadFittingMethod
```

```python
spread = ql.SpreadFittingMethod(ql.NelsonSiegelFitting(), reference_curve)
curve  = ql.FittedBondDiscountCurve(today, helpers, dc, spread)
```

## Volatility reference

### Black volatility

```{eval-rst}
.. autoclass:: pyquantlib.BlackConstantVol
```

```python
const_vol = ql.BlackConstantVol(today, ql.TARGET(), 0.20, dc)

vol = ql.SimpleQuote(0.20)
const_vol = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackVarianceSurface
```

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseBlackVarianceSurface
   :members:
```

Builds a Black volatility surface from one {py:class}`pyquantlib.base.SmileSection` per tenor, interpolating linearly in total variance between tenors at a given strike. Unlike {py:class}`pyquantlib.BlackVarianceSurface`, the smile at each tenor is supplied as a section object, so any smile parameterization (SABR, SVI, interpolated) can be used directly.

```python
surface = ql.PiecewiseBlackVarianceSurface(
    today, [d6m, d1y], [smile_6m, smile_1y], ql.Actual365Fixed())
```

The static `makeFromGrid` constructor mirrors the `BlackVarianceSurface` signature and provides a migration path, turning each column of the matrix into a linearly interpolated smile section:

```python
surface = ql.PiecewiseBlackVarianceSurface.makeFromGrid(
    today, dates, strikes, black_vols, ql.Actual365Fixed())
```

```{eval-rst}
.. autoclass:: pyquantlib.HestonBlackVolSurface
```

```python
model       = ql.HestonModel(heston_process)
vol_surface = ql.HestonBlackVolSurface(model)
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackVolatilitySurfaceDelta
```

An FX Black volatility surface parameterized by market deltas (25-delta put, ATM, 25-delta call, etc.) and maturities. Input quotes are {py:class}`pyquantlib.DeltaVolQuote` objects. Smile interpolation method and time-extrapolation strategy are configurable.

```python
maturities = [1.0, 2.0]
atm_quotes = [ql.DeltaVolQuote(ql.QuoteHandle(ql.SimpleQuote(0.10)),
                                ql.DeltaVolQuote.Spot, t,
                                ql.DeltaVolQuote.AtmDeltaNeutral)
              for t in maturities]
put_quotes  = [ql.DeltaVolQuote(-0.25, ql.QuoteHandle(ql.SimpleQuote(0.11)),
                                 t, ql.DeltaVolQuote.Spot)
               for t in maturities]
call_quotes = [ql.DeltaVolQuote(0.25, ql.QuoteHandle(ql.SimpleQuote(0.115)),
                                 t, ql.DeltaVolQuote.Spot)
               for t in maturities]

surface = ql.BlackVolatilitySurfaceDelta(
    today, maturities,
    putDeltas=[-0.25], callDeltas=[0.25],
    hasAtm=True,
    putVols=put_quotes, atmVols=atm_quotes, callVols=call_quotes,
    dc=ql.Actual365Fixed(), cal=ql.TARGET(),
    interpolationMethod=ql.BlackVolatilitySurfaceDelta.NaturalCubic,
    flatExtrapolation=True,
)
print(surface.blackVol(1.0, 1.08))
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackVolTimeExtrapolation
```

Time-extrapolation strategy used by `BlackVolatilitySurfaceDelta` beyond the last pillar: `FlatVolatility`, `UseInterpolator`, or `LinearVariance`.

#### Black vol handles

```{eval-rst}
.. autoclass:: pyquantlib.BlackVolTermStructureHandle
.. autoclass:: pyquantlib.RelinkableBlackVolTermStructureHandle
```

### Smile sections

```{eval-rst}
.. autoclass:: pyquantlib.FlatSmileSection
```

```python
fs = ql.FlatSmileSection(1.0, 0.2)
fs = ql.FlatSmileSection(ql.Date(15, 6, 2026), 0.2)
fs = ql.FlatSmileSection(1.0, 0.005, type=ql.VolatilityType.Normal)
```

```{eval-rst}
.. autoclass:: pyquantlib.SabrSmileSection
```

```python
section = ql.SabrSmileSection(1.0, 0.03, [0.05, 0.5, 0.4, -0.1])
section = ql.SabrSmileSection(ql.Date(15, 7, 2025), 0.03, params)
```

```{eval-rst}
.. autoclass:: pyquantlib.SabrInterpolatedSmileSection
```

```python
section = ql.SabrInterpolatedSmileSection(
    option_date, 0.03, strikes,
    hasFloatingStrikes=False,
    atmVolatility=0.18, vols=vols,
    alpha=0.05, beta=0.5, nu=0.4, rho=-0.1,
    isBetaFixed=True,
)
section.recalculate()
```

#### SABR free functions

```{eval-rst}
.. autofunction:: pyquantlib.sabrVolatility
.. autofunction:: pyquantlib.shiftedSabrVolatility
.. autofunction:: pyquantlib.validateSabrParameters
```

### No-arbitrage SABR

```{eval-rst}
.. autoclass:: pyquantlib.NoArbSabrModel
```

Doust (2012) no-arbitrage SABR. Provides arbitrage-free option prices, digital prices, and density.

```python
model = ql.NoArbSabrModel(1.0, 0.05, 0.05, 0.5, 0.2, -0.3)
print(model.optionPrice(0.05))
print(model.density(0.05))
print(model.absorptionProbability())
```

```{eval-rst}
.. autoclass:: pyquantlib.NoArbSabrSmileSection
.. autoclass:: pyquantlib.NoArbSabrInterpolatedSmileSection
```

### Kahale arbitrage-free smile

```{eval-rst}
.. autoclass:: pyquantlib.KahaleSmileSection
```

```python
source = ql.SabrSmileSection(1.0, 0.05, [0.3, 0.5, 0.4, -0.3])
kahale = ql.KahaleSmileSection(source)
kahale = ql.KahaleSmileSection(source, interpolate=True,
                                 exponentialExtrapolation=True)
```

### Andreasen-Huge volatility

```{eval-rst}
.. autoclass:: pyquantlib.AndreasenHugeVolatilityInterpl
```

Calibrates a local volatility surface to a sparse grid of vanilla options.

```python
ah = ql.AndreasenHugeVolatilityInterpl(
    calibration_set, spot, rTS, qTS,
    ql.AndreasenHugeInterpolationType.CubicSpline,
    ql.AndreasenHugeCalibrationType.Call,
)
min_err, max_err, avg_err = ah.calibrationError()
```

```{eval-rst}
.. autoclass:: pyquantlib.AndreasenHugeVolatilityAdapter
.. autoclass:: pyquantlib.AndreasenHugeLocalVolAdapter
```

### Local volatility

```{eval-rst}
.. autoclass:: pyquantlib.LocalConstantVol
.. autoclass:: pyquantlib.LocalVolSurface
```

```python
local_surface = ql.LocalVolSurface(black_vol, risk_free, dividend, 100.0)
print(local_surface.localVol(1.0, 100.0))
```

```{eval-rst}
.. autoclass:: pyquantlib.FixedLocalVolSurface
```

```{eval-rst}
.. autoclass:: pyquantlib.NoExceptLocalVolSurface
```

```{eval-rst}
.. autoclass:: pyquantlib.LocalVolTermStructureHandle
.. autoclass:: pyquantlib.RelinkableLocalVolTermStructureHandle
```

### Swaption volatility

```{eval-rst}
.. autoclass:: pyquantlib.ConstantSwaptionVolatility
.. autoclass:: pyquantlib.SwaptionVolatilityMatrix
.. autoclass:: pyquantlib.SwaptionVolatilityCube
.. autoclass:: pyquantlib.SabrSwaptionVolatilityCube
.. autoclass:: pyquantlib.ZabrSwaptionVolatilityCube
.. autoclass:: pyquantlib.SpreadedSwaptionVolatility
```

```python
spread       = ql.SimpleQuote(0.005)
spreaded_vol = ql.SpreadedSwaptionVolatility(base_vol_handle, spread)
```

```{eval-rst}
.. autoclass:: pyquantlib.SwaptionVolatilityStructureHandle
.. autoclass:: pyquantlib.RelinkableSwaptionVolatilityStructureHandle
```

### Optionlet volatility

```{eval-rst}
.. autoclass:: pyquantlib.ConstantOptionletVolatility
```

```{eval-rst}
.. autoclass:: pyquantlib.CapFloorTermVolSurface
```

```{eval-rst}
.. autoclass:: pyquantlib.OptionletStripper1
```

```python
stripper = ql.OptionletStripper1(surface, euribor6m, discount=ts_handle)
n        = stripper.optionletMaturities()
for i in range(n):
    print(stripper.optionletStrikes(i), stripper.optionletVolatilities(i))
```

```{eval-rst}
.. autoclass:: pyquantlib.StrippedOptionletAdapter
```

```{eval-rst}
.. autoclass:: pyquantlib.OptionletVolatilityStructureHandle
.. autoclass:: pyquantlib.RelinkableOptionletVolatilityStructureHandle
```

### YoY inflation optionlet

```{eval-rst}
.. autoclass:: pyquantlib.base.YoYOptionletVolatilitySurface
   :members:
   :undoc-members:
.. autoclass:: pyquantlib.ConstantYoYOptionletVolatility
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.YoYOptionletVolatilitySurfaceHandle
   :members:
   :undoc-members:
.. autoclass:: pyquantlib.RelinkableYoYOptionletVolatilitySurfaceHandle
   :members:
   :undoc-members:
```

## Credit reference

### Default-probability handles

```{eval-rst}
.. autoclass:: pyquantlib.DefaultProbabilityTermStructureHandle
.. autoclass:: pyquantlib.RelinkableDefaultProbabilityTermStructureHandle
```

### Flat hazard rate

```{eval-rst}
.. autoclass:: pyquantlib.FlatHazardRate
```

```python
default_curve = ql.FlatHazardRate(today, 0.01, dc)
print(default_curve.survivalProbability(1.0))
print(default_curve.defaultProbability(1.0))
print(default_curve.hazardRate(1.0))
```

### Default-probability helpers

```{eval-rst}
.. autoclass:: pyquantlib.SpreadCdsHelper
```

```python
helper = ql.SpreadCdsHelper(
    0.01, ql.Period(5, ql.Years), 1, ql.TARGET(),
    ql.Quarterly, ql.Following, ql.DateGeneration.TwentiethIMM,
    ql.Actual360(), 0.4, discount_curve,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.UpfrontCdsHelper
```

### Piecewise default curves

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseLogLinearSurvival
.. autoclass:: pyquantlib.PiecewiseFlatHazardRate
.. autoclass:: pyquantlib.PiecewiseBackwardFlatHazard
```

## Inflation reference

### Inflation term-structure bases

```{eval-rst}
.. autoclass:: pyquantlib.base.InflationTermStructure
   :members:
.. autoclass:: pyquantlib.base.ZeroInflationTermStructure
   :members:
.. autoclass:: pyquantlib.base.YoYInflationTermStructure
   :members:
```

### Inflation handles

```{eval-rst}
.. autoclass:: pyquantlib.ZeroInflationTermStructureHandle
.. autoclass:: pyquantlib.RelinkableZeroInflationTermStructureHandle
.. autoclass:: pyquantlib.YoYInflationTermStructureHandle
.. autoclass:: pyquantlib.RelinkableYoYInflationTermStructureHandle
```

### `inflationPeriod`

```{eval-rst}
.. autofunction:: pyquantlib.inflationPeriod
```

```python
start, end = ql.inflationPeriod(ql.Date(15, ql.March, 2024), ql.Monthly)
```

### Seasonality

```{eval-rst}
.. autoclass:: pyquantlib.base.Seasonality
   :members:
.. autoclass:: pyquantlib.MultiplicativePriceSeasonality
   :members:
.. autoclass:: pyquantlib.KerkhofSeasonality
   :members:
```

```python
factors = [1.0, 1.01, 1.02, 0.99, 0.98, 1.0, 1.01, 1.03, 0.97, 0.98, 1.0, 1.01]
seasonality = ql.MultiplicativePriceSeasonality(
    ql.Date(1, ql.January, 2024), ql.Monthly, factors,
)
curve.setSeasonality(seasonality)
```

### Inflation bootstrap helpers

```{eval-rst}
.. autoclass:: pyquantlib.base.ZeroInflationHelper
   :members:
.. autoclass:: pyquantlib.base.YoYInflationHelper
   :members:
.. autoclass:: pyquantlib.ZeroCouponInflationSwapHelper
   :members:
.. autoclass:: pyquantlib.YearOnYearInflationSwapHelper
   :members:
```

```python
helper = ql.ZeroCouponInflationSwapHelper(
    0.025, ql.Period(3, ql.Months),
    maturity_date, calendar, ql.ModifiedFollowing,
    day_counter, cpi_index, ql.CPI.Flat,
)
```

### Interpolated inflation curves

```{eval-rst}
.. autoclass:: pyquantlib.ZeroInflationCurve
   :members:
.. autoclass:: pyquantlib.YoYInflationCurve
   :members:
```

### Piecewise inflation curves

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseZeroInflationCurve
   :members:
.. autoclass:: pyquantlib.PiecewiseYoYInflationCurve
   :members:
```

```python
curve = ql.PiecewiseZeroInflationCurve(
    reference_date, base_date, ql.Monthly, day_counter, helpers,
)
```

## See also

- {doc}`/concepts/term-structures`: how curves and surfaces wire into processes and engines
- {doc}`/concepts/quotes-and-observables`: hidden vs relinkable handles, observer cascade
- {doc}`indexes`: indices that consume forwarding curves
- {doc}`/cookbook/bootstrap-yield-curve`: deposit + swap bootstrap end to end
- {doc}`/cookbook/piecewise-mixed-helpers`: deposits + FRAs + swaps in one curve
- {doc}`/cookbook/vol-surface`: building a `BlackVarianceSurface` from a quote grid
