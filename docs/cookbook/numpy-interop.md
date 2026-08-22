# NumPy interop

PyQuantLib bridges to NumPy through the buffer protocol on `ql.Array` and `ql.Matrix`. This recipe covers the two workflows that fall out of that:

1. **Building QuantLib inputs from NumPy.** Constructing a vol matrix, a covariance matrix, or an initial parameter vector in NumPy and handing it to QuantLib is much nicer than allocating a `ql.Matrix(rows, cols)` and assigning cells one by one.
2. **Pulling QuantLib outputs into NumPy.** Sampling a curve, scanning an option's NPV / delta over a spot grid, and similar workflows produce arrays of results that are easier to plot, slice, and combine in NumPy than as plain Python lists.

The boundary is at `Array` / `Matrix`: scalar QuantLib methods like `curve.discount(t)` or `option.NPV()` stay scalar. NumPy holds the inputs and outputs around a Python loop, rather than vectorising the C++ call. For a 9-point spot scan that overhead is invisible; for 100k repricings it is real and worth measuring.

## Code

```python
import pyquantlib as ql
import numpy as np

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today    = ql.Settings.evaluationDate
calendar = ql.TARGET()
dc       = ql.Actual365Fixed()

# 1. ndarray -> ql.Matrix (the binding copies into a fresh QuantLib buffer).
strikes      = np.array([80.0, 90.0, 100.0, 110.0, 120.0])
expiries_yrs = np.array([0.25, 0.5, 1.0, 2.0])

skew  = (strikes[:, None] - 100.0) ** 2 / 50000.0
term  = np.array([0.30, 0.27, 0.24, 0.22])
vols  = 0.20 + skew + (term[None, :] - 0.20) * 0.5
print(f"NumPy vol grid {vols.shape}:")
print(vols)

vol_mat = ql.Matrix(vols)
print(f"\nql.Matrix: rows={vol_mat.rows()}, cols={vol_mat.columns()}")

# 2. ql.Matrix -> ndarray. np.array() copies; np.asarray() shares memory.
back = np.array(vol_mat)
print(f"Round-trip exact: {np.allclose(back, vols)}")
print(f"np.array(ql.Matrix) owns its data:    {back.flags.owndata}")
print(f"np.asarray(ql.Matrix) owns its data:  {np.asarray(vol_mat).flags.owndata}")

# 3. ql.Array <-> ndarray
arr = ql.Array([1.0, 2.0, 3.0, 4.0, 5.0])
print(f"\nql.Array as ndarray: {np.array(arr)}")

a2 = ql.Array(np.linspace(0.0, 1.0, 6))
print(f"ql.Array from linspace: {np.array(a2)}")

# 4. Sample a curve onto a NumPy time grid.
curve = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
ts    = np.linspace(0.25, 5.0, 8)
dfs   = np.fromiter((curve.discount(t) for t in ts), dtype=float, count=len(ts))
print(f"\nTime grid (years): {ts}")
print(f"Discount factors:  {np.round(dfs, 4)}")

# 5. Spot scan: re-price across a NumPy spot grid.
# Build the option once, mutate the spot quote, collect NPVs.
spot = ql.SimpleQuote(100.0)
rf   = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
dq   = ql.FlatForward(today, ql.SimpleQuote(0.0), dc)
v    = ql.BlackConstantVol(today, calendar, ql.SimpleQuote(0.20), dc)
process = ql.GeneralizedBlackScholesProcess(spot, dq, rf, v)

option = ql.VanillaOption(
    ql.PlainVanillaPayoff(ql.Call, 100.0),
    ql.EuropeanExercise(today + ql.Period("1Y")),
)
option.setPricingEngine(ql.AnalyticEuropeanEngine(process))

spot_grid = np.linspace(80.0, 120.0, 9)
npvs   = np.empty_like(spot_grid)
deltas = np.empty_like(spot_grid)
for i, s in enumerate(spot_grid):
    spot.setValue(s)                # observer cascade triggers re-price
    npvs[i]   = option.NPV()
    deltas[i] = option.delta()

print(f"\nSpot scan:")
print(f"  Spot   : {spot_grid}")
print(f"  NPV    : {np.round(npvs, 4)}")
print(f"  Delta  : {np.round(deltas, 4)}")
```

## Output

```
NumPy vol grid (5, 4):
[[0.258 0.243 0.228 0.218]
 [0.252 0.237 0.222 0.212]
 [0.25  0.235 0.22  0.21 ]
 [0.252 0.237 0.222 0.212]
 [0.258 0.243 0.228 0.218]]

ql.Matrix: rows=5, cols=4
Round-trip exact: True
np.array(ql.Matrix) owns its data:    True
np.asarray(ql.Matrix) owns its data:  False

ql.Array as ndarray: [1. 2. 3. 4. 5.]
ql.Array from linspace: [0.  0.2 0.4 0.6 0.8 1. ]

Time grid (years): [0.25 0.93 1.61 2.29 2.96 3.64 4.32 5.  ]
Discount factors:  [0.9876 0.9546 0.9228 0.892  0.8622 0.8335 0.8057 0.7788]

Spot scan:
  Spot   : [ 80.  85.  90.  95. 100. 105. 110. 115. 120.]
  NPV    : [ 1.8594  3.2136  5.0912  7.5109 10.4506 13.8579 17.663  21.7905 26.169 ]
  Delta  : [0.2219 0.3218 0.4298 0.5373 0.6368 0.7237 0.7958 0.8529 0.8965]
```

## Key points

- **`ql.Array` and `ql.Matrix` implement the buffer protocol.** NumPy can read the underlying memory directly; the dtype is `float64` and the layout is row-major for `Matrix`. `np.asarray(qmat)` exploits the buffer to share memory (`owndata=False`); `np.array(qmat)` defaults to copying (`owndata=True`).
- **The reverse direction copies.** `ql.Matrix(np_2d_array)` and `ql.Array(np_1d_array)` accept any contiguous `float64` ndarray, but the binding copies the contents into a fresh QuantLib-owned buffer. Mutating the original ndarray afterwards has no effect on the QuantLib object.
- **The binding-level vectorisation stops at `Array` and `Matrix`.** Methods like `discount(t)`, `blackVol(date, strike)`, `forwardRate(d1, d2, ...)`, and `option.NPV()` are scalar in / scalar out. They cannot be vectorised at the C++ level without a different binding; the recipe's curve-sampling and spot-scan sections are Python loops with NumPy holding the inputs and outputs.
- **The spot-scan pattern is just observer cascade.** `spot.setValue(s)` invalidates the engine's cached NPV; the next `option.NPV()` re-prices through the engine. Greeks are read from the same cached state, so they come back at no extra cost on engines that compute them analytically.

## Pitfalls

- **The buffer is float64; integer ndarrays raise.** `ql.Matrix(np.eye(3, dtype=np.int32))` fails with a binding type error. Cast first: `ql.Matrix(np.eye(3).astype(float))`.
- **`np.asarray()` shares memory; `np.array()` copies.** With `np.asarray(qmat)`, mutating the ndarray mutates the underlying `Matrix` in C++; with `np.array(qmat)`, the result is an independent copy. Choose deliberately: shared views are cheaper but easy to mutate by accident.
- **Loop-based scans cross the Python / C++ boundary on every call.** For a 9-point spot scan, this is invisible. For 100k repricings (e.g., MC bumping), the overhead is real; pre-allocate output arrays as above (`np.empty_like(...)`) and avoid building per-iteration Python objects.
- **`ql.Array` does not support negative indexing.** `arr[-1]` raises a binding type error rather than returning the last element. Use `arr[len(arr) - 1]` or convert to ndarray first if pythonic indexing matters.
- **`option.delta()` is engine-specific.** `AnalyticEuropeanEngine` and FD engines expose it; many MC engines do not. The scan loop above will raise on engines that lack the requested Greek; check engine capability before plumbing it into a vectorised pipeline.

## See also

- {doc}`/numpy`: the full NumPy / pandas interop reference (which types convert, which copy)
- {doc}`/api/math`: `Array`, `Matrix`, and other linear-algebra primitives
- {doc}`scenario-analysis`: the same observer-cascade pattern for swapping entire term structures
