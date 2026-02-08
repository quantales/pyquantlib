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

```{note}
Abstract base classes `YieldTermStructure`, `BlackVolTermStructure`, `LocalVolTermStructure`, `SmileSection`, `DefaultProbabilityTermStructure`, `RateHelper`, and `RelativeDateRateHelper` are available in `pyquantlib.base`.
```
