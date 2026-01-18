# Term Structures Module

## Yield Term Structures

### FlatForward

A yield curve with constant forward rate.

```{eval-rst}
.. autoclass:: pyquantlib.FlatForward
   :members:
   :undoc-members:
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
   :members:
   :undoc-members:
```

### RelinkableYieldTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableYieldTermStructureHandle
   :members:
   :undoc-members:
```

## Volatility Term Structures

### BlackConstantVol

Constant Black volatility surface.

```{eval-rst}
.. autoclass:: pyquantlib.BlackConstantVol
   :members:
   :undoc-members:
```

```python
const_vol = ql.BlackConstantVol(today, ql.TARGET(), 0.20, dc)

# Using a quote (hidden handle)
vol = ql.SimpleQuote(0.20)
const_vol = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)
```

### BlackVarianceSurface

Volatility surface interpolated from market data.

```{eval-rst}
.. autoclass:: pyquantlib.BlackVarianceSurface
   :members:
   :undoc-members:
```

### BlackVolTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.BlackVolTermStructureHandle
   :members:
   :undoc-members:
```

### RelinkableBlackVolTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableBlackVolTermStructureHandle
   :members:
   :undoc-members:
```

## Local Volatility

### LocalConstantVol

```{eval-rst}
.. autoclass:: pyquantlib.LocalConstantVol
   :members:
   :undoc-members:
```

### LocalVolSurface

```{eval-rst}
.. autoclass:: pyquantlib.LocalVolSurface
   :members:
   :undoc-members:
```

```python
local_surface = ql.LocalVolSurface(black_vol, risk_free, dividend, 100.0)
print(local_surface.localVol(1.0, 100.0))
```

### FixedLocalVolSurface

```{eval-rst}
.. autoclass:: pyquantlib.FixedLocalVolSurface
   :members:
   :undoc-members:
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
   :members:
   :undoc-members:
```

### LocalVolTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.LocalVolTermStructureHandle
   :members:
   :undoc-members:
```

### RelinkableLocalVolTermStructureHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableLocalVolTermStructureHandle
   :members:
   :undoc-members:
```

```{note}
Abstract base classes `YieldTermStructure`, `BlackVolTermStructure`, and `LocalVolTermStructure` are available in `pyquantlib.base` for custom implementations.
```
