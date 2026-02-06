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
.. autoclass:: pyquantlib.RateHelper
   :members:
```

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

### PiecewiseLinearZero

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseLinearZero
```

### PiecewiseCubicZero

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseCubicZero
```

### PiecewiseFlatForward

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseFlatForward
```

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

```{note}
Abstract base classes `YieldTermStructure`, `BlackVolTermStructure`, `LocalVolTermStructure`, and `SmileSection` are available in `pyquantlib.base` for custom implementations.
```
