# Math

Bindings for QuantLib's numerical-utility layer: linear algebra (`Array`, `Matrix`, decompositions), interpolation (1-D linear / step / cubic, mixed and log-space cubics, smile and Chebyshev / Lagrange variants, plus 2-D bilinear / bicubic), descriptive statistics, optimisation, distributions, root finders, ODE solvers.

```{seealso}
{doc}`/numpy` for `Array` / `Matrix` ↔ ndarray interop semantics.
```

## At a glance

| Family | Classes |
|---|---|
| Linear algebra | {py:class}`pyquantlib.Array`, {py:class}`pyquantlib.Matrix`, {py:class}`pyquantlib.SVD`, {py:class}`pyquantlib.SymmetricSchurDecomposition` |
| 1-D linear / step | {py:class}`pyquantlib.LinearInterpolation`, {py:class}`pyquantlib.LogLinearInterpolation`, {py:class}`pyquantlib.BackwardFlatInterpolation`, {py:class}`pyquantlib.ForwardFlatInterpolation` |
| 1-D cubic | {py:class}`pyquantlib.CubicInterpolation`, {py:class}`pyquantlib.CubicNaturalSpline`, {py:class}`pyquantlib.MonotonicCubicNaturalSpline`, {py:class}`pyquantlib.LogCubicInterpolation`, {py:class}`pyquantlib.LogCubicNaturalSpline`, {py:class}`pyquantlib.MonotonicLogCubicNaturalSpline`, {py:class}`pyquantlib.KrugerLogCubic`, {py:class}`pyquantlib.HarmonicLogCubic`, {py:class}`pyquantlib.FritschButlandLogCubic` |
| 1-D mixed | {py:class}`pyquantlib.MixedLinearCubicInterpolation`, {py:class}`pyquantlib.MixedLinearCubicNaturalSpline`, {py:class}`pyquantlib.MixedLinearMonotonicCubicNaturalSpline`, {py:class}`pyquantlib.MixedLinearKrugerCubic`, {py:class}`pyquantlib.MixedLinearFritschButlandCubic`, {py:class}`pyquantlib.LogMixedLinearCubicInterpolation`, {py:class}`pyquantlib.LogMixedLinearCubicNaturalSpline` |
| 1-D smile / structured | {py:class}`pyquantlib.SABRInterpolation`, {py:class}`pyquantlib.ConvexMonotoneInterpolation`, {py:class}`pyquantlib.LagrangeInterpolation`, {py:class}`pyquantlib.ChebyshevInterpolation` |
| 1-D extrapolation | {py:class}`pyquantlib.FlatExtrapolator` |
| 2-D | {py:class}`pyquantlib.BilinearInterpolation`, {py:class}`pyquantlib.BicubicSpline`, {py:class}`pyquantlib.BackwardflatLinearInterpolation`, {py:class}`pyquantlib.FlatExtrapolator2D` |
| Statistics | {py:class}`pyquantlib.Statistics`, {py:class}`pyquantlib.IncrementalStatistics`, {py:class}`pyquantlib.SequenceStatistics` |
| Optimisation | {py:class}`pyquantlib.LevenbergMarquardt`, {py:class}`pyquantlib.Simplex`, {py:class}`pyquantlib.ConjugateGradient`, {py:class}`pyquantlib.SteepestDescent`, {py:class}`pyquantlib.BFGS`, {py:class}`pyquantlib.LBFGSB`, {py:class}`pyquantlib.DifferentialEvolution`, {py:class}`pyquantlib.EndCriteria`, {py:class}`pyquantlib.Problem`, {py:class}`pyquantlib.NoConstraint`, {py:class}`pyquantlib.PositiveConstraint`, {py:class}`pyquantlib.BoundaryConstraint`, {py:class}`pyquantlib.CompositeConstraint` |
| Distributions | {py:class}`pyquantlib.NormalDistribution`, {py:class}`pyquantlib.CumulativeNormalDistribution`, {py:class}`pyquantlib.InverseCumulativeNormal`, {py:class}`pyquantlib.BivariateCumulativeNormalDistribution` |
| 1-D solvers | {py:class}`pyquantlib.Brent`, {py:class}`pyquantlib.Bisection`, {py:class}`pyquantlib.Secant`, {py:class}`pyquantlib.Newton` |
| ODE | {py:class}`pyquantlib.AdaptiveRungeKutta` |
| Misc | {py:class}`pyquantlib.RichardsonExtrapolation` |

```{note}
Abstract base classes (`Interpolation`, `Interpolation2D`, `Constraint`, `OptimizationMethod`, `CostFunction`) live under `pyquantlib.base` for `isinstance` checks and custom subclassing.
```

## Common patterns

### Move data between `ql.Array` / `ql.Matrix` and NumPy

```python
import pyquantlib as ql
import numpy as np

# ndarray -> ql (the binding copies into a fresh QL buffer)
arr = ql.Array(np.array([1.0, 2.0, 3.0]))
mat = ql.Matrix(np.eye(3))

# ql -> ndarray (np.asarray shares memory; np.array copies)
view = np.asarray(mat)        # owndata=False, mutates back into mat
copy = np.array(mat)           # owndata=True, independent
```

See {doc}`/cookbook/numpy-interop` for the full sharing semantics.

### Build a 1-D interpolation and call it

```python
x = [1.0, 2.0, 3.0, 4.0]
y = [1.0, 4.0, 9.0, 16.0]

interp = ql.CubicNaturalSpline(x, y)
interp(2.5)              # interpolated value
interp.derivative(2.5)   # first derivative
```

All 1-D interpolations share the call interface: `interp(x)` for the value, plus `derivative(x)`, `secondDerivative(x)`, and `primitive(x)` where the kernel supports them. They are *not* drop-in replacements for each other (different smoothness and shape-preservation properties).

### Calibrate a SABR smile

```python
strikes = [0.03, 0.04, 0.05, 0.06, 0.07]
vols    = [0.25, 0.22, 0.20, 0.21, 0.23]

sabr = ql.SABRInterpolation(
    strikes, vols, expiry=1.0, forward=0.05,
    alpha=0.2, beta=0.5, nu=0.4, rho=-0.3,
    alphaIsFixed=False, betaIsFixed=True,
    nuIsFixed=False, rhoIsFixed=False,
)
sabr.update()                                # runs the calibration
print(sabr.alpha(), sabr.rho(), sabr.rmsError())
```

### Run a 1-D root finder

```python
brent = ql.Brent()

# Bracket from a guess + step
root = brent.solve(lambda x: x**2 - 4, accuracy=1e-10, guess=1.0, step=0.5)

# Or with an explicit bracket
root = brent.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.0, 10.0)
```

`Brent`, `Bisection`, `Secant`, and `Newton` share the calling convention. `Newton` additionally accepts a derivative callable as the second argument. Common configuration: `setMaxEvaluations(n)`, `setLowerBound(x)`, `setUpperBound(x)`.

### Set up an optimisation problem

```python
lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
ec = ql.EndCriteria(
    maxIterations=500,
    maxStationaryStateIterations=50,
    rootEpsilon=1e-8,
    functionEpsilon=1e-8,
    gradientNormEpsilon=1e-8,
)
# Calibrated models call lm.minimize(...) internally; user-driven
# minimisation goes through ql.Problem.
```

The Levenberg-Marquardt + `EndCriteria` pair is the default for calibration. Other algorithms (`Simplex`, `ConjugateGradient`, `BFGS`, `DifferentialEvolution`) plug into the same `model.calibrate(helpers, method, end_criteria)` signature.

## Reference

### Linear algebra

```{eval-rst}
.. autoclass:: pyquantlib.Array
```

```{eval-rst}
.. autoclass:: pyquantlib.Matrix
```

```{eval-rst}
.. autoclass:: pyquantlib.SVD
```

```python
m = ql.Matrix([[1, 2], [3, 4], [5, 6]])
svd = ql.SVD(m)
U, V, s = svd.U(), svd.V(), svd.singularValues()
```

```{eval-rst}
.. autoclass:: pyquantlib.SymmetricSchurDecomposition
```

```python
m = ql.Matrix([[4, 1], [1, 3]])
ssd = ql.SymmetricSchurDecomposition(m)
print(ssd.eigenvalues(), ssd.eigenvectors())
```

### 1-D linear and step interpolations

```{eval-rst}
.. autoclass:: pyquantlib.LinearInterpolation
```

```{eval-rst}
.. autoclass:: pyquantlib.LogLinearInterpolation
```

Linear in log-space; useful for discount factors.

```{eval-rst}
.. autoclass:: pyquantlib.BackwardFlatInterpolation
```

Step function using the next node's value.

```{eval-rst}
.. autoclass:: pyquantlib.ForwardFlatInterpolation
```

Step function using the current node's value.

### 1-D cubic interpolations

```{eval-rst}
.. autoclass:: pyquantlib.CubicInterpolation
```

The fully configurable cubic; convenience subclasses below pre-fill common boundary conditions.

```python
interp = ql.CubicInterpolation(
    x, y,
    derivativeApprox=ql.CubicDerivativeApprox.Spline,
    leftCondition=ql.CubicBoundaryCondition.SecondDerivative,
    leftConditionValue=0.0,
    rightCondition=ql.CubicBoundaryCondition.SecondDerivative,
    rightConditionValue=0.0,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.CubicNaturalSpline
.. autoclass:: pyquantlib.MonotonicCubicNaturalSpline
.. autoclass:: pyquantlib.LogCubicInterpolation
.. autoclass:: pyquantlib.LogCubicNaturalSpline
.. autoclass:: pyquantlib.MonotonicLogCubicNaturalSpline
.. autoclass:: pyquantlib.KrugerLogCubic
.. autoclass:: pyquantlib.HarmonicLogCubic
.. autoclass:: pyquantlib.FritschButlandLogCubic
```

```{eval-rst}
.. autoclass:: pyquantlib.CubicDerivativeApprox
   :members:
   :undoc-members:

.. autoclass:: pyquantlib.CubicBoundaryCondition
   :members:
   :undoc-members:
```

### 1-D mixed interpolations

Use linear (or log-linear) for the first $n$ points and cubic (or log-cubic) for the rest.

```{eval-rst}
.. autoclass:: pyquantlib.MixedLinearCubicInterpolation
```

```python
interp = ql.MixedLinearCubicInterpolation(x, y, n=2)
```

```{eval-rst}
.. autoclass:: pyquantlib.MixedLinearCubicNaturalSpline
.. autoclass:: pyquantlib.MixedLinearMonotonicCubicNaturalSpline
.. autoclass:: pyquantlib.MixedLinearKrugerCubic
.. autoclass:: pyquantlib.MixedLinearFritschButlandCubic
.. autoclass:: pyquantlib.LogMixedLinearCubicInterpolation
.. autoclass:: pyquantlib.LogMixedLinearCubicNaturalSpline
```

```{eval-rst}
.. autoclass:: pyquantlib.MixedInterpolationBehavior
   :members:
   :undoc-members:
```

### 1-D smile and structured interpolations

```{eval-rst}
.. autoclass:: pyquantlib.SABRInterpolation
```

```{eval-rst}
.. autoclass:: pyquantlib.ConvexMonotoneInterpolation
```

```python
interp = ql.ConvexMonotoneInterpolation(
    x, y, quadraticity=0.3, monotonicity=0.7,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.LagrangeInterpolation
```

Supports evaluation with alternative $y$ values via `value(y, x)`.

```{eval-rst}
.. autoclass:: pyquantlib.ChebyshevInterpolation

.. autoclass:: pyquantlib.ChebyshevPointsType
   :members:
   :undoc-members:
```

```python
import math
interp = ql.ChebyshevInterpolation(20, math.sin)
interp(0.5)    # ~ sin(0.5)
```

### 2-D interpolations

```{eval-rst}
.. autoclass:: pyquantlib.BilinearInterpolation
```

`z` follows QuantLib convention: `z[y_idx][x_idx]`.

```{eval-rst}
.. autoclass:: pyquantlib.BicubicSpline
```

```{eval-rst}
.. autoclass:: pyquantlib.BackwardflatLinearInterpolation
```

Backward-flat in the first component, linear in the second.

```{eval-rst}
.. autoclass:: pyquantlib.FlatExtrapolator
```

Decorator that adds flat extrapolation outside the range of any 1-D interpolation.
Values are clamped to the boundary, the first and second derivatives vanish outside
the range, and the primitive extends linearly.

```python
inner  = ql.LinearInterpolation(x, y)
extrap = ql.FlatExtrapolator(inner)
extrap.enableExtrapolation()
extrap(0.0)
```

```{eval-rst}
.. autoclass:: pyquantlib.FlatExtrapolator2D
```

Decorator that adds flat extrapolation outside the range of any 2-D interpolation.

```python
inner  = ql.BilinearInterpolation(x, y, z)
extrap = ql.FlatExtrapolator2D(inner)
extrap.enableExtrapolation()
extrap(0.0, 0.0)
```

### Richardson extrapolation

```{eval-rst}
.. autoclass:: pyquantlib.RichardsonExtrapolation
```

```python
import math
re = ql.RichardsonExtrapolation(lambda h: math.sin(h) / h, 0.01, n=2.0)
re(2.0)
```

### Statistics

```{eval-rst}
.. autoclass:: pyquantlib.Statistics
```

General accumulator with empirical-distribution measures (`mean`, `standardDeviation`, `skewness`, `kurtosis`, `percentile`, `valueAtRisk`, `expectedShortfall`).

```{eval-rst}
.. autoclass:: pyquantlib.IncrementalStatistics
```

Online (streaming) statistics. Supports weighted observations.

```{eval-rst}
.. autoclass:: pyquantlib.SequenceStatistics
```

N-dimensional statistics with covariance and correlation.

### Optimisation

```{eval-rst}
.. autoclass:: pyquantlib.EndCriteria
```

```{eval-rst}
.. autoclass:: pyquantlib.LevenbergMarquardt
```

```{eval-rst}
.. autoclass:: pyquantlib.Simplex
```

Nelder-Mead simplex.

```{eval-rst}
.. autoclass:: pyquantlib.ConjugateGradient
.. autoclass:: pyquantlib.SteepestDescent
.. autoclass:: pyquantlib.BFGS
```

```{eval-rst}
.. autoclass:: pyquantlib.LBFGSB
```

Limited-memory BFGS with box constraints. Without active bounds it reduces to plain
L-BFGS. Bounds are taken from the problem's constraint unless explicit `lowerBound`
and `upperBound` arrays are passed to the constructor, which override it; use
`+/- sys.float_info.max` for unbounded coordinates.

```python
opt = ql.LBFGSB(lowerBound=ql.Array([-1.0, -1.0]),
                upperBound=ql.Array([1.0, 1.0]))
opt.minimize(problem, end_criteria)
```

```{eval-rst}
.. autoclass:: pyquantlib.DifferentialEvolution

.. autoclass:: pyquantlib.DEConfiguration

.. autoclass:: pyquantlib.DEStrategy
   :members:
   :undoc-members:

.. autoclass:: pyquantlib.DECrossoverType
   :members:
   :undoc-members:
```

```python
config    = ql.DEConfiguration().withStepsizeWeight(0.5).withCrossoverProbability(0.9)
optimiser = ql.DifferentialEvolution(config)
```

```{eval-rst}
.. autoclass:: pyquantlib.Problem
```

#### Constraints

```{eval-rst}
.. autoclass:: pyquantlib.NoConstraint
.. autoclass:: pyquantlib.PositiveConstraint
.. autoclass:: pyquantlib.BoundaryConstraint
.. autoclass:: pyquantlib.CompositeConstraint
```

### Distributions

```{eval-rst}
.. autoclass:: pyquantlib.NormalDistribution
```

```python
pdf = ql.NormalDistribution()                    # standard normal
pdf(0.0)                                          # ~ 0.3989
pdf2 = ql.NormalDistribution(average=5.0, sigma=2.0)
```

```{eval-rst}
.. autoclass:: pyquantlib.CumulativeNormalDistribution
```

```{eval-rst}
.. autoclass:: pyquantlib.InverseCumulativeNormal
```

```python
inv = ql.InverseCumulativeNormal()
inv(0.5)     # 0.0
inv(0.975)   # ~ 1.96

ql.InverseCumulativeNormal.standard_value(0.975)
```

```{eval-rst}
.. autoclass:: pyquantlib.BivariateCumulativeNormalDistribution
```

```python
bvn = ql.BivariateCumulativeNormalDistribution(rho=0.5)
bvn(0.0, 0.0)
```

### 1-D solvers

```{eval-rst}
.. autoclass:: pyquantlib.Brent
```

```{eval-rst}
.. autoclass:: pyquantlib.Bisection
```

```{eval-rst}
.. autoclass:: pyquantlib.Secant
```

```{eval-rst}
.. autoclass:: pyquantlib.Newton
```

```python
solver = ql.Newton()
root = solver.solve(
    lambda x: x ** 2 - 4,
    lambda x: 2 * x,
    1e-10, 1.0, 0.0, 10.0,
)
```

### ODE solvers

```{eval-rst}
.. autoclass:: pyquantlib.AdaptiveRungeKutta
```

```python
import math
rk = ql.AdaptiveRungeKutta(eps=1e-8)

# 1-D ODE: y' = y
rk.solve1d(lambda x, y: y, 1.0, 0.0, 1.0)        # ~ e

# N-D ODE system (harmonic oscillator)
rk(lambda x, y: [y[1], -y[0]], [1.0, 0.0], 0.0, math.pi)
```

## See also

- {doc}`/numpy`: NumPy / pandas interop reference
- {doc}`/concepts/calibration`: how the optimisers fit into the calibration pipeline
- {doc}`/cookbook/numpy-interop`: `Array` / `Matrix` ↔ ndarray sharing semantics
