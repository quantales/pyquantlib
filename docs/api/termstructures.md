# Term Structures Module

Yield curves and volatility surfaces.

## Yield Term Structures

### FlatForward

A yield curve with constant forward rate.

```{eval-rst}
.. autoclass:: pyquantlib.FlatForward
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today
dc = ql.Actual365Fixed()

# Flat forward curve at 5%
flat = ql.FlatForward(today, 0.05, dc)
print(flat.discount(1.0))      # Discount factor for 1 year
print(flat.zeroRate(1.0, ql.Continuous).rate())  # Zero rate

# Using a quote (hidden handle, for dynamic updates)
rate_quote = ql.SimpleQuote(0.05)
flat = ql.FlatForward(today, rate_quote, dc)
rate_quote.setValue(0.06)  # Curve updates automatically

# Explicit handle (for relinking to different objects)
flat = ql.FlatForward(today, ql.QuoteHandle(rate_quote), dc)
```

### Handles

```{eval-rst}
.. autoclass:: pyquantlib.YieldTermStructureHandle
   :members:
   :undoc-members:

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

### BlackVarianceSurface

Volatility surface interpolated from market data.

```{eval-rst}
.. autoclass:: pyquantlib.BlackVarianceSurface
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today
dc = ql.Actual365Fixed()

# Constant volatility at 20% (fixed value)
const_vol = ql.BlackConstantVol(today, ql.TARGET(), 0.20, dc)
print(const_vol.blackVol(1.0, 100.0))  # Vol at T=1, K=100

# Using a quote (hidden handle, for dynamic updates)
vol = ql.SimpleQuote(0.20)
const_vol = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)
vol.setValue(0.25)  # Surface updates automatically

# Variance surface from market data
expiries = [today + ql.Period("1M"), today + ql.Period("3M"), today + ql.Period("1Y")]
strikes = [90.0, 100.0, 110.0]
vols = ql.Matrix(3, 3)  # 3 expiries x 3 strikes
# ... fill vols matrix ...
# surface = ql.BlackVarianceSurface(today, ql.TARGET(), expiries, strikes, vols, dc)
```

### Handles

```{eval-rst}
.. autoclass:: pyquantlib.BlackVolTermStructureHandle
   :members:
   :undoc-members:

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

### Usage

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today
dc = ql.Actual365Fixed()

# Constant local vol (hidden handle)
vol_quote = ql.SimpleQuote(0.20)
local_vol = ql.LocalConstantVol(today, vol_quote, dc)

# Local vol surface from Black vol (hidden handles)
risk_free = ql.FlatForward(today, 0.05, dc)
dividend = ql.FlatForward(today, 0.02, dc)
black_vol = ql.BlackConstantVol(today, ql.TARGET(), 0.20, dc)

local_surface = ql.LocalVolSurface(black_vol, risk_free, dividend, 100.0)
print(local_surface.localVol(1.0, 100.0))
```

### FixedLocalVolSurface

```{eval-rst}
.. autoclass:: pyquantlib.FixedLocalVolSurface
   :members:
   :undoc-members:
```

**Usage:**

```python
import numpy as np
import pyquantlib as ql

ref_date = ql.Date(15, 6, 2025)
dates = [ref_date + ql.Period(i, ql.Months) for i in [1, 3, 6]]
strikes = [90.0, 100.0, 110.0]

# Create Matrix from numpy array
vol_data = np.array([
    [0.22, 0.21, 0.20],  # strike 90
    [0.20, 0.19, 0.18],  # strike 100
    [0.21, 0.20, 0.19],  # strike 110
])
vol_matrix = ql.Matrix(vol_data)

surface = ql.FixedLocalVolSurface(
    ref_date, dates, strikes, vol_matrix, ql.Actual365Fixed()
)
```

### NoExceptLocalVolSurface

```{eval-rst}
.. autoclass:: pyquantlib.NoExceptLocalVolSurface
   :members:
   :undoc-members:
```

### Handles

```{eval-rst}
.. autoclass:: pyquantlib.LocalVolTermStructureHandle
   :members:
   :undoc-members:

.. autoclass:: pyquantlib.RelinkableLocalVolTermStructureHandle
   :members:
   :undoc-members:
```

```{note}
Abstract base classes `YieldTermStructure`, `BlackVolTermStructure`, and `LocalVolTermStructure` are available in `pyquantlib.base` for custom implementations.
```
