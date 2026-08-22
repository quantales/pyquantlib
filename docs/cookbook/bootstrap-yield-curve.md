# Bootstrap a yield curve

Demonstrates the binding pattern for building a discount curve from market quotes: rate helpers (`DepositRateHelper`, `SwapRateHelper`) feeding a `PiecewiseLogLinearDiscount` curve. The curve exposes `discount()`, `zeroRate()`, and `forwardRate()` once bootstrapping is done.

## Code

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today    = ql.Settings.evaluationDate
calendar = ql.TARGET()
dc       = ql.Actual360()

# Market quotes: short end as deposits, long end as par swaps.
deposits = [
    ("1W", 0.0410),
    ("1M", 0.0415),
    ("3M", 0.0425),
    ("6M", 0.0432),
]
swaps = [
    ("1Y", 0.0440),
    ("2Y", 0.0420),
    ("3Y", 0.0405),
    ("5Y", 0.0395),
    ("7Y", 0.0395),
    ("10Y", 0.0400),
    ("15Y", 0.0410),
    ("20Y", 0.0418),
    ("30Y", 0.0420),
]

# Helpers wrap each quote with the market conventions needed to price it.
helpers = []
for tenor, rate in deposits:
    helpers.append(ql.DepositRateHelper(
        rate, ql.Period(tenor),
        2, calendar, ql.ModifiedFollowing, False, dc,
    ))

ibor = ql.Euribor6M()
for tenor, rate in swaps:
    helpers.append(ql.SwapRateHelper(
        rate, ql.Period(tenor), calendar,
        ql.Annual, ql.Unadjusted,
        ql.Thirty360(ql.Thirty360.BondBasis),
        ibor,
    ))

# Bootstrapping happens lazily on first access. The curve is templated on
# (interpolation, what gets interpolated): here, log-linear on discount factors.
curve = ql.PiecewiseLogLinearDiscount(today, helpers, dc)
curve.enableExtrapolation()

# Inspect the bootstrapped curve.
print(f"{'Years':>6}{'DF':>10}{'Zero %':>10}{'1Y Fwd %':>11}")
print("-" * 37)
for years in [0.25, 0.5, 1, 2, 3, 5, 7, 10, 15, 20, 30]:
    d  = today + ql.Period(int(years * 12), ql.Months)
    df = curve.discount(d)
    z  = curve.zeroRate(d, dc, ql.Continuous, ql.Annual).rate()
    f  = curve.forwardRate(
        d, calendar.advance(d, 1, ql.Years),
        dc, ql.Continuous, ql.Annual,
    ).rate()
    print(f"{years:>6.2f}{df:>10.4f}{z*100:>9.3f}%{f*100:>10.3f}%")
```

## Output

```
 Years        DF    Zero %   1Y Fwd %
-------------------------------------
  0.25    0.9893    4.222%     4.158%
  0.50    0.9785    4.270%     4.044%
  1.00    0.9579    4.246%     3.864%
  2.00    0.9211    4.055%     3.597%
  3.00    0.8880    3.902%     3.669%
  5.00    0.8243    3.809%     3.815%
  7.00    0.7629    3.811%     4.001%
 10.00    0.6754    3.868%     4.215%
 15.00    0.5453    3.984%     4.384%
 20.00    0.4366    4.084%     4.133%
 30.00    0.2872    4.100%     4.130%
```

## Key points

- **Helpers carry the conventions, quotes carry the numbers.** A `DepositRateHelper(rate, tenor, fixingDays, calendar, convention, endOfMonth, dayCounter)` knows how to price a deposit given a curve. A `SwapRateHelper(rate, tenor, ..., iborIndex)` knows how to price a par swap. The curve solves for the discount factors that re-price every helper at par.
- **`PiecewiseLogLinearDiscount` is one of many `Piecewise*` variants.** The name encodes (interpolation, what's interpolated): `LinearZero`, `CubicZero`, `LogLinearDiscount`, `FlatForward`, etc. They all take the same constructor signature `(referenceDate, helpers, dayCounter)`. See {doc}`/api/termstructures` for the full list.
- **Bootstrapping is lazy.** The curve doesn't solve anything in the constructor; the first call to `discount()` / `zeroRate()` / `forwardRate()` triggers it. Subsequent calls are cached until any underlying quote changes.
- **The curve is observable.** Wrap it in a `RelinkableYieldTermStructureHandle` and downstream consumers (processes, engines) re-price automatically when a quote's value changes or the handle is relinked. See {doc}`scenario-analysis` for that pattern.

## Pitfalls

- **Helpers must be sorted by maturity, with no gaps.** The sequence above (1W → 6M deposits, then 1Y → 30Y swaps) is monotonic in pillar date, which the bootstrapper requires. Deposits past the first swap pillar, or swap tenors out of order, raise during bootstrap.
- **Mixing day-count conventions matters.** Deposits typically use Actual/360, swaps use 30/360 on the fixed leg. The curve's own day counter (the third constructor argument) is for *its* output (zero / forward rates the user reads back), not the helpers' inputs; each helper carries its own.
- **`enableExtrapolation()` is opt-in.** Without it, asking for a discount factor past the last pillar raises. With it, the curve flat-extrapolates the last forward rate. For risk and pricing, leave extrapolation disabled and let errors surface; for plotting and quick sanity checks, enable it.
- **Live quotes change the curve, but pillar dates are fixed at construction.** Bootstrapping is lazy, but pillar dates are derived from the helpers when the curve is built. Replacing the quotes with new values re-bootstraps; replacing the helpers requires rebuilding the curve.

## See also

- {doc}`/api/termstructures`: all `Piecewise*` variants and their interpolation choices
- {doc}`/concepts/term-structures`: how `YieldTermStructure` is wired into processes and engines
- {doc}`scenario-analysis`: relinking the curve under a `RelinkableYieldTermStructureHandle`
