# Math Module

```{seealso}
{doc}`/numpy` for detailed NumPy interoperability documentation.
```

## Linear Algebra

### Array

```{eval-rst}
.. autoclass:: pyquantlib.Array
```

```python
import pyquantlib as ql
import numpy as np

arr = ql.Array([1.0, 2.0, 3.0])
arr = ql.Array(np.array([1, 2, 3]))

# Zero-copy view to numpy
np_view = np.array(arr, copy=False)
```

Functions expecting `Array` accept Python lists and numpy arrays directly:

```python
result = ql.DotProduct([1, 2, 3], [4, 5, 6])  # automatic conversion
```

### Matrix

```{eval-rst}
.. autoclass:: pyquantlib.Matrix
```

```python
mat = ql.Matrix([[1, 2], [3, 4]])
mat = ql.Matrix(np.array([[1, 2], [3, 4]], dtype=float))

# Zero-copy view to numpy
np_view = np.array(mat, copy=False)
```

### SVD

```{eval-rst}
.. autoclass:: pyquantlib.SVD
```

Singular value decomposition of a matrix.

```python
m = ql.Matrix([[1, 2], [3, 4], [5, 6]])
svd = ql.SVD(m)
U = svd.U()
V = svd.V()
s = svd.singularValues()
```

### SymmetricSchurDecomposition

```{eval-rst}
.. autoclass:: pyquantlib.SymmetricSchurDecomposition
```

Eigenvalue decomposition of a symmetric matrix.

```python
m = ql.Matrix([[4, 1], [1, 3]])
ssd = ql.SymmetricSchurDecomposition(m)
eigenvalues = ssd.eigenvalues()
eigenvectors = ssd.eigenvectors()
```

## Interpolation

Interpolation classes for constructing continuous functions from discrete data points.

### LinearInterpolation

```{eval-rst}
.. autoclass:: pyquantlib.LinearInterpolation
```

```python
x = [1.0, 2.0, 3.0]
y = [10.0, 20.0, 30.0]
interp = ql.LinearInterpolation(x, y)

interp(1.5)  # 15.0
interp.derivative(1.5)  # 10.0
```

### LogLinearInterpolation

```{eval-rst}
.. autoclass:: pyquantlib.LogLinearInterpolation
```

Log-linear interpolation interpolates linearly in log-space, useful for discount factors.

```python
x = [1.0, 2.0]
y = [1.0, math.e]
interp = ql.LogLinearInterpolation(x, y)
interp(1.5)  # exp(0.5)
```

### BackwardFlatInterpolation

```{eval-rst}
.. autoclass:: pyquantlib.BackwardFlatInterpolation
```

Step function that uses the value at the next node.

```python
x = [1.0, 2.0, 3.0]
y = [10.0, 20.0, 30.0]
interp = ql.BackwardFlatInterpolation(x, y)
interp(1.5)  # 20.0 (uses next node's value)
```

### CubicInterpolation

```{eval-rst}
.. autoclass:: pyquantlib.CubicInterpolation
```

Cubic spline interpolation with configurable derivative approximation and boundary conditions.

```python
x = [1.0, 2.0, 3.0, 4.0]
y = [1.0, 4.0, 9.0, 16.0]

# Default (Kruger derivative approximation)
interp = ql.CubicInterpolation(x, y)

# Natural spline (second derivative = 0 at boundaries)
interp = ql.CubicInterpolation(
    x, y,
    derivativeApprox=ql.CubicDerivativeApprox.Spline,
    leftCondition=ql.CubicBoundaryCondition.SecondDerivative,
    leftConditionValue=0.0,
    rightCondition=ql.CubicBoundaryCondition.SecondDerivative,
    rightConditionValue=0.0
)
```

### CubicNaturalSpline

```{eval-rst}
.. autoclass:: pyquantlib.CubicNaturalSpline
```

Convenience class for natural cubic spline (second derivative = 0 at boundaries).

### MonotonicCubicNaturalSpline

```{eval-rst}
.. autoclass:: pyquantlib.MonotonicCubicNaturalSpline
```

Monotonicity-preserving cubic spline that prevents oscillations.

### Enums

```{eval-rst}
.. autoclass:: pyquantlib.CubicDerivativeApprox
   :members:
   :undoc-members:

.. autoclass:: pyquantlib.CubicBoundaryCondition
   :members:
   :undoc-members:
```

### ForwardFlatInterpolation

```{eval-rst}
.. autoclass:: pyquantlib.ForwardFlatInterpolation
```

Step function that uses the current node's value (forward-flat).

```python
x = [1.0, 2.0, 3.0]
y = [10.0, 20.0, 30.0]
interp = ql.ForwardFlatInterpolation(x, y)
interp(1.5)  # 10.0 (uses current node's value)
```

### LagrangeInterpolation

```{eval-rst}
.. autoclass:: pyquantlib.LagrangeInterpolation
```

Lagrange polynomial interpolation. Supports evaluation with alternative y values via `value(y, x)`.

```python
x = [1.0, 2.0, 3.0]
y = [1.0, 4.0, 9.0]
interp = ql.LagrangeInterpolation(x, y)
interp(1.5)  # 2.25

# Evaluate with different y values
alt_y = ql.Array([1.0, 8.0, 27.0])
interp.value(alt_y, 2.0)  # 8.0
```

### BilinearInterpolation

```{eval-rst}
.. autoclass:: pyquantlib.BilinearInterpolation
```

Bilinear interpolation on a 2-D grid. Matrix z uses QuantLib convention: `z[y_idx][x_idx]`.

```python
x = [0.0, 1.0]
y = [0.0, 1.0]
z = ql.Matrix([[1.0, 2.0], [3.0, 4.0]])
interp = ql.BilinearInterpolation(x, y, z)
interp(0.5, 0.5)  # 2.5
```

### BicubicSpline

```{eval-rst}
.. autoclass:: pyquantlib.BicubicSpline
```

Bicubic spline interpolation on a 2-D grid with derivative methods.

```python
x = [0.0, 1.0, 2.0]
y = [0.0, 1.0, 2.0]
z = ql.Matrix([[0, 0, 0], [0, 1, 2], [0, 2, 4]])
interp = ql.BicubicSpline(x, y, z)
interp(1.0, 1.0)          # 1.0
interp.derivativeX(1, 1)   # ~1.0
```

### ChebyshevInterpolation

```{eval-rst}
.. autoclass:: pyquantlib.ChebyshevInterpolation

.. autoclass:: pyquantlib.ChebyshevPointsType
   :members:
   :undoc-members:
```

Chebyshev polynomial interpolation on [-1, 1].

```python
import math
interp = ql.ChebyshevInterpolation(20, math.sin)
interp(0.5)  # sin(0.5)
```

### RichardsonExtrapolation

```{eval-rst}
.. autoclass:: pyquantlib.RichardsonExtrapolation
```

Richardson extrapolation for improving convergence of numerical methods.

```python
f = lambda h: math.sin(h) / h
re = ql.RichardsonExtrapolation(f, 0.01, n=2.0)
re(2.0)  # ~1.0 (limit as h->0)
```

```{note}
The abstract base classes `Interpolation` and `Interpolation2D` are available in `pyquantlib.base` for type checking.
```

## Statistics

### Statistics

```{eval-rst}
.. autoclass:: pyquantlib.Statistics
```

General statistics accumulator with empirical-distribution risk measures, Gaussian-assumption analytics, and percentile/VaR/ES methods.

```python
stats = ql.Statistics()
stats.addSequence([1.0, 2.0, 3.0, 4.0, 5.0])
print(stats.mean(), stats.standardDeviation(), stats.skewness())
```

### IncrementalStatistics

```{eval-rst}
.. autoclass:: pyquantlib.IncrementalStatistics
```

Online (streaming) statistics via boost accumulators. Supports weighted observations.

```python
stats = ql.IncrementalStatistics()
stats.add(1.0, 1.0)
stats.add(2.0, 1.0)
print(stats.mean(), stats.weightSum())
```

### SequenceStatistics

```{eval-rst}
.. autoclass:: pyquantlib.SequenceStatistics
```

N-dimensional statistics with covariance and correlation matrices.

```python
stats = ql.SequenceStatistics(2)
stats.add([1.0, 2.0])
stats.add([3.0, 4.0])
print(stats.mean(), stats.covariance())
```

## Optimization

### EndCriteria

```{eval-rst}
.. autoclass:: pyquantlib.EndCriteria
```

### LevenbergMarquardt

```{eval-rst}
.. autoclass:: pyquantlib.LevenbergMarquardt
```

### Simplex

```{eval-rst}
.. autoclass:: pyquantlib.Simplex
```

Nelder-Mead simplex optimization method.

```python
optimizer = ql.Simplex(0.1)
```

### ConjugateGradient

```{eval-rst}
.. autoclass:: pyquantlib.ConjugateGradient
```

### SteepestDescent

```{eval-rst}
.. autoclass:: pyquantlib.SteepestDescent
```

### BFGS

```{eval-rst}
.. autoclass:: pyquantlib.BFGS
```

### DifferentialEvolution

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

Global optimizer using differential evolution. Configuration uses a builder pattern:

```python
config = ql.DEConfiguration()
config = config.withStepsizeWeight(0.5).withCrossoverProbability(0.9)
optimizer = ql.DifferentialEvolution(config)
```

### Problem

```{eval-rst}
.. autoclass:: pyquantlib.Problem
```

### Constraints

```{eval-rst}
.. autoclass:: pyquantlib.NoConstraint


.. autoclass:: pyquantlib.PositiveConstraint


.. autoclass:: pyquantlib.BoundaryConstraint


.. autoclass:: pyquantlib.CompositeConstraint

```

```{note}
Abstract base classes like `Constraint`, `OptimizationMethod`, and `CostFunction` are available in `pyquantlib.base` for subclassing.
```

## Distributions

### NormalDistribution

```{eval-rst}
.. autoclass:: pyquantlib.NormalDistribution
```

Normal (Gaussian) probability density function.

```python
pdf = ql.NormalDistribution()       # standard normal (mean=0, sigma=1)
pdf(0.0)                            # ~0.3989 (peak)
pdf.derivative(0.0)                 # 0.0 (at the peak)

pdf2 = ql.NormalDistribution(average=5.0, sigma=2.0)
```

### CumulativeNormalDistribution

```{eval-rst}
.. autoclass:: pyquantlib.CumulativeNormalDistribution
```

Cumulative distribution function of the normal distribution.

```python
cdf = ql.CumulativeNormalDistribution()
cdf(0.0)    # 0.5
cdf(1.96)   # ~0.975
```

### InverseCumulativeNormal

```{eval-rst}
.. autoclass:: pyquantlib.InverseCumulativeNormal
```

Inverse of the cumulative normal distribution (quantile function).

```python
inv = ql.InverseCumulativeNormal()
inv(0.5)    # 0.0
inv(0.975)  # ~1.96

# Static method for standard normal
ql.InverseCumulativeNormal.standard_value(0.975)  # ~1.96
```

### BivariateCumulativeNormalDistribution

```{eval-rst}
.. autoclass:: pyquantlib.BivariateCumulativeNormalDistribution
```

Cumulative bivariate normal distribution with given correlation.

```python
bvn = ql.BivariateCumulativeNormalDistribution(rho=0.5)
bvn(0.0, 0.0)  # P(X<=0, Y<=0) with correlation 0.5
```

## 1-D Solvers

Root-finding algorithms for one-dimensional functions.

### Brent

```{eval-rst}
.. autoclass:: pyquantlib.Brent
```

Brent's method combines bisection, secant, and inverse quadratic interpolation.

```python
solver = ql.Brent()
root = solver.solve(lambda x: x**2 - 4, 1e-10, 1.0, 0.0, 10.0)  # 2.0
```

### Bisection

```{eval-rst}
.. autoclass:: pyquantlib.Bisection
```

Simple bisection method. Robust but slower than Brent.

### Secant

```{eval-rst}
.. autoclass:: pyquantlib.Secant
```

Secant method. Faster convergence than bisection, does not require derivative.

### Newton

```{eval-rst}
.. autoclass:: pyquantlib.Newton
```

Newton-Raphson method. Requires a separate derivative function.

```python
solver = ql.Newton()
root = solver.solve(
    lambda x: x**2 - 4,       # f(x)
    lambda x: 2 * x,           # f'(x)
    1e-10, 1.0, 0.0, 10.0,
)
```

All solvers support two calling conventions:

```python
# Automatic bracketing (guess + step)
root = solver.solve(f, accuracy, guess, step)

# Explicit bracket
root = solver.solve(f, accuracy, guess, xMin, xMax)
```

Common methods: `setMaxEvaluations(n)`, `setLowerBound(x)`, `setUpperBound(x)`.

## ODE Solvers

### AdaptiveRungeKutta

```{eval-rst}
.. autoclass:: pyquantlib.AdaptiveRungeKutta
```

Adaptive step-size Runge-Kutta ODE integrator using the Cash-Karp method.

```python
rk = ql.AdaptiveRungeKutta(eps=1e-8)

# 1-D ODE: y' = f(x, y)
import math
result = rk.solve1d(lambda x, y: y, 1.0, 0.0, 1.0)  # y' = y => e
print(result)  # ~2.71828

# N-D ODE system: y' = F(x, y)
result = rk(lambda x, y: [y[1], -y[0]], [1.0, 0.0], 0.0, math.pi)
print(result)  # ~[-1, 0] (harmonic oscillator)
```
