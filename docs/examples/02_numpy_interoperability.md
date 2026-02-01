# NumPy Interoperability

Working with `ql.Array`, `ql.Matrix`, and NumPy.

```{note}
View the full notebook: [02_numpy_interoperability.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/02_numpy_interoperability.ipynb)
```

## Array Conversion

Functions expecting `Array` automatically accept Python lists and numpy arrays:

```python
import pyquantlib as ql
import numpy as np

# All three work identically
result1 = ql.DotProduct(ql.Array([1, 2, 3]), ql.Array([4, 5, 6]))  # Explicit
result2 = ql.DotProduct([1, 2, 3], [4, 5, 6])                      # List (auto-converted)
result3 = ql.DotProduct(np.array([1, 2, 3]), np.array([4, 5, 6]))  # NumPy (auto-converted)
```

Convert back to numpy:

```python
arr = ql.Array([1.0, 2.0, 3.0])
np_arr = np.array(arr)  # Copy
np_view = np.array(arr, copy=False)  # Zero-copy view
```

## Matrix Conversion

Functions expecting `Matrix` also accept list-of-lists and 2D numpy arrays:

```python
data = [[1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0]]

# All three work identically
result1 = ql.transpose(ql.Matrix(data))  # Explicit
result2 = ql.transpose(data)             # List (auto-converted)
result3 = ql.transpose(np.array(data))   # NumPy (auto-converted)
```

Explicit construction is still useful when creating Matrix objects:

```python
mat = ql.Matrix([[1.0, 0.5], [0.5, 1.0]])
np_mat = np.array(mat)  # Convert to numpy
```

## Zero-Copy Views

For performance-critical code, use zero-copy views:

```python
arr = ql.Array([1.0, 2.0, 3.0, 4.0, 5.0])
view = np.array(arr, copy=False)

# Modifications affect the original
view[0] = 99.0
print(arr[0])  # 99.0
```

```{warning}
The original `ql.Array` must stay alive while the view is in use.
```

## Practical Example: Volatility Surface

The full notebook demonstrates building a volatility surface from market data:

```python
# Strikes and expiries
strikes = [80, 90, 100, 110, 120]
expiries = [ql.Date(15, 6, 2025) + ql.Period(f"{m}M") for m in [1, 3, 6, 12]]

# Volatility matrix (strikes x expiries)
vols = [
    [0.25, 0.23, 0.21, 0.20],  # 80 strike
    [0.22, 0.21, 0.20, 0.19],  # 90 strike
    [0.20, 0.19, 0.18, 0.18],  # 100 strike (ATM)
    [0.21, 0.20, 0.19, 0.18],  # 110 strike
    [0.23, 0.22, 0.21, 0.20],  # 120 strike
]

# Create surface
surface = ql.BlackVarianceSurface(
    ref_date, calendar, expiries,
    strikes, ql.Matrix(vols), day_counter
)
```

Download the [full notebook](https://github.com/quantales/pyquantlib/blob/main/examples/02_numpy_interoperability.ipynb) for the complete example with visualization.

## See Also

- {doc}`/numpy` for detailed conversion reference
- {doc}`01_hello_pyquantlib` for basic PyQuantLib usage
