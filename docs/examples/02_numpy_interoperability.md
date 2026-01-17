# NumPy Interoperability

PyQuantLib integrates seamlessly with NumPy for numerical computing.

```{note}
See the full notebook: [02_numpy_interoperability.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/02_numpy_interoperability.ipynb)
```

## Topics Covered

1. **Array Conversion**: Automatic conversion from lists and numpy
2. **Matrix Conversion**: Explicit construction required
3. **Zero-Copy Views**: Performance with `copy=False`
4. **Practical Example**: Building a volatility surface from numpy data
5. **Performance Tips**: Benchmarks and best practices

## Quick Reference

| Type | Python → QuantLib | QuantLib → NumPy |
|------|-------------------|------------------|
| Array | Automatic (list, tuple, numpy) | `np.array(arr)` or `np.array(arr, copy=False)` |
| Matrix | Explicit `ql.Matrix(...)` | `np.array(mat)` or `np.array(mat, copy=False)` |

## Example: Array Conversion

```python
import pyquantlib as ql
import numpy as np

# All three work identically (auto-converted)
result = ql.DotProduct([1, 2, 3], [4, 5, 6])
result = ql.DotProduct(np.array([1, 2, 3]), np.array([4, 5, 6]))
result = ql.DotProduct(ql.Array([1, 2, 3]), ql.Array([4, 5, 6]))
```

## Example: Zero-Copy View

```python
arr = ql.Array([1.0, 2.0, 3.0])

# Copy (safe, independent data)
np_copy = np.array(arr)

# Zero-copy view (fast, shares memory)
np_view = np.array(arr, copy=False)
```

See also: {doc}`/numpy`
