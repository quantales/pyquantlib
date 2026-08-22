# Piecewise curve from mixed instruments

Extends {doc}`bootstrap-yield-curve` to a more realistic setup: deposits at the short end, `FraRateHelper`s in the belly, swaps at the long end, all passed to a single `PiecewiseLogLinearDiscount`. The binding pattern is the same; the new piece is `FraRateHelper` and the pillar-ordering rules that govern how the helper types interleave.

## Code

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today    = ql.Settings.evaluationDate
calendar = ql.TARGET()
dc_dep   = ql.Actual360()
dc_swap  = ql.Thirty360(ql.Thirty360.BondBasis)

# Short end: deposits to 6M.
deposits = [
    ("1W", 0.0410),
    ("1M", 0.0415),
    ("3M", 0.0425),
    ("6M", 0.0432),
]

# Belly: FRAs against 6M Euribor. The first argument is months-to-start.
# A "3x9" FRA starts in 3M and ends in 9M (matching the 6M tenor of the index).
ibor = ql.Euribor6M()
fras = [
    (3,  0.0428),
    (6,  0.0435),
    (9,  0.0440),
    (12, 0.0445),
]

# Long end: par swaps from 2Y onwards.
swaps = [
    ("2Y", 0.0420),
    ("3Y", 0.0405),
    ("5Y", 0.0395),
    ("7Y", 0.0395),
    ("10Y", 0.0400),
    ("15Y", 0.0410),
    ("20Y", 0.0418),
    ("30Y", 0.0420),
]

helpers = []
for tenor, rate in deposits:
    helpers.append(ql.DepositRateHelper(
        rate, ql.Period(tenor),
        2, calendar, ql.ModifiedFollowing, False, dc_dep,
    ))

for months_to_start, rate in fras:
    helpers.append(ql.FraRateHelper(rate, months_to_start, ibor))

for tenor, rate in swaps:
    helpers.append(ql.SwapRateHelper(
        rate, ql.Period(tenor), calendar,
        ql.Annual, ql.Unadjusted, dc_swap, ibor,
    ))

curve = ql.PiecewiseLogLinearDiscount(today, helpers, dc_dep)
curve.enableExtrapolation()

print(f"{'Years':>6}{'DF':>10}{'Zero %':>10}{'Fwd 6M %':>11}")
print("-" * 37)
for years in [0.25, 0.5, 0.75, 1, 1.5, 2, 5, 10, 30]:
    d  = today + ql.Period(int(years * 12), ql.Months)
    df = curve.discount(d)
    z  = curve.zeroRate(d, dc_dep, ql.Continuous, ql.Annual).rate()
    f  = curve.forwardRate(
        d, calendar.advance(d, 6, ql.Months),
        dc_dep, ql.Continuous, ql.Annual,
    ).rate()
    print(f"{years:>6.2f}{df:>10.4f}{z*100:>9.3f}%{f*100:>10.3f}%")
```

## Output

```
 Years        DF    Zero %   Fwd 6M %
-------------------------------------
  0.25    0.9893    4.222%     4.236%
  0.50    0.9785    4.270%     4.301%
  0.75    0.9684    4.232%     4.350%
  1.00    0.9575    4.285%     4.399%
  1.50    0.9363    4.323%     3.254%
  2.00    0.9210    4.057%     3.589%
  5.00    0.8243    3.809%     3.813%
 10.00    0.6754    3.868%     4.213%
 30.00    0.2872    4.099%     4.130%
```

The 6M forward rate kink between 1Y and 2Y is the bootstrap reading the FRA pillars (last FRA ends at 18M, quoted at 4.45%) and then the 2Y par swap (4.20%): the curve has to make the forward rates jump down to land back on the swap. This is honest, not a bug, but it is a sign the input quotes are not arbitrage-consistent at the FRA / swap seam.

## Key points

- **`FraRateHelper(rate, monthsToStart, iborIndex)` is the FRA equivalent of a deposit helper.** The helper builds a forward-starting deposit on the given Ibor index: `monthsToStart=3` with a 6M Euribor index is a 3x9 FRA. The helper's pillar date is the FRA's end date.
- **All helper types feed the same `Piecewise*` curve.** The bootstrap algorithm does not care which helper class produced each pillar; it only sorts them by pillar date and solves for the discount factors that re-price each one at par.
- **The helpers' internal day counts are independent of the curve's.** Deposits typically use Actual/360, swaps use 30/360 on the fixed leg; the curve's day counter (third constructor argument) is for output only. Each helper carries its own.

## Pitfalls

- **Pillar dates must be strictly increasing across helper types.** If a deposit's maturity exceeds an FRA's start date or an FRA's end date overshoots a swap pillar, the bootstrap raises with a "two instruments have the same pillar date" or "non-monotonic pillar dates" error. Sketch the timeline before assembling.
- **`Pillar.Choice` matters when an FRA settles on a non-business day.** The default `Pillar.LastRelevantDate` uses the FRA's end date adjusted by the index's business-day convention. For unusual index conventions, either pin the pillar via `customPillarDate` or sanity-check `helper.pillarDate()` after construction.
- **A kink in forward rates between segments usually means input inconsistency.** Real markets quote FRAs and swaps off slightly different curves (single-curve assumption breaks down with collateralisation). For collateralised pricing, build the discount curve from OIS helpers and the projection curve from FRAs / swaps separately, then attach both to the index.

## See also

- {doc}`bootstrap-yield-curve`: the simpler deposits + swaps version
- {doc}`/api/termstructures`: all `Piecewise*` curve variants
- {doc}`/concepts/term-structures`: how a yield curve is wired into processes and engines
