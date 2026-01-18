# NumPy Interoperability

PyQuantLib provides seamless integration with NumPy for numerical arrays and matrices.

## Implicit Conversion

Lists and numpy arrays can be passed directly to functions expecting `Array` or `Matrix`:

```python
import pyquantlib as ql
import numpy as np

# Lists work directly in functions
result = ql.DotProduct([1, 2, 3], [4, 5, 6])

# Numpy arrays work too
a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])
result = ql.DotProduct(a, b)

# Matrix functions accept list of lists or 2D numpy arrays
transposed = ql.transpose([[1, 2], [3, 4]])
```

`ql.Array` and `ql.Matrix` can also be constructed explicitly when needed.

## Array

`ql.Array` is a 1-dimensional array of real numbers.

### Python → QuantLib

```python
import pyquantlib as ql
import numpy as np

# Explicit construction from Python list
arr = ql.Array([1.0, 2.0, 3.0])

# Explicit construction from numpy array
arr = ql.Array(np.array([1.0, 2.0, 3.0]))

# Or pass directly (implicit conversion)
result = ql.DotProduct([1, 2, 3], [4, 5, 6])
```

### QuantLib → NumPy

Convert using `np.array()`:

```python
arr = ql.Array([1.0, 2.0, 3.0])

# Copy (safe, independent data)
np_arr = np.array(arr)

# Zero-copy view (fast, shares memory)
np_view = np.array(arr, copy=False)
```

```{warning}
Zero-copy views share memory with the original object. Modifying the view modifies the original, and the original must stay alive while the view is in use.
```

## Matrix

`ql.Matrix` is a 2-dimensional matrix of real numbers.

### Python → QuantLib

```python
# Explicit construction from numpy array
mat = ql.Matrix(np.array([[1, 2], [3, 4]], dtype=float))

# Explicit construction from list of lists
mat = ql.Matrix([[1, 2], [3, 4]])

# Or pass directly (implicit conversion)
transposed = ql.transpose([[1, 2], [3, 4]])
```

### QuantLib → NumPy

Convert using `np.array()`:

```python
mat = ql.Matrix([[1, 2], [3, 4]])

# Copy (safe, independent data)
np_arr = np.array(mat)

# Zero-copy view (fast, shares memory)
np_view = np.array(mat, copy=False)
```

### Row Access

Individual rows return numpy views:

```python
mat = ql.Matrix([[1, 2, 3], [4, 5, 6]])
row = mat[0]  # numpy array view of first row
```

## Summary

| Type | Python → QuantLib | QuantLib → NumPy |
|------|-------------------|------------------|
| Array | `ql.Array(list)` or `ql.Array(np_array)` | `np.array(arr)` or `np.array(arr, copy=False)` |
| Matrix | `ql.Matrix(list)` or `ql.Matrix(np_array)` | `np.array(mat)` or `np.array(mat, copy=False)` |

## Performance Tips

1. **Use zero-copy views** when reading data and the source object stays alive
2. **Use copies** when the source object may be modified or destroyed
3. **Pre-allocate matrices** with `ql.Matrix(rows, cols)` when building incrementally
