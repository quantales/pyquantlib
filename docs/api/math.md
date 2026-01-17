# Math Module

Arrays, matrices, and optimization.

## Array

```{eval-rst}
.. autoclass:: pyquantlib.Array
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql
import numpy as np

# Create from list
arr = ql.Array([1.0, 2.0, 3.0])

# Create with size and default value
arr = ql.Array(10, 0.0)

# NumPy interoperability (zero-copy view)
np_arr = np.array(arr, copy=False)
arr2 = ql.Array(np_arr)
```

### Automatic Conversion

Functions expecting `Array` accept Python lists and numpy arrays directly:

```python
# Both work identically
result = ql.DotProduct(ql.Array([1, 2, 3]), ql.Array([4, 5, 6]))
result = ql.DotProduct([1, 2, 3], [4, 5, 6])  # automatic conversion
```

## Matrix

```{eval-rst}
.. autoclass:: pyquantlib.Matrix
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql
import numpy as np

# Create a 3x3 identity matrix
mat = ql.Matrix(3, 3, 0.0)
mat[0, 0] = 1.0
mat[1, 1] = 1.0
mat[2, 2] = 1.0

# Create from numpy array
np_mat = np.array([[1, 2], [3, 4]], dtype=float)
mat = ql.Matrix(np_mat)

# Create from list of lists
mat = ql.Matrix([[1, 2], [3, 4]])

# NumPy interoperability (zero-copy view)
np_view = np.array(mat, copy=False)
```

## Optimization

### EndCriteria

```{eval-rst}
.. autoclass:: pyquantlib.EndCriteria
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

### Usage Example

```python
import pyquantlib as ql

# Define optimization problem
end_criteria = ql.EndCriteria(1000, 100, 1e-8, 1e-8, 1e-8)
optimizer = ql.LevenbergMarquardt()
constraint = ql.NoConstraint()

# Solve (requires custom CostFunction implementation from pyquantlib.base)
# from pyquantlib.base import CostFunction
# problem = ql.Problem(cost_function, constraint, initial_values)
# optimizer.minimize(problem, end_criteria)
```

```{note}
Abstract base classes like `Constraint`, `OptimizationMethod`, and `CostFunction` are available in `pyquantlib.base` for subclassing.
```
