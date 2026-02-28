# Methods Module

Monte Carlo simulation infrastructure: paths, path generators, Brownian bridges, and Brownian generators.

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

```{note}
Abstract base classes `BrownianGenerator` and `BrownianGeneratorFactory` are available in `pyquantlib.base` for type checking.
```
