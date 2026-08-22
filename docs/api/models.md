# Models

Bindings for the calibrated-model layer: `HestonModel`, the short-rate models (`Vasicek`, `HullWhite`, `BlackKarasinski`, `G2`, `CIR`), Gaussian-1D models (`Gsr`, `MarkovFunctional`), Heston-SLV, and the `*Helper` classes that drive calibration. Each model exposes the same `CalibratedModel` interface (`params`, `calibrate`, `setParams`); subclasses differ in the SDE they implement and the parameters that pin it down.

## At a glance

| Family | Classes |
|---|---|
| Heston / Bates | {py:class}`pyquantlib.HestonModel`, {py:class}`pyquantlib.PiecewiseTimeDependentHestonModel`, {py:class}`pyquantlib.BatesModel` |
| Short-rate | {py:class}`pyquantlib.Vasicek`, {py:class}`pyquantlib.HullWhite`, {py:class}`pyquantlib.BlackKarasinski`, {py:class}`pyquantlib.G2`, {py:class}`pyquantlib.CoxIngersollRoss`, {py:class}`pyquantlib.ExtendedCoxIngersollRoss` |
| Gaussian 1-D | {py:class}`pyquantlib.Gsr`, {py:class}`pyquantlib.MarkovFunctional` |
| Stochastic local vol | {py:class}`pyquantlib.HestonSLVFDMModel`, {py:class}`pyquantlib.HestonSLVMCModel` |
| Calibration helpers | {py:class}`pyquantlib.SwaptionHelper`, {py:class}`pyquantlib.CapHelper`, {py:class}`pyquantlib.HestonModelHelper` |
| Handles | {py:class}`pyquantlib.HestonModelHandle`, {py:class}`pyquantlib.ShortRateModelHandle`, {py:class}`pyquantlib.RelinkableShortRateModelHandle` |
| Parameters | {py:class}`pyquantlib.Parameter`, {py:class}`pyquantlib.ConstantParameter` |

```{note}
Abstract base classes for custom model implementations live in `pyquantlib.base`:
`CalibratedModel`, `ShortRateModel`, `OneFactorModel`, `OneFactorAffineModel`, `TwoFactorModel`, `AffineModel`, `TermStructureConsistentModel`, `Gaussian1dModel`, `CalibrationHelper`, `BlackCalibrationHelper`.
```

## Common patterns

### Build and use a Heston model

```python
import pyquantlib as ql

heston_process = ql.HestonProcess(
    risk_free_handle, dividend_handle, spot_handle,
    v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7,
)
model  = ql.HestonModel(heston_process)
engine = ql.AnalyticHestonEngine(model)
option.setPricingEngine(engine)
```

The model owns the parameter vector; the engine reads it on every pricing call. See {doc}`/cookbook/heston-calibration` for the full calibration loop.

### Read calibrated parameters via named accessors

```python
print(model.v0(), model.kappa(), model.theta(), model.sigma(), model.rho())
```

`HestonModel.params()` returns `(theta, kappa, sigma, rho, v0)`, which is *not* the same order as `HestonProcess`'s constructor (`(v0, kappa, theta, sigma, rho)`). Use the named accessors to avoid silent unpacking bugs.

### Build a Hull-White model and price a discount-bond option

```python
curve = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
hw    = ql.HullWhite(curve, a=0.1, sigma=0.01)

ts_handle = hw.termStructure()
price     = hw.discountBondOption(ql.Call, 0.95, 1.0, 2.0)

# Convexity bias (static method)
bias = ql.HullWhite.convexityBias(95.0, 0.25, 0.5, 0.01, 0.1)
```

### Build calibration helpers and run `calibrate`

```python
vol = ql.SimpleQuote(0.20)
helper = ql.SwaptionHelper(
    maturity=ql.Period(1, ql.Years),
    length=ql.Period(5, ql.Years),
    volatility=vol,
    index=ql.Euribor6M(curve),
    fixedLegTenor=ql.Period(1, ql.Years),
    fixedLegDayCounter=ql.Thirty360(ql.Thirty360.BondBasis),
    floatingLegDayCounter=ql.Actual360(),
    termStructure=curve,
)
helper.setPricingEngine(engine)

lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
ec = ql.EndCriteria(500, 50, 1e-8, 1e-8, 1e-8)
model.calibrate([helper, ...], lm, ec)
```

The optimisation loop is hidden in `calibrate()`: the optimiser hands a parameter vector to the model, the model re-prices each helper through its engine, the optimiser sees the errors and asks for a step. See {doc}`/concepts/calibration` for the full mechanism.

## Reference

### Heston and Bates

```{eval-rst}
.. autoclass:: pyquantlib.HestonModel
```

Constructor parameters (taken from the underlying `HestonProcess`):

| Parameter | Symbol |
|---|---|
| `v0` | $v_0$ |
| `kappa` | $\kappa$ |
| `theta` | $\theta$ |
| `sigma` | $\sigma$ |
| `rho` | $\rho$ |

```{eval-rst}
.. autoclass:: pyquantlib.PiecewiseTimeDependentHestonModel
```

```{eval-rst}
.. autoclass:: pyquantlib.HestonModelHandle
```

```{eval-rst}
.. autoclass:: pyquantlib.BatesModel
```

`BatesModel` adds three jump parameters on top of Heston:

| Parameter | Symbol |
|---|---|
| `lambda` | $\lambda$ |
| `nu` | $\nu$ |
| `delta` | $\delta$ |

### Short-rate models

```{eval-rst}
.. autoclass:: pyquantlib.Vasicek
```

SDE: $dr_t = a(b - r_t)\,dt + \sigma\,dW_t$.

| Parameter | Symbol |
|---|---|
| `r0` | $r_0$ |
| `a` | $a$ |
| `b` | $b$ |
| `sigma` | $\sigma$ |

```{eval-rst}
.. autoclass:: pyquantlib.HullWhite
```

SDE: $dr_t = (\theta(t) - a r_t)\,dt + \sigma\,dW_t$. The drift $\theta(t)$ is set internally to fit the input term structure.

| Parameter | Symbol |
|---|---|
| `a` | $a$ |
| `sigma` | $\sigma$ |

```{eval-rst}
.. autoclass:: pyquantlib.BlackKarasinski
```

SDE: $d(\ln r_t) = (\theta(t) - a \ln r_t)\,dt + \sigma\,dW_t$.

| Parameter | Symbol |
|---|---|
| `a` | $a$ |
| `sigma` | $\sigma$ |

```python
bk = ql.BlackKarasinski(curve, a=0.1, sigma=0.1)
ts_handle = bk.termStructure()
params    = bk.params()         # [a, sigma]
```

```{eval-rst}
.. autoclass:: pyquantlib.G2
```

Two-additive-factor Gaussian model:

$$\begin{cases}
r_t = \varphi(t) + x_t + y_t \\
dx_t = -a\,x_t\,dt + \sigma\,dW^1_t \\
dy_t = -b\,y_t\,dt + \eta\,dW^2_t \\
dW^1_t\,dW^2_t = \rho\,dt
\end{cases}$$

| Parameter | Symbol |
|---|---|
| `a` | $a$ |
| `sigma` | $\sigma$ |
| `b` | $b$ |
| `eta` | $\eta$ |
| `rho` | $\rho$ |

```python
g2 = ql.G2(curve, a=0.1, sigma=0.01, b=0.1, eta=0.01, rho=-0.75)
print(g2.a(), g2.sigma(), g2.b(), g2.eta(), g2.rho())
price = g2.discountBondOption(ql.Call, 0.95, 1.0, 2.0)
```

```{eval-rst}
.. autoclass:: pyquantlib.CoxIngersollRoss
```

CIR model; `params()` returns `(theta, k, sigma, r0)`.

```{eval-rst}
.. autoclass:: pyquantlib.ExtendedCoxIngersollRoss
```

Extended CIR model fitted to the initial term structure.

```{eval-rst}
.. autoclass:: pyquantlib.ShortRateModelHandle
```

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableShortRateModelHandle
```

```python
m1 = ql.Vasicek(r0=0.03)
m2 = ql.Vasicek(r0=0.05)
handle = ql.RelinkableShortRateModelHandle(m1)
handle.linkTo(m2)
```

### Calibration helpers

```{eval-rst}
.. autoclass:: pyquantlib.CalibrationErrorType
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.RateAveraging
```

```{eval-rst}
.. autoclass:: pyquantlib.SwaptionHelper
```

```{eval-rst}
.. autoclass:: pyquantlib.CapHelper
```

```python
helper = ql.CapHelper(
    ql.Period(5, ql.Years), vol, index, ql.Annual,
    index.dayCounter(), True, curve,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.HestonModelHelper
```

```python
helper = ql.HestonModelHelper(
    ql.Period(1, ql.Years), ql.TARGET(), 100.0, 100.0,
    vol_handle, risk_free, dividend,
)
```

### Parameters

```{eval-rst}
.. autoclass:: pyquantlib.Parameter
```

```{eval-rst}
.. autoclass:: pyquantlib.ConstantParameter
```

### Gaussian 1-D framework

```{eval-rst}
.. autoclass:: pyquantlib.Gsr
```

GSR model in forward measure. Supports constant or piecewise mean reversion and volatility, with both static and floating (handle-based) data.

```python
gsr = ql.Gsr(term_structure_handle, [], [0.01], 0.1)
gsr = ql.Gsr(term_structure, [step_date], [0.01, 0.02], [0.1, 0.15])
```

```{eval-rst}
.. autoclass:: pyquantlib.MarkovFunctional
```

```{eval-rst}
.. autoclass:: pyquantlib.MarkovFunctionalModelSettings
```

```{eval-rst}
.. autoclass:: pyquantlib.MarkovFunctionalModelOutputs
```

```python
mf = ql.MarkovFunctional(
    term_structure, 0.01, [], [0.01],
    swaption_vol_handle, expiries, tenors, swap_index,
)
```

### Stochastic local volatility

```{eval-rst}
.. autoclass:: pyquantlib.HestonSLVFDMModel
```

Heston SLV calibrated via Fokker-Planck FDM. Produces a leverage function that can be passed to `FdHestonVanillaEngine`.

```python
local_vol  = ql.LocalConstantVol(today, 0.20, dc)
heston     = ql.HestonModel(heston_process)
params     = ql.HestonSLVFokkerPlanckFdmParams(xGrid=51, vGrid=51)
slv        = ql.HestonSLVFDMModel(local_vol, heston, end_date, params)
leverage   = slv.leverageFunction()
engine     = ql.FdHestonVanillaEngine(heston, leverageFct=leverage)
```

```{eval-rst}
.. autoclass:: pyquantlib.HestonSLVMCModel
```

```python
bgf = ql.MTBrownianGeneratorFactory(seed=42)
slv = ql.HestonSLVMCModel(
    local_vol, heston, bgf, end_date,
    timeStepsPerYear=365, nBins=201, calibrationPaths=4096,
)
leverage = slv.leverageFunction()
```

```{eval-rst}
.. autoclass:: pyquantlib.HestonSLVFokkerPlanckFdmParams
```

The two enums that parametrise it, {py:class}`pyquantlib.FdmHestonGreensFctAlgorithm`
and {py:class}`pyquantlib.FdmSquareRootFwdOpTransformationType`, are documented
with the rest of the FDM machinery in {doc}`methods`.

## See also

- {doc}`/concepts/calibration`: optimisers, end criteria, and constraints
- {doc}`processes`: stochastic processes that feed these models
- {doc}`pricingengines`: engines built on top of the models
- {doc}`/cookbook/heston-calibration`: end-to-end Heston fit
