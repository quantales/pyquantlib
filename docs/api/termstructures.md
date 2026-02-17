# Term Structures Module

## Yield Term Structures

### FlatForward

```{eval-rst}
.. autoclass:: pyquantlib.FlatForward
```

```python
today = ql.Date(15, 6, 2025)
dc = ql.Actual365Fixed()

flat = ql.FlatForward(today, 0.05, dc)
print(flat.discount(1.0))

# Using a quote (hidden handle, for dynamic updates)
rate_quote = ql.SimpleQuote(0.05)
flat = ql.FlatForward(today, rate_quote, dc)
rate_quote.setValue(0.06)  # Curve updates automatically
```

### YieldTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.YieldTermStructureHandle
```

### RelinkableYieldTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableYieldTermStructureHandle
```

## Rate Helpers

### Pillar

```{eval-rst}
.. autoclass:: pyquantlib.Pillar
   :members:
   :undoc-members:
```

### RateHelper

```{eval-rst}
.. autoclass:: pyquantlib.base.RateHelper
   :members:
```

### RelativeDateRateHelper

```{eval-rst}
.. autoclass:: pyquantlib.base.RelativeDateRateHelper
```

Rate helper with date schedule that updates when the evaluation date changes. Base class for `DepositRateHelper`, `FraRateHelper`, `SwapRateHelper`, and `OISRateHelper`.

### DepositRateHelper

```{eval-rst}
.. autoclass:: pyquantlib.DepositRateHelper
```

Rate helper for bootstrapping over deposit rates.

```python
euribor6m = ql.Euribor6M(curve_handle)
helper = ql.DepositRateHelper(0.032, euribor6m)
```

### FraRateHelper

```{eval-rst}
.. autoclass:: pyquantlib.FraRateHelper
```

Rate helper for bootstrapping over FRA rates.

```python
helper = ql.FraRateHelper(0.035, 3, euribor6m)  # 3x9 FRA
```

### SwapRateHelper

```{eval-rst}
.. autoclass:: pyquantlib.SwapRateHelper
```

Rate helper for bootstrapping over swap rates.

```python
helper = ql.SwapRateHelper(
    0.04, ql.Period(5, ql.Years), ql.TARGET(),
    ql.Annual, ql.Unadjusted,
    ql.Thirty360(ql.Thirty360.BondBasis), euribor6m
)
swap = helper.swap()  # access underlying VanillaSwap
```

### OISRateHelper

```{eval-rst}
.. autoclass:: pyquantlib.OISRateHelper
```

Rate helper for bootstrapping over OIS rates.

```python
overnight_index = ql.OvernightIndex("ESTR", 0, ql.EURCurrency(),
                                     ql.TARGET(), ql.Actual360(), curve)
helper = ql.OISRateHelper(2, ql.Period(1, ql.Years), 0.035, overnight_index)

# With explicit averaging method
helper = ql.OISRateHelper(
    2, ql.Period(1, ql.Years), 0.035, overnight_index,
    averagingMethod=ql.RateAveraging.Type.Simple,
)
```

### BondHelper

```{eval-rst}
.. autoclass:: pyquantlib.BondHelper
```

Bond helper for bootstrapping yield curves from a pre-constructed bond.

```python
bond = ql.FixedRateBond(3, 100.0, schedule, [0.04], dc)
helper = ql.BondHelper(ql.SimpleQuote(101.0), bond)
```

### FixedRateBondHelper

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateBondHelper
```

Convenience helper that constructs a fixed-rate bond internally.

```python
helper = ql.FixedRateBondHelper(
    101.0,          # clean price
    3,              # settlement days
    100.0,          # face amount
    schedule,
    [0.04],         # coupon rates
    ql.Thirty360(ql.Thirty360.BondBasis),
)
bond = helper.bond()  # access the underlying FixedRateBond
```

## Interpolated Yield Curves

### ZeroCurve

```{eval-rst}
.. autoclass:: pyquantlib.ZeroCurve
```

Zero rate curve with linear interpolation.

```python
dates = [today, today + ql.Period(1, ql.Years), today + ql.Period(5, ql.Years)]
rates = [0.03, 0.035, 0.04]
curve = ql.ZeroCurve(dates, rates, ql.Actual365Fixed())
print(curve.zeroRate(target_date, dc, ql.Continuous).rate())
print(curve.nodes())
```

### DiscountCurve

```{eval-rst}
.. autoclass:: pyquantlib.DiscountCurve
```

Discount factor curve with log-linear interpolation.

```python
dfs = [1.0, 0.965, 0.835]
curve = ql.DiscountCurve(dates, dfs, ql.Actual365Fixed())
print(curve.discount(target_date))
```

### ForwardCurve

```{eval-rst}
.. autoclass:: pyquantlib.ForwardCurve
```

Forward rate curve with backward-flat interpolation.

```python
forwards = [0.03, 0.035, 0.04]
curve = ql.ForwardCurve(dates, forwards, ql.Actual365Fixed())
print(curve.forwardRate(d1, d2, dc, ql.Continuous).rate())
```

### ZeroSpreadedTermStructure

```{eval-rst}
.. autoclass:: pyquantlib.ZeroSpreadedTermStructure
```

Yield term structure with an additive spread over a base curve.

```python
base = ql.FlatForward(today, 0.03, dc)
spread = ql.SimpleQuote(0.005)
spreaded = ql.ZeroSpreadedTermStructure(base, spread)
spread.setValue(0.01)  # spread updates dynamically
```

## Piecewise Yield Curves

### PiecewiseLogLinearDiscount

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseLogLinearDiscount
```

### PiecewiseLinearDiscount

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseLinearDiscount
```

### PiecewiseCubicDiscount

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseCubicDiscount
```

### PiecewiseLinearZero

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseLinearZero
```

### PiecewiseCubicZero

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseCubicZero
```

### PiecewiseLinearForward

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseLinearForward
```

### PiecewiseBackwardFlatForward

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseBackwardFlatForward
```

`PiecewiseFlatForward` is an alias for `PiecewiseBackwardFlatForward`.

Piecewise yield curves bootstrap a term structure from market instruments.

```python
helpers = [
    ql.DepositRateHelper(0.032, euribor6m),
    ql.SwapRateHelper(0.04, ql.Period(5, ql.Years), ql.TARGET(),
                      ql.Annual, ql.Unadjusted,
                      ql.Thirty360(ql.Thirty360.BondBasis), euribor6m),
]

curve = ql.PiecewiseLogLinearDiscount(today, helpers, ql.Actual365Fixed())
print(curve.discount(1.0))
print(curve.nodes())
```

## Fitted Bond Discount Curves

### FittedBondDiscountCurve

```{eval-rst}
.. autoclass:: pyquantlib.FittedBondDiscountCurve
```

Discount curve fitted to a set of bond prices using a parametric fitting method.

```python
curve = ql.FittedBondDiscountCurve(
    today, bond_helpers, dc,
    ql.NelsonSiegelFitting()
)
curve.discount(1.0)
```

### Fitting Methods

#### NelsonSiegelFitting

```{eval-rst}
.. autoclass:: pyquantlib.NelsonSiegelFitting
```

#### SvenssonFitting

```{eval-rst}
.. autoclass:: pyquantlib.SvenssonFitting
```

#### ExponentialSplinesFitting

```{eval-rst}
.. autoclass:: pyquantlib.ExponentialSplinesFitting
```

#### CubicBSplinesFitting

```{eval-rst}
.. autoclass:: pyquantlib.CubicBSplinesFitting
```

#### SimplePolynomialFitting

```{eval-rst}
.. autoclass:: pyquantlib.SimplePolynomialFitting
```

#### SpreadFittingMethod

```{eval-rst}
.. autoclass:: pyquantlib.SpreadFittingMethod
```

```python
# Fit with Nelson-Siegel
ns = ql.NelsonSiegelFitting()
curve = ql.FittedBondDiscountCurve(today, helpers, dc, ns)

# Fit with Svensson
sv = ql.SvenssonFitting()
curve = ql.FittedBondDiscountCurve(today, helpers, dc, sv)

# Spread fitting over a reference curve
spread = ql.SpreadFittingMethod(ql.NelsonSiegelFitting(), reference_curve)
curve = ql.FittedBondDiscountCurve(today, helpers, dc, spread)
```

## Volatility Term Structures

### BlackConstantVol

```{eval-rst}
.. autoclass:: pyquantlib.BlackConstantVol
```

```python
const_vol = ql.BlackConstantVol(today, ql.TARGET(), 0.20, dc)

# Using a quote (hidden handle)
vol = ql.SimpleQuote(0.20)
const_vol = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)
```

### BlackVarianceSurface

```{eval-rst}
.. autoclass:: pyquantlib.BlackVarianceSurface
```

### BlackVolTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.BlackVolTermStructureHandle
```

### RelinkableBlackVolTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableBlackVolTermStructureHandle
```

## SABR Volatility

### SabrSmileSection

```{eval-rst}
.. autoclass:: pyquantlib.SabrSmileSection
```

Parametric SABR smile section defined by alpha, beta, nu, rho.

```python
params = [0.05, 0.5, 0.4, -0.1]  # alpha, beta, nu, rho
forward = 0.03

# From exercise time
section = ql.SabrSmileSection(1.0, forward, params)
vol = section.volatility(0.03)

# From expiry date
section = ql.SabrSmileSection(ql.Date(15, 7, 2025), forward, params)
```

### SabrInterpolatedSmileSection

```{eval-rst}
.. autoclass:: pyquantlib.SabrInterpolatedSmileSection
```

Smile section that calibrates SABR parameters to market strikes and volatilities.

```python
option_date = ql.Date(15, 7, 2025)
forward = 0.03
strikes = [0.01, 0.02, 0.025, 0.03, 0.035, 0.04, 0.05]
vols = [0.30, 0.22, 0.19, 0.18, 0.185, 0.20, 0.25]

section = ql.SabrInterpolatedSmileSection(
    option_date, forward, strikes,
    hasFloatingStrikes=False,
    atmVolatility=0.18,
    vols=vols,
    alpha=0.05, beta=0.5, nu=0.4, rho=-0.1,
    isBetaFixed=True,
)
section.recalculate()
print(section.alpha(), section.rmsError())
```

### SABR Free Functions

```{eval-rst}
.. autofunction:: pyquantlib.sabrVolatility
.. autofunction:: pyquantlib.shiftedSabrVolatility
.. autofunction:: pyquantlib.validateSabrParameters
```

```python
vol = ql.sabrVolatility(strike, forward, T, alpha, beta, nu, rho)
vol_shifted = ql.shiftedSabrVolatility(strike, forward, T, alpha, beta, nu, rho, shift)
ql.validateSabrParameters(alpha, beta, nu, rho)
```

## Local Volatility

### LocalConstantVol

```{eval-rst}
.. autoclass:: pyquantlib.LocalConstantVol
```

### LocalVolSurface

```{eval-rst}
.. autoclass:: pyquantlib.LocalVolSurface
```

```python
local_surface = ql.LocalVolSurface(black_vol, risk_free, dividend, 100.0)
print(local_surface.localVol(1.0, 100.0))
```

### FixedLocalVolSurface

```{eval-rst}
.. autoclass:: pyquantlib.FixedLocalVolSurface
```

```python
import numpy as np

dates = [ref_date + ql.Period(i, ql.Months) for i in [1, 3, 6]]
strikes = [90.0, 100.0, 110.0]
vol_matrix = ql.Matrix(np.array([[0.22, 0.21, 0.20], ...]))

surface = ql.FixedLocalVolSurface(ref_date, dates, strikes, vol_matrix, dc)
```

### NoExceptLocalVolSurface

```{eval-rst}
.. autoclass:: pyquantlib.NoExceptLocalVolSurface
```

### LocalVolTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.LocalVolTermStructureHandle
```

### RelinkableLocalVolTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableLocalVolTermStructureHandle
```

## Swaption Volatility Term Structures

### ConstantSwaptionVolatility

```{eval-rst}
.. autoclass:: pyquantlib.ConstantSwaptionVolatility
```

```python
const_vol = ql.ConstantSwaptionVolatility(
    0, ql.TARGET(), ql.Following, 0.20, ql.Actual365Fixed()
)
```

### SwaptionVolatilityMatrix

```{eval-rst}
.. autoclass:: pyquantlib.SwaptionVolatilityMatrix
```

### SwaptionVolatilityCube

```{eval-rst}
.. autoclass:: pyquantlib.SwaptionVolatilityCube
```

### SabrSwaptionVolatilityCube

```{eval-rst}
.. autoclass:: pyquantlib.SabrSwaptionVolatilityCube
```

### SwaptionVolatilityStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.SwaptionVolatilityStructureHandle
```

### RelinkableSwaptionVolatilityStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableSwaptionVolatilityStructureHandle
```

## Optionlet Volatility Term Structures

### ConstantOptionletVolatility

```{eval-rst}
.. autoclass:: pyquantlib.ConstantOptionletVolatility
```

```python
const_vol = ql.ConstantOptionletVolatility(
    0, ql.TARGET(), ql.Following, 0.20, ql.Actual365Fixed()
)
```

### OptionletVolatilityStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.OptionletVolatilityStructureHandle
```

### RelinkableOptionletVolatilityStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableOptionletVolatilityStructureHandle
```

## YoY Inflation Optionlet Volatility

### YoYOptionletVolatilitySurface

```{eval-rst}
.. autoclass:: pyquantlib.base.YoYOptionletVolatilitySurface
   :members:
   :undoc-members:
```

Abstract base class for year-on-year inflation optionlet volatility surfaces.

### ConstantYoYOptionletVolatility

```{eval-rst}
.. autoclass:: pyquantlib.ConstantYoYOptionletVolatility
   :members:
   :undoc-members:
```

Constant year-on-year inflation optionlet volatility.

```python
yoy_vol = ql.ConstantYoYOptionletVolatility(
    0.10, 0, ql.TARGET(), ql.ModifiedFollowing, ql.Actual365Fixed(),
    ql.Period(3, ql.Months), ql.Monthly,
)
```

### YoYOptionletVolatilitySurfaceHandle

```{eval-rst}
.. autoclass:: pyquantlib.YoYOptionletVolatilitySurfaceHandle
   :members:
   :undoc-members:
```

### RelinkableYoYOptionletVolatilitySurfaceHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableYoYOptionletVolatilitySurfaceHandle
   :members:
   :undoc-members:
```

## Cap/Floor Term Volatility

### CapFloorTermVolSurface

```{eval-rst}
.. autoclass:: pyquantlib.CapFloorTermVolSurface
```

Cap/floor smile volatility surface interpolating market term volatilities.

```python
option_tenors = [ql.Period("1Y"), ql.Period("2Y"), ql.Period("5Y")]
strikes = [0.01, 0.02, 0.03, 0.04, 0.05]
vols = ql.Matrix(3, 5)  # populate with market volatilities

surface = ql.CapFloorTermVolSurface(
    2, ql.TARGET(), ql.ModifiedFollowing,
    option_tenors, strikes, vols, ql.Actual365Fixed()
)
print(surface.volatility(ql.Period("1Y"), 0.03))
```

## Optionlet Stripping

### OptionletStripper1

```{eval-rst}
.. autoclass:: pyquantlib.OptionletStripper1
```

Strips optionlet (caplet/floorlet) volatilities from a cap/floor term volatility surface.

```python
# Build cap/floor vol surface (see above)
index = ql.Euribor(ql.Period("6M"), ts_handle)
stripper = ql.OptionletStripper1(surface, index, discount=ts_handle)

# Access stripped optionlet data
n = stripper.optionletMaturities()
for i in range(n):
    print(stripper.optionletStrikes(i))
    print(stripper.optionletVolatilities(i))
```

### StrippedOptionletAdapter

```{eval-rst}
.. autoclass:: pyquantlib.StrippedOptionletAdapter
```

Adapts stripped optionlet data into an `OptionletVolatilityStructure` for use with pricing engines.

```python
adapter = ql.StrippedOptionletAdapter(stripper)
handle = ql.OptionletVolatilityStructureHandle(adapter)
vol = adapter.volatility(ql.Period("1Y"), 0.03)
```

## Credit Term Structures

### DefaultProbabilityTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.DefaultProbabilityTermStructureHandle
```

### RelinkableDefaultProbabilityTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableDefaultProbabilityTermStructureHandle
```

### FlatHazardRate

```{eval-rst}
.. autoclass:: pyquantlib.FlatHazardRate
```

Flat hazard rate default probability term structure.

```python
today = ql.Date(15, 1, 2025)
dc = ql.Actual365Fixed()
default_curve = ql.FlatHazardRate(today, 0.01, dc)
print(default_curve.survivalProbability(1.0))  # ~0.99
print(default_curve.defaultProbability(1.0))   # ~0.01
print(default_curve.hazardRate(1.0))           # 0.01
```

### Default Probability Helpers

#### SpreadCdsHelper

```{eval-rst}
.. autoclass:: pyquantlib.SpreadCdsHelper
```

Bootstrap helper for spread-quoted CDS.

```python
helper = ql.SpreadCdsHelper(
    0.01, ql.Period(5, ql.Years), 1, ql.TARGET(),
    ql.Quarterly, ql.Following, ql.DateGeneration.TwentiethIMM,
    ql.Actual360(), 0.4, discount_curve,
)
```

#### UpfrontCdsHelper

```{eval-rst}
.. autoclass:: pyquantlib.UpfrontCdsHelper
```

Bootstrap helper for upfront-quoted CDS.

```python
helper = ql.UpfrontCdsHelper(
    0.02, 0.01, ql.Period(5, ql.Years), 1, ql.TARGET(),
    ql.Quarterly, ql.Following, ql.DateGeneration.TwentiethIMM,
    ql.Actual360(), 0.4, discount_curve,
)
```

### Piecewise Default Curves

#### PiecewiseLogLinearSurvival

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseLogLinearSurvival
```

#### PiecewiseFlatHazardRate

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseFlatHazardRate
```

#### PiecewiseBackwardFlatHazard

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseBackwardFlatHazard
```

Bootstrap a default probability curve from CDS helpers.

```python
helpers = [
    ql.SpreadCdsHelper(spread, tenor, 1, ql.TARGET(),
                       ql.Quarterly, ql.Following,
                       ql.DateGeneration.TwentiethIMM,
                       ql.Actual360(), 0.4, discount_curve)
    for spread, tenor in zip(spreads, tenors)
]
curve = ql.PiecewiseLogLinearSurvival(today, helpers, ql.Actual365Fixed())
print(curve.survivalProbability(1.0))
print(curve.nodes())
```

## Inflation Term Structures

### InflationTermStructure

```{eval-rst}
.. autoclass:: pyquantlib.base.InflationTermStructure
   :members:
```

Base class for all inflation term structures. Provides `frequency()`, `baseRate()`, `baseDate()`, and `hasSeasonality()`.

### ZeroInflationTermStructure

```{eval-rst}
.. autoclass:: pyquantlib.base.ZeroInflationTermStructure
   :members:
```

Additional method: `zeroRate(date, observationLag, forceLinearInterpolation=False, extrapolate=False)`.

### YoYInflationTermStructure

```{eval-rst}
.. autoclass:: pyquantlib.base.YoYInflationTermStructure
   :members:
```

Additional method: `yoyRate(date, observationLag, forceLinearInterpolation=False, extrapolate=False)`.

### Inflation Handles

```{eval-rst}
.. autoclass:: pyquantlib.ZeroInflationTermStructureHandle
.. autoclass:: pyquantlib.RelinkableZeroInflationTermStructureHandle
.. autoclass:: pyquantlib.YoYInflationTermStructureHandle
.. autoclass:: pyquantlib.RelinkableYoYInflationTermStructureHandle
```

### inflationPeriod

```{eval-rst}
.. autofunction:: pyquantlib.inflationPeriod
```

Returns the (start, end) date pair for the inflation period containing the given date.

```python
start, end = ql.inflationPeriod(ql.Date(15, ql.March, 2024), ql.Monthly)
# start = Date(1, March, 2024), end = Date(31, March, 2024)
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
    ql.Date(1, ql.January, 2024), ql.Monthly, factors
)
curve.setSeasonality(seasonality)
```

### Inflation Bootstrap Helpers

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
    0.025,                          # quoted rate
    ql.Period(3, ql.Months),        # observation lag
    maturity_date, calendar, ql.ModifiedFollowing,
    day_counter, cpi_index, ql.CPI.Flat,
)
```

### Interpolated Inflation Curves

```{eval-rst}
.. autoclass:: pyquantlib.ZeroInflationCurve
   :members:
.. autoclass:: pyquantlib.YoYInflationCurve
   :members:
```

```python
curve = ql.ZeroInflationCurve(
    reference_date, dates, rates, ql.Monthly, day_counter
)
```

### Piecewise Inflation Curves

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseZeroInflationCurve
   :members:
.. autoclass:: pyquantlib.PiecewiseYoYInflationCurve
   :members:
```

```python
curve = ql.PiecewiseZeroInflationCurve(
    reference_date, base_date, ql.Monthly, day_counter, helpers
)
```

```{note}
Abstract base classes `YieldTermStructure`, `BlackVolTermStructure`, `LocalVolTermStructure`, `SmileSection`, `DefaultProbabilityTermStructure`, `RateHelper`, `RelativeDateRateHelper`, `FittingMethod`, `SwaptionVolatilityStructure`, `SwaptionVolatilityDiscrete`, `OptionletVolatilityStructure`, `CapFloorTermVolatilityStructure`, `StrippedOptionletBase`, `OptionletStripper`, `InflationTermStructure`, `ZeroInflationTermStructure`, `YoYInflationTermStructure`, `Seasonality`, `ZeroInflationHelper`, `YoYInflationHelper`, and `YoYOptionletVolatilitySurface` are available in `pyquantlib.base`.
```
