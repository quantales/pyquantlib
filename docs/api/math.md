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
