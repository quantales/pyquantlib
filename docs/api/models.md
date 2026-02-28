# Models Module

## Heston

### HestonModel

```{eval-rst}
.. autoclass:: pyquantlib.HestonModel
```

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `v0` | $v_0$ | Initial variance |
| `kappa` | $\kappa$ | Mean reversion speed |
| `theta` | $\theta$ | Long-term variance |
| `sigma` | $\sigma$ | Volatility of variance (vol of vol) |
| `rho` | $\rho$ | Correlation between spot and variance |

```python
heston_process = ql.HestonProcess(
    ql.YieldTermStructureHandle(risk_free),
    ql.YieldTermStructureHandle(dividend),
    ql.QuoteHandle(spot),
    v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
)
model = ql.HestonModel(heston_process)

engine = ql.AnalyticHestonEngine(model)
option.setPricingEngine(engine)
```

### PiecewiseTimeDependentHestonModel

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseTimeDependentHestonModel
```

### HestonModelHandle

```{eval-rst}
.. autoclass:: pyquantlib.HestonModelHandle
```

### BatesModel

```{eval-rst}
.. autoclass:: pyquantlib.BatesModel
```

Extends `HestonModel` with jump parameters:

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `lambda` | $\lambda$ | Jump intensity |
| `nu` | $\nu$ | Mean jump size |
| `delta` | $\delta$ | Jump size volatility |

```python
bates_process = ql.BatesProcess(
    risk_free, dividend, spot,
    0.04, 1.0, 0.04, 0.5, -0.7,  # v0, kappa, theta, sigma, rho
    0.1, -0.05, 0.1,              # lambda, nu, delta
)
model = ql.BatesModel(bates_process)
engine = ql.BatesEngine(model)
```

## Short Rate Models

### Vasicek

```{eval-rst}
.. autoclass:: pyquantlib.Vasicek
```

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `r0` | $r_0$ | Initial short rate |
| `a` | $a$ | Mean reversion speed |
| `b` | $b$ | Long-term mean rate |
| `sigma` | $\sigma$ | Volatility |

The Vasicek model follows the SDE: $dr_t = a(b - r_t)dt + \sigma dW_t$

```python
vasicek = ql.Vasicek(r0=0.05, a=0.3, b=0.03, sigma=0.01)

# Price a discount bond option
price = vasicek.discountBondOption(ql.Call, 0.95, 1.0, 2.0)
```

### HullWhite

```{eval-rst}
.. autoclass:: pyquantlib.HullWhite
```

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `a` | $a$ | Mean reversion speed |
| `sigma` | $\sigma$ | Volatility |

The Hull-White model extends Vasicek with time-dependent drift to fit the initial term structure: $dr_t = (\theta(t) - a \cdot r_t)dt + \sigma dW_t$

```python
# Create a term structure
today = ql.Date(15, 1, 2026)
ql.Settings.instance().evaluationDate = today
curve = ql.FlatForward(today, 0.05, ql.Actual365Fixed())

# Hull-White model fitted to the curve
hw = ql.HullWhite(curve, a=0.1, sigma=0.01)

# Access the fitted term structure
ts_handle = hw.termStructure()

# Price a discount bond option
price = hw.discountBondOption(ql.Call, 0.95, 1.0, 2.0)

# Compute futures convexity bias
bias = ql.HullWhite.convexityBias(95.0, 0.25, 0.5, 0.01, 0.1)
```

### BlackKarasinski

```{eval-rst}
.. autoclass:: pyquantlib.BlackKarasinski
```

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `a` | $a$ | Mean reversion speed |
| `sigma` | $\sigma$ | Volatility |

The Black-Karasinski model is a lognormal short-rate model: $d(\ln r_t) = (\theta(t) - a \ln r_t)dt + \sigma dW_t$

Unlike Hull-White, Black-Karasinski ensures positive interest rates since $r_t = e^{x_t}$ where $x_t$ follows an Ornstein-Uhlenbeck process.

```python
# Create a term structure
today = ql.Date(15, 1, 2026)
ql.Settings.instance().evaluationDate = today
curve = ql.FlatForward(today, 0.05, ql.Actual365Fixed())

# Black-Karasinski model fitted to the curve
bk = ql.BlackKarasinski(curve, a=0.1, sigma=0.1)

# Access the fitted term structure
ts_handle = bk.termStructure()

# Model parameters via CalibratedModel interface
params = bk.params()  # [a, sigma]
```

### G2

```{eval-rst}
.. autoclass:: pyquantlib.G2
```

| Parameter | Symbol | Description |
|-----------|--------|-------------|
| `a` | $a$ | First factor mean reversion speed |
| `sigma` | $\sigma$ | First factor volatility |
| `b` | $b$ | Second factor mean reversion speed |
| `eta` | $\eta$ | Second factor volatility |
| `rho` | $\rho$ | Correlation between factors |

The G2++ model is a two-additive-factor Gaussian model where the short rate is:
$r_t = \varphi(t) + x_t + y_t$

with $dx_t = -a x_t dt + \sigma dW^1_t$ and $dy_t = -b y_t dt + \eta dW^2_t$, and $dW^1_t dW^2_t = \rho dt$.

```python
# Create a term structure
today = ql.Date(15, 1, 2026)
ql.Settings.instance().evaluationDate = today
curve = ql.FlatForward(today, 0.05, ql.Actual365Fixed())

# G2++ model fitted to the curve
g2 = ql.G2(curve, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)

# Parameter accessors
print(g2.a(), g2.sigma(), g2.b(), g2.eta(), g2.rho())

# Price a discount bond option
price = g2.discountBondOption(ql.Call, 0.95, 1.0, 2.0)
```

### CoxIngersollRoss

```{eval-rst}
.. autoclass:: pyquantlib.CoxIngersollRoss
```

Cox-Ingersoll-Ross short-rate model. Parameters accessible via `params()` (theta, k, sigma, r0).

### ExtendedCoxIngersollRoss

```{eval-rst}
.. autoclass:: pyquantlib.ExtendedCoxIngersollRoss
```

Extended CIR model fitted to the initial term structure.

### ShortRateModelHandle

```{eval-rst}
.. autoclass:: pyquantlib.ShortRateModelHandle
```

```python
model = ql.Vasicek(r0=0.05)
handle = ql.ShortRateModelHandle(model)
```

### RelinkableShortRateModelHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableShortRateModelHandle
```

```python
model1 = ql.Vasicek(r0=0.03)
model2 = ql.Vasicek(r0=0.05)

handle = ql.RelinkableShortRateModelHandle(model1)
handle.linkTo(model2)  # Switch to different model
```

## Calibration Helpers

### CalibrationErrorType

```{eval-rst}
.. autoclass:: pyquantlib.CalibrationErrorType
   :members:
   :undoc-members:
```

### RateAveraging

```{eval-rst}
.. autoclass:: pyquantlib.RateAveraging
```

```{eval-rst}
.. autoclass:: pyquantlib.RateAveraging.Type
   :members:
   :undoc-members:
```

### SwaptionHelper

```{eval-rst}
.. autoclass:: pyquantlib.SwaptionHelper
```

Used for calibrating short-rate models to market swaption prices.

```python
# Create market environment
today = ql.Date(15, 1, 2026)
ql.Settings.instance().evaluationDate = today
curve = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
index = ql.Euribor6M(curve)

# Create swaption helper with 20% implied volatility
vol = ql.SimpleQuote(0.20)
helper = ql.SwaptionHelper(
    maturity=ql.Period(1, ql.Years),
    length=ql.Period(5, ql.Years),
    volatility=vol,
    index=index,
    fixedLegTenor=ql.Period(1, ql.Years),
    fixedLegDayCounter=ql.Thirty360(ql.Thirty360.BondBasis),
    floatingLegDayCounter=ql.Actual360(),
    termStructure=curve,
)

# Access underlying instruments
swap = helper.underlying()
swaption = helper.swaption()
```

### CapHelper

```{eval-rst}
.. autoclass:: pyquantlib.CapHelper
```

Calibration helper for ATM caps, used for calibrating short-rate models.

```python
helper = ql.CapHelper(
    ql.Period(5, ql.Years), vol, index, ql.Annual,
    index.dayCounter(), True, curve,
)
```

### HestonModelHelper

```{eval-rst}
.. autoclass:: pyquantlib.HestonModelHelper
```

Calibration helper for the Heston model using market option prices.

```python
helper = ql.HestonModelHelper(
    ql.Period(1, ql.Years), ql.TARGET(), 100.0, 100.0,
    vol, risk_free, div,
)
```

## Parameters

### Parameter

```{eval-rst}
.. autoclass:: pyquantlib.Parameter
```

### ConstantParameter

```{eval-rst}
.. autoclass:: pyquantlib.ConstantParameter
```

```{note}
Abstract base classes are available in `pyquantlib.base` for custom model implementations:
`CalibratedModel`, `ShortRateModel`, `OneFactorModel`, `OneFactorAffineModel`, `TwoFactorModel`, `AffineModel`, `TermStructureConsistentModel`, `CalibrationHelper`, `BlackCalibrationHelper`.
```
