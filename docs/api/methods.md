# Methods

Bindings for the two simulation / numerical pipelines beneath the pricing engines: Monte Carlo (paths, Brownian bridge, path generators, Brownian generators) and finite difference (meshers, operators, schemes, step conditions, solvers, boundary conditions). Plus risk-neutral density calculators that consume processes and produce CDFs / PDFs / quantiles.

Most user code does not assemble these pieces by hand. The pre-built MC and FD engines under {doc}`pricingengines` wire them up internally. The bindings on this page exist for users building custom engines or post-processing simulation output.

## At a glance

| Group | Classes |
|---|---|
| Paths | {py:class}`pyquantlib.Path`, {py:class}`pyquantlib.MultiPath`, {py:class}`pyquantlib.SamplePath`, {py:class}`pyquantlib.SampleMultiPath` |
| Brownian bridge | {py:class}`pyquantlib.BrownianBridge` |
| Path generators | {py:class}`pyquantlib.GaussianPathGenerator`, {py:class}`pyquantlib.GaussianSobolPathGenerator`, {py:class}`pyquantlib.GaussianMultiPathGenerator`, {py:class}`pyquantlib.GaussianSobolMultiPathGenerator` |
| Brownian generators | {py:class}`pyquantlib.MTBrownianGenerator`, {py:class}`pyquantlib.MTBrownianGeneratorFactory`, {py:class}`pyquantlib.SobolBrownianGenerator`, {py:class}`pyquantlib.SobolBrownianGeneratorFactory`, {py:class}`pyquantlib.Burley2020SobolBrownianGenerator`, {py:class}`pyquantlib.Burley2020SobolBrownianGeneratorFactory` |
| FDM meshers (1-D) | {py:class}`pyquantlib.Uniform1dMesher`, {py:class}`pyquantlib.Concentrating1dMesher`, {py:class}`pyquantlib.Predefined1dMesher`, {py:class}`pyquantlib.FdmBlackScholesMesher`, {py:class}`pyquantlib.FdmHestonVarianceMesher`, {py:class}`pyquantlib.FdmHestonLocalVolatilityVarianceMesher`, {py:class}`pyquantlib.FdmCEV1dMesher`, {py:class}`pyquantlib.FdmSimpleProcess1dMesher`, {py:class}`pyquantlib.ExponentialJump1dMesher`, {py:class}`pyquantlib.Glued1dMesher` |
| FDM meshers (composite) | {py:class}`pyquantlib.FdmMesherComposite`, {py:class}`pyquantlib.FdmLinearOpLayout`, {py:class}`pyquantlib.FdmLinearOpIterator`, {py:class}`pyquantlib.FdmQuantoHelper` |
| FDM building-block ops | {py:class}`pyquantlib.TripleBandLinearOp`, {py:class}`pyquantlib.FirstDerivativeOp`, {py:class}`pyquantlib.SecondDerivativeOp`, {py:class}`pyquantlib.NinePointLinearOp`, {py:class}`pyquantlib.SecondOrderMixedDerivativeOp`, {py:class}`pyquantlib.NthOrderDerivativeOp` |
| FDM process ops | {py:class}`pyquantlib.FdmBlackScholesOp`, {py:class}`pyquantlib.FdmBlackScholesFwdOp`, {py:class}`pyquantlib.Fdm2dBlackScholesOp`, {py:class}`pyquantlib.FdmHestonOp`, {py:class}`pyquantlib.FdmHestonFwdOp`, {py:class}`pyquantlib.FdmHestonHullWhiteOp`, {py:class}`pyquantlib.FdmBatesOp`, {py:class}`pyquantlib.FdmHullWhiteOp`, {py:class}`pyquantlib.FdmG2Op`, {py:class}`pyquantlib.FdmCEVOp`, {py:class}`pyquantlib.FdmSabrOp`, {py:class}`pyquantlib.FdmLocalVolFwdOp`, {py:class}`pyquantlib.FdmSquareRootFwdOp`, {py:class}`pyquantlib.FdmOrnsteinUhlenbeckOp` |
| FDM schemes | {py:class}`pyquantlib.ExplicitEulerScheme`, {py:class}`pyquantlib.ImplicitEulerScheme`, {py:class}`pyquantlib.CrankNicolsonScheme`, {py:class}`pyquantlib.DouglasScheme`, {py:class}`pyquantlib.CraigSneydScheme`, {py:class}`pyquantlib.HundsdorferScheme`, {py:class}`pyquantlib.ModifiedCraigSneydScheme`, {py:class}`pyquantlib.MethodOfLinesScheme` |
| FDM inner-value calculators | {py:class}`pyquantlib.FdmCellAveragingInnerValue`, {py:class}`pyquantlib.FdmLogInnerValue`, {py:class}`pyquantlib.FdmLogBasketInnerValue`, {py:class}`pyquantlib.FdmZeroInnerValue` |
| FDM step conditions | {py:class}`pyquantlib.FdmSnapshotCondition`, {py:class}`pyquantlib.FdmAmericanStepCondition`, {py:class}`pyquantlib.FdmBermudanStepCondition`, {py:class}`pyquantlib.FdmDividendHandler`, {py:class}`pyquantlib.FdmStepConditionComposite`, {py:class}`pyquantlib.FdmArithmeticAverageCondition`, {py:class}`pyquantlib.FdmSimpleSwingCondition` |
| FDM solvers | {py:class}`pyquantlib.FdmSolverDesc`, {py:class}`pyquantlib.FdmBackwardSolver`, {py:class}`pyquantlib.Fdm1DimSolver`, {py:class}`pyquantlib.Fdm2DimSolver`, {py:class}`pyquantlib.Fdm3DimSolver`, {py:class}`pyquantlib.FdmBlackScholesSolver`, {py:class}`pyquantlib.FdmHestonSolver`, {py:class}`pyquantlib.FdmBatesSolver`, {py:class}`pyquantlib.FdmHullWhiteSolver`, {py:class}`pyquantlib.FdmG2Solver`, {py:class}`pyquantlib.Fdm2dBlackScholesSolver` |
| FDM boundary conditions | {py:class}`pyquantlib.FdmBoundaryCondition`, {py:class}`pyquantlib.FdmDirichletBoundary`, {py:class}`pyquantlib.FdmDiscountDirichletBoundary`, {py:class}`pyquantlib.FdmTimeDepDirichletBoundary` |
| FDM enums | {py:class}`pyquantlib.FdmSchemeDesc`, {py:class}`pyquantlib.FdmHestonGreensFctAlgorithm`, {py:class}`pyquantlib.FdmSquareRootFwdOpTransformationType`, {py:class}`pyquantlib.BoundaryConditionSide`, {py:class}`pyquantlib.ImplicitEulerSolverType` |
| RND calculators | {py:class}`pyquantlib.BSMRNDCalculator`, {py:class}`pyquantlib.GBSMRNDCalculator`, {py:class}`pyquantlib.HestonRNDCalculator`, {py:class}`pyquantlib.CEVRNDCalculator`, {py:class}`pyquantlib.SquareRootProcessRNDCalculator`, {py:class}`pyquantlib.LocalVolRNDCalculator` |

```{note}
Abstract base classes (`FdmLinearOp`, `FdmLinearOpComposite`, `BrownianGenerator`, `BrownianGeneratorFactory`, `FdmMesher`, `FdmStepCondition`, `FdmInnerValueCalculator`, `RiskNeutralDensityCalculator`) live under `pyquantlib.base` for `isinstance` checks and custom subclassing. See {doc}`/concepts/finite-difference` and {doc}`/concepts/random-numbers` for the architecture.
```

## Common patterns

### Generate a Black-Scholes MC path

```python
import pyquantlib as ql

process = ql.BlackScholesMertonProcess(spot, div, rf, vol)
rsg = ql.GaussianRandomSequenceGenerator(
    ql.UniformRandomSequenceGenerator(10, ql.MersenneTwisterUniformRng(42))
)

gen = ql.GaussianPathGenerator(process, length=1.0, steps=10, rsg=rsg, brownianBridge=False)

sample = gen.next()              # SamplePath
path   = sample.value            # Path
weight = sample.weight

anti = gen.antithetic()          # antithetic counterpart
```

The Sobol variant `GaussianSobolPathGenerator` swaps in a low-discrepancy sequence; multi-factor processes use `GaussianMultiPathGenerator` / `GaussianSobolMultiPathGenerator`.

### Build a 2-D Heston FDM grid

```python
process = ql.HestonProcess(rf, div, spot, 0.04, 1.0, 0.04, 0.5, -0.7)

spot_mesher = ql.FdmBlackScholesMesher(100, process.s0(), 1.0, 100.0)
var_mesher  = ql.FdmHestonVarianceMesher(10, process, 1.0)
mesher      = ql.FdmMesherComposite(spot_mesher, var_mesher)

mesher.layout()             # FdmLinearOpLayout
mesher.getFdm1dMeshers()    # the two underlying 1-D meshers
```

`FdmMesherComposite` builds an N-D grid from any combination of 1-D meshers. `FdmLinearOpLayout` exposes the flat index <-> coordinate mapping needed by operators.

### Apply a derivative operator

```python
mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.0, 1.0, 10))

d_dx   = ql.FirstDerivativeOp(0, mesher)
d2_dx2 = ql.SecondDerivativeOp(0, mesher)

gradient  = d_dx.apply(values)
laplacian = d2_dx2.apply(values)
```

Building-block operators inherit from `TripleBandLinearOp` (1-D) or `NinePointLinearOp` (2-D mixed). Process-level operators (`FdmBlackScholesOp`, `FdmHestonOp`, ...) compose them with the right drift / diffusion / cross terms.

### Run a backward FDM solve

```python
op       = ql.FdmBlackScholesOp(mesher, process, strike=100.0)
scheme   = ql.FdmSchemeDesc.Douglas()

solver = ql.FdmBackwardSolver(op, bcSet=[], schemeDesc=scheme)
result = solver.rollback(array, from_=1.0, to=0.0, steps=100, dampingSteps=0)
```

For the typical "build solver + interpolate" workflow, the dimension-specific helpers (`Fdm1DimSolver`, `Fdm2DimSolver`, `Fdm3DimSolver`) and the process-specific solvers (`FdmBlackScholesSolver`, `FdmHestonSolver`, ...) wrap this loop.

### Query a risk-neutral density

```python
import math

calc = ql.GBSMRNDCalculator(process)         # spot-space
calc.pdf(100.0, 1.0)                          # density at S=100, t=1
calc.cdf(100.0, 1.0)
calc.invcdf(0.5, 1.0)
```

`BSMRNDCalculator`, `HestonRNDCalculator`, and `LocalVolRNDCalculator` operate in *log-space* (`x = ln(S)`). `GBSMRNDCalculator` and `CEVRNDCalculator` operate in *spot-space*. Always check the calculator's space before passing inputs.

## Reference

### Paths

```{eval-rst}
.. autoclass:: pyquantlib.Path
```

```{eval-rst}
.. autoclass:: pyquantlib.MultiPath
```

```{eval-rst}
.. autoclass:: pyquantlib.SamplePath
.. autoclass:: pyquantlib.SampleMultiPath
```

Weighted samples returned by path generators. Each carries a `value` (the path) and `weight` (the sample weight).

### Brownian bridge

```{eval-rst}
.. autoclass:: pyquantlib.BrownianBridge
```

```python
bb = ql.BrownianBridge(10)                       # from number of steps
bb = ql.BrownianBridge(timeGrid=ql.TimeGrid(1.0, 10))

import random
variates = [random.gauss(0, 1) for _ in range(bb.size())]
output   = bb.transform(variates)

bb.bridgeIndex()
bb.leftWeight()
bb.stdDeviation()
```

### Path generators

```{eval-rst}
.. autoclass:: pyquantlib.GaussianPathGenerator
.. autoclass:: pyquantlib.GaussianSobolPathGenerator
.. autoclass:: pyquantlib.GaussianMultiPathGenerator
.. autoclass:: pyquantlib.GaussianSobolMultiPathGenerator
```

```python
heston = ql.HestonProcess(rf, div, spot, 0.04, 1.0, 0.04, 0.5, -0.7)
grid = ql.TimeGrid(1.0, 50)
rsg  = ql.GaussianRandomSequenceGenerator(
    ql.UniformRandomSequenceGenerator(
        heston.factors() * 50, ql.MersenneTwisterUniformRng(42),
    )
)
gen = ql.GaussianMultiPathGenerator(heston, grid, rsg)

sample    = gen.next()              # SampleMultiPath
mp        = sample.value            # MultiPath
spot_path = mp[0]
var_path  = mp[1]
```

### Brownian generators

```{eval-rst}
.. autoclass:: pyquantlib.MTBrownianGenerator
.. autoclass:: pyquantlib.MTBrownianGeneratorFactory
.. autoclass:: pyquantlib.SobolBrownianGenerator
.. autoclass:: pyquantlib.SobolBrownianGeneratorFactory
.. autoclass:: pyquantlib.Burley2020SobolBrownianGenerator
.. autoclass:: pyquantlib.Burley2020SobolBrownianGeneratorFactory
```

```python
gen = ql.MTBrownianGenerator(factors=2, steps=10, seed=42)
weight, variates = gen.nextStep()
path_weight = gen.nextPath()

sobol = ql.SobolBrownianGenerator(
    factors=2, steps=10, ordering=ql.Ordering.Steps,
)
```

### FDM enums

```{eval-rst}
.. autoclass:: pyquantlib.FdmSchemeDesc
```

Scheme descriptors used by FD engines and Heston SLV FDM calibration.

```{eval-rst}
.. autoclass:: pyquantlib.FdmHestonGreensFctAlgorithm
   :members:
   :undoc-members:
```

`ZeroCorrelation`, `Gaussian`, `SemiAnalytical`.

```{eval-rst}
.. autoclass:: pyquantlib.FdmSquareRootFwdOpTransformationType
   :members:
   :undoc-members:
```

`Plain`, `Power`, `Log`.

```{eval-rst}
.. autoclass:: pyquantlib.BoundaryConditionSide
   :members:
   :undoc-members:
```

`None_`, `Upper`, `Lower`.

### FDM grid infrastructure

```{eval-rst}
.. autoclass:: pyquantlib.FdmLinearOpIterator
```

```python
layout = ql.FdmLinearOpLayout([5, 3])
it = layout.begin()
it.index()         # 0
it.coordinates()   # [0, 0]
it.increment()
```

```{eval-rst}
.. autoclass:: pyquantlib.FdmLinearOpLayout
```

```python
layout = ql.FdmLinearOpLayout([5, 3])
len(layout)         # 15
layout.dim()        # [5, 3]
for it in layout:
    print(it.index(), it.coordinates())
```

```{eval-rst}
.. autoclass:: pyquantlib.Fdm1dMesher
```

```{eval-rst}
.. autoclass:: pyquantlib.Uniform1dMesher
```

```{eval-rst}
.. autoclass:: pyquantlib.Concentrating1dMesher
```

```python
mesher = ql.Concentrating1dMesher(50.0, 150.0, 100, cPoint=(100.0, 0.1))
mesher = ql.Concentrating1dMesher(
    50.0, 150.0, 100,
    cPoints=[(100.0, 0.1, False), (120.0, 0.05, False)],
)
```

```{eval-rst}
.. autoclass:: pyquantlib.Predefined1dMesher
.. autoclass:: pyquantlib.FdmBlackScholesMesher
.. autoclass:: pyquantlib.FdmHestonVarianceMesher
.. autoclass:: pyquantlib.FdmHestonLocalVolatilityVarianceMesher
.. autoclass:: pyquantlib.FdmCEV1dMesher
.. autoclass:: pyquantlib.FdmSimpleProcess1dMesher
.. autoclass:: pyquantlib.ExponentialJump1dMesher
.. autoclass:: pyquantlib.Glued1dMesher
```

```{eval-rst}
.. autoclass:: pyquantlib.FdmMesherComposite
.. autoclass:: pyquantlib.FdmQuantoHelper
```

### FDM boundary conditions

```{eval-rst}
.. autoclass:: pyquantlib.FdmBoundaryCondition
.. autoclass:: pyquantlib.FdmDirichletBoundary
.. autoclass:: pyquantlib.FdmDiscountDirichletBoundary
.. autoclass:: pyquantlib.FdmTimeDepDirichletBoundary
```

### FDM operators

#### Building blocks

```{eval-rst}
.. autoclass:: pyquantlib.TripleBandLinearOp
```

```python
op = ql.TripleBandLinearOp(0, mesher)
result  = op.apply(array)
result2 = op.solve_splitting(rhs, a, b)
```

```{eval-rst}
.. autoclass:: pyquantlib.FirstDerivativeOp
.. autoclass:: pyquantlib.SecondDerivativeOp
.. autoclass:: pyquantlib.NinePointLinearOp
.. autoclass:: pyquantlib.SecondOrderMixedDerivativeOp
.. autoclass:: pyquantlib.NthOrderDerivativeOp
```

#### Process operators

These encode the drift, diffusion, and cross terms for a given stochastic process. All inherit from `FdmLinearOpComposite` and are called by FDM schemes through the `apply` / `apply_mixed` / `apply_direction` / `solve_splitting` interface.

```{eval-rst}
.. autoclass:: pyquantlib.FdmBlackScholesOp
.. autoclass:: pyquantlib.FdmBlackScholesFwdOp
.. autoclass:: pyquantlib.Fdm2dBlackScholesOp
.. autoclass:: pyquantlib.FdmHestonOp
.. autoclass:: pyquantlib.FdmHestonFwdOp
.. autoclass:: pyquantlib.FdmHestonHullWhiteOp
.. autoclass:: pyquantlib.FdmBatesOp
.. autoclass:: pyquantlib.FdmHullWhiteOp
.. autoclass:: pyquantlib.FdmG2Op
.. autoclass:: pyquantlib.FdmCEVOp
.. autoclass:: pyquantlib.FdmSabrOp
.. autoclass:: pyquantlib.FdmLocalVolFwdOp
.. autoclass:: pyquantlib.FdmSquareRootFwdOp
.. autoclass:: pyquantlib.FdmOrnsteinUhlenbeckOp
```

### FDM schemes

All schemes share `setStep(dt)` and `step(array, t)`; the latter returns the modified array (Python copy semantics).

```{eval-rst}
.. autoclass:: pyquantlib.ExplicitEulerScheme
.. autoclass:: pyquantlib.ImplicitEulerScheme
```

```python
scheme = ql.ImplicitEulerScheme(op, relTol=1e-8)
scheme.numberOfIterations()
```

```{eval-rst}
.. autoclass:: pyquantlib.ImplicitEulerSolverType
   :members:
   :undoc-members:
```

`BiCGstab`, `GMRES`.

```{eval-rst}
.. autoclass:: pyquantlib.CrankNicolsonScheme
.. autoclass:: pyquantlib.DouglasScheme
.. autoclass:: pyquantlib.CraigSneydScheme
.. autoclass:: pyquantlib.HundsdorferScheme
.. autoclass:: pyquantlib.ModifiedCraigSneydScheme
.. autoclass:: pyquantlib.MethodOfLinesScheme
```

### FDM inner-value calculators

```{eval-rst}
.. autoclass:: pyquantlib.FdmCellAveragingInnerValue
```

```python
import math
calc = ql.FdmCellAveragingInnerValue(payoff, mesher, 0)
calc = ql.FdmCellAveragingInnerValue(payoff, mesher, 0, gridMapping=math.exp)
```

```{eval-rst}
.. autoclass:: pyquantlib.FdmLogInnerValue
.. autoclass:: pyquantlib.FdmLogBasketInnerValue
.. autoclass:: pyquantlib.FdmZeroInnerValue
```

### FDM step conditions

```{eval-rst}
.. autoclass:: pyquantlib.FdmSnapshotCondition
```

```python
snapshot = ql.FdmSnapshotCondition(0.5)
snapshot.getTime()
snapshot.getValues()
```

```{eval-rst}
.. autoclass:: pyquantlib.FdmAmericanStepCondition
.. autoclass:: pyquantlib.FdmBermudanStepCondition
.. autoclass:: pyquantlib.FdmDividendHandler
.. autoclass:: pyquantlib.FdmStepConditionComposite
.. autoclass:: pyquantlib.FdmArithmeticAverageCondition
.. autoclass:: pyquantlib.FdmSimpleSwingCondition
```

```python
composite = ql.FdmStepConditionComposite.vanillaComposite(
    dividends, exercise, mesher, calculator, refDate, dc,
)
joined = ql.FdmStepConditionComposite.joinConditions(snapshot, composite)
```

### FDM solvers

```{eval-rst}
.. autoclass:: pyquantlib.FdmSolverDesc
```

```{eval-rst}
.. autoclass:: pyquantlib.FdmBackwardSolver
```

```{eval-rst}
.. autoclass:: pyquantlib.Fdm1DimSolver
.. autoclass:: pyquantlib.Fdm2DimSolver
.. autoclass:: pyquantlib.Fdm3DimSolver
```

```python
solver = ql.Fdm2DimSolver(desc, ql.FdmSchemeDesc.Hundsdorfer(), op)
solver.interpolateAt(x, y)
solver.derivativeXY(x, y)
```

#### Process-specific solvers

```{eval-rst}
.. autoclass:: pyquantlib.FdmBlackScholesSolver
.. autoclass:: pyquantlib.FdmHestonSolver
.. autoclass:: pyquantlib.FdmBatesSolver
.. autoclass:: pyquantlib.FdmHullWhiteSolver
.. autoclass:: pyquantlib.FdmG2Solver
.. autoclass:: pyquantlib.Fdm2dBlackScholesSolver
```

### Risk-neutral density calculators

```{eval-rst}
.. autoclass:: pyquantlib.BSMRNDCalculator
```

Operates in log-space ($x = \ln S$).

```{eval-rst}
.. autoclass:: pyquantlib.GBSMRNDCalculator
```

Operates in spot-space ($x = S$).

```{eval-rst}
.. autoclass:: pyquantlib.HestonRNDCalculator
```

Operates in log-space.

```{eval-rst}
.. autoclass:: pyquantlib.CEVRNDCalculator
```

```python
calc = ql.CEVRNDCalculator(f0=100.0, alpha=0.3, beta=0.5)
calc.pdf(100.0, 1.0)
calc.massAtZero(1.0)
```

```{eval-rst}
.. autoclass:: pyquantlib.SquareRootProcessRNDCalculator
```

```python
calc = ql.SquareRootProcessRNDCalculator(v0=0.04, kappa=1.0, theta=0.04, sigma=0.2)
calc.pdf(0.04, 1.0)
calc.stationary_pdf(0.04)
calc.stationary_invcdf(0.5)
```

```{eval-rst}
.. autoclass:: pyquantlib.LocalVolRNDCalculator
```

Local volatility-based RND, log-space.

## See also

- {doc}`/concepts/finite-difference`: how meshers, operators, schemes, and step conditions compose into FD engines
- {doc}`/concepts/random-numbers`: the layered Rng / Rsg / Brownian-bridge architecture and how path generators sit on top
- {doc}`pricingengines`: pre-built MC and FD engines that wrap these pieces
