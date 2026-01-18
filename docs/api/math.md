# Math Module

```{seealso}
{doc}`/numpy` for detailed NumPy interoperability documentation.
```

## Classes

### Array

```{eval-rst}
.. autoclass:: pyquantlib.Array
   :members:
   :undoc-members:
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
   :members:
   :undoc-members:
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
   :members:
   :undoc-members:
```

### LevenbergMarquardt

```{eval-rst}
.. autoclass:: pyquantlib.LevenbergMarquardt
   :members:
   :undoc-members:
```

### Problem

```{eval-rst}
.. autoclass:: pyquantlib.Problem
   :members:
   :undoc-members:
```

### Constraints

```{eval-rst}
.. autoclass:: pyquantlib.NoConstraint
   :members:

.. autoclass:: pyquantlib.PositiveConstraint
   :members:

.. autoclass:: pyquantlib.BoundaryConstraint
   :members:

.. autoclass:: pyquantlib.CompositeConstraint
   :members:
```

```{note}
Abstract base classes like `Constraint`, `OptimizationMethod`, and `CostFunction` are available in `pyquantlib.base` for subclassing.
```
