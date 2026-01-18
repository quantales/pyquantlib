# NumPy Interoperability

Working with `ql.Array`, `ql.Matrix`, and NumPy.

```{note}
View the full notebook: [02_numpy_interoperability.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/02_numpy_interoperability.ipynb)
```

## Array Conversion

`ql.Array` accepts Python lists and numpy arrays:

```python
import pyquantlib as ql
import numpy as np

# From Python list
arr = ql.Array([1.0, 2.0, 3.0])

# From numpy array
arr = ql.Array(np.array([1.0, 2.0, 3.0]))

# Use in QuantLib functions
result = ql.DotProduct(ql.Array([1, 2, 3]), ql.Array([4, 5, 6]))
```

Convert back to numpy:

```python
arr = ql.Array([1.0, 2.0, 3.0])
np_arr = np.array(arr)  # Copy
np_view = np.array(arr, copy=False)  # Zero-copy view
```

## Matrix Conversion

`ql.Matrix` works similarly:

```python
# From numpy array
mat = ql.Matrix(np.array([[1, 2], [3, 4]], dtype=float))

# From list of lists
mat = ql.Matrix([[1.0, 0.5], [0.5, 1.0]])

# Convert to numpy
np_mat = np.array(mat)
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
strikes = np.array([80, 90, 100, 110, 120], dtype=float)
expiries = [ql.Date(15, 6, 2025) + ql.Period(f"{m}M") for m in [1, 3, 6, 12]]

# Volatility matrix (strikes x expiries)
vols = ql.Matrix([
    [0.25, 0.23, 0.21, 0.20],  # 80 strike
    [0.22, 0.21, 0.20, 0.19],  # 90 strike
    [0.20, 0.19, 0.18, 0.18],  # 100 strike (ATM)
    [0.21, 0.20, 0.19, 0.18],  # 110 strike
    [0.23, 0.22, 0.21, 0.20],  # 120 strike
])

# Create surface
surface = ql.BlackVarianceSurface(
    ref_date, calendar, expiries,
    ql.Array(strikes), vols, day_counter
)
```

Download the [full notebook](https://github.com/quantales/pyquantlib/blob/main/examples/02_numpy_interoperability.ipynb) for the complete example with visualization.

## See Also

- {doc}`/numpy` for detailed conversion reference
- {doc}`01_option_pricing` for basic PyQuantLib usage
