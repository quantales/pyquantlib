# Math Module

```{seealso}
{doc}`/numpy` for detailed NumPy interoperability documentation.
```

## Classes

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

```{note}
The abstract base class `Interpolation` is available in `pyquantlib.base` for type checking.
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
