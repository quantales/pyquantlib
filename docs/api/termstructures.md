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
Abstract base classes `YieldTermStructure`, `BlackVolTermStructure`, and `LocalVolTermStructure` are available in `pyquantlib.base` for custom implementations.
```
