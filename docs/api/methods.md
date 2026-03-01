# Methods Module

Monte Carlo simulation and finite-difference grid infrastructure.

## Paths

### Path

```{eval-rst}
.. autoclass:: pyquantlib.Path
```

Single-factor price path storing values at discrete time points.

```python
grid = ql.TimeGrid(1.0, 4)  # 4 steps over 1 year
path = ql.Path(grid)

# Access values
path[0]           # first value
path[-1]          # last value
path.front()      # same as path[0]
path.back()       # same as path[-1]
len(path)         # number of path values
path.timeGrid()   # underlying TimeGrid
```

### MultiPath

```{eval-rst}
.. autoclass:: pyquantlib.MultiPath
```

Correlated multi-asset paths, each sharing the same time grid.

```python
grid = ql.TimeGrid(1.0, 4)
mp = ql.MultiPath(2, grid)  # 2 assets

mp[0]               # Path for first asset
mp[1]               # Path for second asset
mp.assetNumber()     # 2
mp.pathSize()        # number of time points
len(mp)              # same as assetNumber()
```

### Sample Types

```{eval-rst}
.. autoclass:: pyquantlib.SamplePath
.. autoclass:: pyquantlib.SampleMultiPath
```

Weighted path samples returned by path generators. Each has `value` (the path) and `weight` (the sample weight).

## Brownian Bridge

### BrownianBridge

```{eval-rst}
.. autoclass:: pyquantlib.BrownianBridge
```

Builds Wiener process paths using Gaussian variates via bridge construction (variance reduction).

```python
# From number of steps
bb = ql.BrownianBridge(10)

# From time grid
grid = ql.TimeGrid(1.0, 10)
bb = ql.BrownianBridge(timeGrid=grid)

# Transform random variates into bridge path
import random
variates = [random.gauss(0, 1) for _ in range(bb.size())]
output = bb.transform(variates)

# Inspect bridge construction
bb.bridgeIndex()   # construction order
bb.leftWeight()    # interpolation weights
bb.stdDeviation()  # step standard deviations
```

## Path Generators

### GaussianPathGenerator

```{eval-rst}
.. autoclass:: pyquantlib.GaussianPathGenerator
```

Single-factor path generator using pseudo-random Gaussian variates (Mersenne Twister).

```python
process = ql.BlackScholesMertonProcess(spot, div, rf, vol)
rsg = ql.GaussianRandomSequenceGenerator(
    ql.UniformRandomSequenceGenerator(10, ql.MersenneTwisterUniformRng(42))
)

gen = ql.GaussianPathGenerator(process, 1.0, 10, rsg, False)
sample = gen.next()       # SamplePath
path = sample.value       # Path object
weight = sample.weight    # sample weight

anti = gen.antithetic()   # antithetic sample
```

### GaussianSobolPathGenerator

```{eval-rst}
.. autoclass:: pyquantlib.GaussianSobolPathGenerator
```

Single-factor path generator using Sobol low-discrepancy variates.

```python
sobol_rsg = ql.GaussianLowDiscrepancySequenceGenerator(
    ql.SobolRsg(10)
)
gen = ql.GaussianSobolPathGenerator(process, 1.0, 10, sobol_rsg, True)
```

### GaussianMultiPathGenerator

```{eval-rst}
.. autoclass:: pyquantlib.GaussianMultiPathGenerator
```

Multi-factor path generator using pseudo-random Gaussian variates.

```python
heston = ql.HestonProcess(rf, div, spot, 0.04, 1.0, 0.04, 0.5, -0.7)
grid = ql.TimeGrid(1.0, 50)
rsg = ql.GaussianRandomSequenceGenerator(
    ql.UniformRandomSequenceGenerator(
        heston.factors() * 50, ql.MersenneTwisterUniformRng(42)
    )
)

gen = ql.GaussianMultiPathGenerator(heston, grid, rsg)
sample = gen.next()         # SampleMultiPath
mp = sample.value           # MultiPath
spot_path = mp[0]           # Path for spot
var_path = mp[1]            # Path for variance
```

### GaussianSobolMultiPathGenerator

```{eval-rst}
.. autoclass:: pyquantlib.GaussianSobolMultiPathGenerator
```

Multi-factor path generator using Sobol low-discrepancy variates.

## Brownian Generators

Low-level generators for producing correlated Brownian increments. Used internally by MC engines and SLV models.

### MTBrownianGenerator

```{eval-rst}
.. autoclass:: pyquantlib.MTBrownianGenerator
```

Mersenne-Twister-based Brownian generator.

```python
gen = ql.MTBrownianGenerator(factors=2, steps=10, seed=42)
weight, variates = gen.nextStep()  # single time step
path = gen.nextPath()              # full path weight
```

### MTBrownianGeneratorFactory

```{eval-rst}
.. autoclass:: pyquantlib.MTBrownianGeneratorFactory
```

### SobolBrownianGenerator

```{eval-rst}
.. autoclass:: pyquantlib.SobolBrownianGenerator
```

Sobol-based Brownian generator with configurable ordering.

```python
gen = ql.SobolBrownianGenerator(
    factors=2, steps=10,
    ordering=ql.Ordering.Steps,
)
```

### SobolBrownianGeneratorFactory

```{eval-rst}
.. autoclass:: pyquantlib.SobolBrownianGeneratorFactory
```

### Burley2020SobolBrownianGenerator

```{eval-rst}
.. autoclass:: pyquantlib.Burley2020SobolBrownianGenerator
```

Scrambled Sobol Brownian generator (Burley 2020 hash-based Owen scrambling).

### Burley2020SobolBrownianGeneratorFactory

```{eval-rst}
.. autoclass:: pyquantlib.Burley2020SobolBrownianGeneratorFactory
```

## FDM Enums

### FdmSchemeDesc

```{eval-rst}
.. autoclass:: pyquantlib.FdmSchemeDesc
```

Finite difference scheme descriptors used by FD engines and the Heston SLV FDM calibration.

### FdmHestonGreensFctAlgorithm

```{eval-rst}
.. autoclass:: pyquantlib.FdmHestonGreensFctAlgorithm
   :members:
   :undoc-members:
```

Algorithm for computing Heston Fokker-Planck Green's functions: `ZeroCorrelation`, `Gaussian`, `SemiAnalytical`.

### FdmSquareRootFwdOpTransformationType

```{eval-rst}
.. autoclass:: pyquantlib.FdmSquareRootFwdOpTransformationType
   :members:
   :undoc-members:
```

Coordinate transformation for the square-root forward operator: `Plain`, `Power`, `Log`.

## FDM Grid Infrastructure

Layout, iterators, and meshers for multi-dimensional finite-difference grids.

### FdmLinearOpIterator

```{eval-rst}
.. autoclass:: pyquantlib.FdmLinearOpIterator
```

Iterator over grid points in an FDM layout. Tracks flat index and multi-dimensional coordinates.

```python
layout = ql.FdmLinearOpLayout([5, 3])
it = layout.begin()
it.index()        # 0
it.coordinates()  # [0, 0]
it.increment()
it.index()        # 1
it.coordinates()  # [1, 0]
```

### FdmLinearOpLayout

```{eval-rst}
.. autoclass:: pyquantlib.FdmLinearOpLayout
```

Memory layout for multi-dimensional FDM grids. Supports Python iteration.

```python
layout = ql.FdmLinearOpLayout([5, 3])
len(layout)            # 15
layout.dim()           # [5, 3]
layout.spacing()       # stride vector

for it in layout:
    print(it.index(), it.coordinates())
```

### Fdm1dMesher

```{eval-rst}
.. autoclass:: pyquantlib.Fdm1dMesher
```

Base class for one-dimensional FDM meshers. All 1D meshers below inherit from this.

```python
mesher = ql.Uniform1dMesher(0.0, 1.0, 5)
mesher.locations()  # grid point locations
mesher.dplus(0)     # forward difference at index 0
mesher.dminus(1)    # backward difference at index 1
```

### Uniform1dMesher

```{eval-rst}
.. autoclass:: pyquantlib.Uniform1dMesher
```

Uniform grid between start and end values.

### Concentrating1dMesher

```{eval-rst}
.. autoclass:: pyquantlib.Concentrating1dMesher
```

Grid concentrating points around one or more critical points.

```python
# Single concentration point at 100.0 with density 0.1
mesher = ql.Concentrating1dMesher(50.0, 150.0, 100, cPoint=(100.0, 0.1))

# Multiple concentration points
mesher = ql.Concentrating1dMesher(
    50.0, 150.0, 100,
    cPoints=[(100.0, 0.1, False), (120.0, 0.05, False)]
)
```

### Predefined1dMesher

```{eval-rst}
.. autoclass:: pyquantlib.Predefined1dMesher
```

Mesher from user-supplied grid points.

### FdmBlackScholesMesher

```{eval-rst}
.. autoclass:: pyquantlib.FdmBlackScholesMesher
```

One-dimensional mesher for the Black-Scholes process (in ln(S)).

```python
process = ql.BlackScholesMertonProcess(spot, div, rf, vol)
mesher = ql.FdmBlackScholesMesher(100, process, 1.0, 100.0)
```

### FdmHestonVarianceMesher

```{eval-rst}
.. autoclass:: pyquantlib.FdmHestonVarianceMesher
```

Variance dimension mesher for Heston models with volatility estimate.

```python
heston = ql.HestonProcess(rf, div, spot, 0.04, 1.0, 0.04, 0.5, -0.7)
mesher = ql.FdmHestonVarianceMesher(10, heston, 1.0)
mesher.volaEstimate()  # estimated volatility
```

### FdmHestonLocalVolatilityVarianceMesher

```{eval-rst}
.. autoclass:: pyquantlib.FdmHestonLocalVolatilityVarianceMesher
```

Heston variance mesher incorporating local volatility leverage.

### FdmCEV1dMesher

```{eval-rst}
.. autoclass:: pyquantlib.FdmCEV1dMesher
```

One-dimensional mesher for the CEV model.

### FdmSimpleProcess1dMesher

```{eval-rst}
.. autoclass:: pyquantlib.FdmSimpleProcess1dMesher
```

Generic one-dimensional mesher for any 1D stochastic process.

### FdmMesherComposite

```{eval-rst}
.. autoclass:: pyquantlib.FdmMesherComposite
```

Composite multi-dimensional mesher built from 1D meshers.

```python
# 2D grid from two 1D meshers
m1 = ql.FdmBlackScholesMesher(100, process, 1.0, 100.0)
m2 = ql.FdmHestonVarianceMesher(10, heston, 1.0)
mesher = ql.FdmMesherComposite(m1, m2)

mesher.layout()            # FdmLinearOpLayout
mesher.getFdm1dMeshers()   # underlying 1D meshers
```

### FdmQuantoHelper

```{eval-rst}
.. autoclass:: pyquantlib.FdmQuantoHelper
```

Helper for applying quanto adjustments in FDM pricing.

## FDM Boundary Conditions

### BoundaryConditionSide

```{eval-rst}
.. autoclass:: pyquantlib.BoundaryConditionSide
   :members:
   :undoc-members:
```

Side of the domain for boundary conditions: `None_`, `Upper`, `Lower`.

### FdmBoundaryCondition

```{eval-rst}
.. autoclass:: pyquantlib.FdmBoundaryCondition
```

Abstract boundary condition for FDM operators. Used in boundary condition sets passed to schemes.

## FDM Operators

### Building Block Operators

#### TripleBandLinearOp

```{eval-rst}
.. autoclass:: pyquantlib.TripleBandLinearOp
```

Tridiagonal (triple-band) linear operator on one grid dimension.

```python
mesher = ql.FdmMesherComposite(ql.Uniform1dMesher(0.0, 1.0, 10))
op = ql.TripleBandLinearOp(0, mesher)

result = op.apply(array)
result = op.solve_splitting(rhs, a, b)
op2 = op.mult(array)
op3 = op.add(other_op)
```

#### FirstDerivativeOp

```{eval-rst}
.. autoclass:: pyquantlib.FirstDerivativeOp
```

Central first-derivative operator (inherits from `TripleBandLinearOp`).

```python
d_dx = ql.FirstDerivativeOp(0, mesher)
gradient = d_dx.apply(values)
```

#### SecondDerivativeOp

```{eval-rst}
.. autoclass:: pyquantlib.SecondDerivativeOp
```

Central second-derivative operator (inherits from `TripleBandLinearOp`).

```python
d2_dx2 = ql.SecondDerivativeOp(0, mesher)
laplacian = d2_dx2.apply(values)
```

#### NinePointLinearOp

```{eval-rst}
.. autoclass:: pyquantlib.NinePointLinearOp
```

Nine-point cross-derivative operator on two grid dimensions.

#### SecondOrderMixedDerivativeOp

```{eval-rst}
.. autoclass:: pyquantlib.SecondOrderMixedDerivativeOp
```

Second-order mixed partial derivative operator (inherits from `NinePointLinearOp`).

```python
d2_dxdy = ql.SecondOrderMixedDerivativeOp(0, 1, mesher)
```

### Process Operators

Process-specific PDE operators, all inheriting from `FdmLinearOpComposite`. These encode the drift, diffusion, and cross terms for a given stochastic process. Constructed from a mesher and the corresponding process; the inherited methods (`size`, `setTime`, `apply`, `apply_mixed`, `apply_direction`, `solve_splitting`, `preconditioner`) are called internally by FDM schemes.

#### FdmBlackScholesOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmBlackScholesOp
```

Black-Scholes PDE operator.

```python
op = ql.FdmBlackScholesOp(mesher, process, strike=100.0)
```

#### FdmBlackScholesFwdOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmBlackScholesFwdOp
```

Black-Scholes forward (Fokker-Planck) operator.

#### Fdm2dBlackScholesOp

```{eval-rst}
.. autoclass:: pyquantlib.Fdm2dBlackScholesOp
```

Two-dimensional correlated Black-Scholes operator.

#### FdmHestonOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmHestonOp
```

Heston stochastic volatility PDE operator.

```python
op = ql.FdmHestonOp(mesher, heston_process)
```

#### FdmHestonFwdOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmHestonFwdOp
```

Heston forward (Fokker-Planck) operator.

#### FdmHestonHullWhiteOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmHestonHullWhiteOp
```

Three-factor Heston plus Hull-White operator.

#### FdmBatesOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmBatesOp
```

Bates (Heston + jumps) PDE operator.

#### FdmHullWhiteOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmHullWhiteOp
```

Hull-White short-rate PDE operator.

#### FdmG2Op

```{eval-rst}
.. autoclass:: pyquantlib.FdmG2Op
```

Two-factor Gaussian short-rate (G2) PDE operator.

#### FdmCEVOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmCEVOp
```

Constant Elasticity of Variance PDE operator.

#### FdmSabrOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmSabrOp
```

SABR stochastic volatility PDE operator.

#### FdmLocalVolFwdOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmLocalVolFwdOp
```

Local volatility forward (Fokker-Planck) operator.

#### FdmSquareRootFwdOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmSquareRootFwdOp
```

Square-root (CIR) forward operator, used in Heston SLV calibration.

#### FdmOrnsteinUhlenbeckOp

```{eval-rst}
.. autoclass:: pyquantlib.FdmOrnsteinUhlenbeckOp
```

Ornstein-Uhlenbeck mean-reverting PDE operator.

## FDM Schemes

Time-stepping schemes for evolving the PDE solution backward (or forward) in time. All schemes share the same interface:

```python
scheme.setStep(dt)                 # set time step size
array = scheme.step(array, t)      # advance one step from time t
```

The `step` method returns the modified array (Python copy semantics).

### ExplicitEulerScheme

```{eval-rst}
.. autoclass:: pyquantlib.ExplicitEulerScheme
```

Forward Euler (explicit) time stepping.

### ImplicitEulerScheme

```{eval-rst}
.. autoclass:: pyquantlib.ImplicitEulerScheme
```

Backward Euler (implicit) time stepping with iterative solver.

```python
scheme = ql.ImplicitEulerScheme(op, relTol=1e-8)
scheme.numberOfIterations()  # solver iterations from last step
```

#### ImplicitEulerSolverType

```{eval-rst}
.. autoclass:: pyquantlib.ImplicitEulerSolverType
   :members:
   :undoc-members:
```

Iterative solver for implicit schemes: `BiCGstab`, `GMRES`.

### CrankNicolsonScheme

```{eval-rst}
.. autoclass:: pyquantlib.CrankNicolsonScheme
```

Crank-Nicolson (theta = 0.5) time stepping.

```python
scheme = ql.CrankNicolsonScheme(0.5, op)
scheme.numberOfIterations()
```

### DouglasScheme

```{eval-rst}
.. autoclass:: pyquantlib.DouglasScheme
```

Douglas ADI time-stepping scheme.

### CraigSneydScheme

```{eval-rst}
.. autoclass:: pyquantlib.CraigSneydScheme
```

Craig-Sneyd ADI time-stepping scheme.

### HundsdorferScheme

```{eval-rst}
.. autoclass:: pyquantlib.HundsdorferScheme
```

Hundsdorfer ADI time-stepping scheme.

### ModifiedCraigSneydScheme

```{eval-rst}
.. autoclass:: pyquantlib.ModifiedCraigSneydScheme
```

Modified Craig-Sneyd ADI time-stepping scheme.

### MethodOfLinesScheme

```{eval-rst}
.. autoclass:: pyquantlib.MethodOfLinesScheme
```

Method of lines (Runge-Kutta) time-stepping scheme.

```{note}
Abstract base classes `FdmLinearOp`, `FdmLinearOpComposite`, `BrownianGenerator`, `BrownianGeneratorFactory`, and `FdmMesher` are available in `pyquantlib.base` for type checking.
```
