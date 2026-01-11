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

# Create from list
arr = ql.Array([1.0, 2.0, 3.0])

# Create with size and default value
arr = ql.Array(10, 0.0)

# NumPy interoperability
import numpy as np
np_arr = np.array(arr)
arr2 = ql.Array(np_arr)
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

# Create a 3x3 matrix
mat = ql.Matrix(3, 3, 0.0)

# Set values
mat[0][0] = 1.0
mat[1][1] = 1.0
mat[2][2] = 1.0

# NumPy interoperability
import numpy as np
np_mat = np.array(mat)
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
