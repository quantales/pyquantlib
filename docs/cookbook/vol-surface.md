# Build a Black vol surface from a quote grid

Demonstrates the binding pattern for constructing a `BlackVarianceSurface` from a 2D grid of (expiry, strike, vol) quotes and plugging it into a `GeneralizedBlackScholesProcess`. The same `setPricingEngine()` mechanism that uses a flat vol works unchanged with a smile-and-term-structure surface.

## Code

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today    = ql.Settings.evaluationDate
calendar = ql.TARGET()
dc       = ql.Actual365Fixed()

# 5 expiry pillars, 5 strike pillars.
expiries = [today + ql.Period(p) for p in ["1M", "3M", "6M", "1Y", "2Y"]]
strikes  = [80.0, 90.0, 100.0, 110.0, 120.0]

# Vol matrix: rows index strikes, columns index expiries.
# A skew (low strikes higher), flattening at longer expiries.
vols_data = [
    # 1M    3M    6M    1Y    2Y
    [0.30, 0.27, 0.26, 0.25, 0.24],   # K =  80
    [0.26, 0.24, 0.23, 0.22, 0.22],   # K =  90
    [0.22, 0.21, 0.21, 0.21, 0.21],   # K = 100
    [0.24, 0.23, 0.22, 0.22, 0.22],   # K = 110
    [0.28, 0.26, 0.24, 0.24, 0.23],   # K = 120
]

# QuantLib expects a ql.Matrix, populated cell by cell.
vol_mat = ql.Matrix(len(strikes), len(expiries))
for i, row in enumerate(vols_data):
    for j, v in enumerate(row):
        vol_mat[i, j] = v

surface = ql.BlackVarianceSurface(
    today, calendar, expiries, strikes, vol_mat, dc,
)
surface.enableExtrapolation()

# Pillar lookups round-trip the input (within the day-count convention).
print(f"{'Tenor':<6}{'K=80':>9}{'K=90':>9}{'K=100':>9}{'K=110':>9}{'K=120':>9}")
print("-" * 51)
for tenor_str in ["1M", "3M", "6M", "1Y", "2Y"]:
    d = today + ql.Period(tenor_str)
    row = [surface.blackVol(d, k) for k in strikes]
    print(f"{tenor_str:<6}" + "".join(f"{v:>9.4f}" for v in row))

# Off-grid queries are interpolated.
d = today + ql.Period("9M")
print(f"\n9M, K=95 (interpolated):  {surface.blackVol(d, 95.0):.4f}")

# Plug the surface into a process. It accepts the surface object directly
# (it is a BlackVolTermStructure), the same way it accepts a flat vol.
spot = ql.SimpleQuote(100.0)
rf   = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
dq   = ql.FlatForward(today, ql.SimpleQuote(0.0), dc)
process = ql.GeneralizedBlackScholesProcess(spot, dq, rf, surface)

# Price an OTM call: the engine pulls the right vol from the surface.
option = ql.VanillaOption(
    ql.PlainVanillaPayoff(ql.Call, 110.0),
    ql.EuropeanExercise(today + ql.Period("1Y")),
)
option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
print(f"1Y K=110 call NPV (smile-aware):  {option.NPV():.4f}")
```

## Output

```
Tenor      K=80     K=90    K=100    K=110    K=120
---------------------------------------------------
1M       0.3000   0.2600   0.2200   0.2400   0.2800
3M       0.2700   0.2400   0.2100   0.2300   0.2600
6M       0.2600   0.2300   0.2100   0.2200   0.2400
1Y       0.2500   0.2200   0.2100   0.2200   0.2400
2Y       0.2400   0.2200   0.2100   0.2200   0.2300

9M, K=95 (interpolated):  0.2168

1Y K=110 call NPV (smile-aware):  6.8330
```

## Key points

- **`BlackVarianceSurface` interpolates *variance*, not vol.** Internally the surface stores `T * sigma(K, T)^2` and interpolates linearly in time and (by default) bicubically in strike. Querying with `blackVol(date, strike)` divides back out by `sqrt(T)`. Storing variance keeps the interpolation arbitrage-free along the time axis (forward variance is non-negative); see {doc}`/api/termstructures` for the full set of vol structures.
- **The `ql.Matrix` shape is `(strikes, expiries)`.** Rows index strikes, columns index expiries. A column-major layout matches QuantLib's internal expectation.
- **A surface is a `BlackVolTermStructure`.** Process constructors accept it the same way they accept a flat `BlackConstantVol`. No special wiring is needed in the engine: `AnalyticEuropeanEngine` pulls `sigma(K, T)` for the option's strike and expiry transparently.
- **`enableExtrapolation()` is opt-in.** Without it, queries past the last expiry pillar or outside the strike range raise. The lower / upper extrapolation modes are configurable in the constructor's last two arguments.

## Pitfalls

- **Strikes and expiries must be sorted ascending.** Out-of-order entries are not detected at construction; the surface silently produces wrong values. Build the lists in order.
- **The surface stores its quotes by reference, not by value.** A `BlackVarianceSurface` does *not* observe `SimpleQuote` instances out of the box: the constructor takes a raw `Matrix`, not a matrix of `Quote` handles. Mutating the matrix after construction does not invalidate the cached interpolator. To get live updates, rebuild the surface (or use `BlackVarianceSurface` only as a snapshot and rebuild whenever quotes change).
- **Interpolation in time is on variance, in strike is on vol-by-default.** The default strike interpolator is `Bicubic` on vol; the time interpolator is linear on variance. For very short expiries the vol interpolation can produce small artifacts at the wings; set a tighter strike grid if those wings matter for the pricing target.

## See also

- {doc}`/api/termstructures`: full list of vol structures (`BlackConstantVol`, `BlackVarianceSurface`, `LocalVolSurface`, ...)
- {doc}`/concepts/term-structures`: how the surface plugs into `GeneralizedBlackScholesProcess`
- {doc}`bootstrap-yield-curve`: the discount-curve counterpart to this recipe
