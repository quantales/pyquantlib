# Cash flows

Bindings for the cash-flow layer: bare `CashFlow` types, the coupon hierarchy (fixed, floating Ibor, overnight, CMS, capped / floored, digital, inflation), the fluent leg builders that materialise a `Leg` from a `Schedule`, the coupon pricers, and a few supporting enums and singletons.

## At a glance

| Family | Classes |
|---|---|
| Cash flows | {py:class}`pyquantlib.SimpleCashFlow`, {py:class}`pyquantlib.Redemption`, {py:class}`pyquantlib.AmortizingPayment` |
| Coupons | {py:class}`pyquantlib.FixedRateCoupon`, {py:class}`pyquantlib.FloatingRateCoupon`, {py:class}`pyquantlib.IborCoupon`, {py:class}`pyquantlib.OvernightIndexedCoupon`, {py:class}`pyquantlib.CmsCoupon` |
| Capped / floored | {py:class}`pyquantlib.CappedFlooredCoupon`, {py:class}`pyquantlib.CappedFlooredIborCoupon`, {py:class}`pyquantlib.CappedFlooredCmsCoupon` |
| Digital | {py:class}`pyquantlib.DigitalCoupon`, {py:class}`pyquantlib.DigitalIborCoupon`, {py:class}`pyquantlib.DigitalCmsCoupon`, {py:class}`pyquantlib.DigitalIborLeg`, {py:class}`pyquantlib.DigitalCmsLeg` |
| BMA | {py:class}`pyquantlib.AverageBMACoupon`, {py:class}`pyquantlib.AverageBMALeg` |
| Inflation | {py:class}`pyquantlib.ZeroInflationCashFlow`, {py:class}`pyquantlib.YoYInflationCoupon`, {py:class}`pyquantlib.CappedFlooredYoYInflationCoupon`, {py:class}`pyquantlib.yoyInflationLeg` |
| Dividends | {py:class}`pyquantlib.FixedDividend`, {py:class}`pyquantlib.FractionalDividend`, {py:func}`pyquantlib.DividendVector` |
| Leg builders | {py:class}`pyquantlib.FixedRateLeg`, {py:class}`pyquantlib.IborLeg`, {py:class}`pyquantlib.OvernightLeg`, {py:class}`pyquantlib.CmsLeg` |
| Coupon pricers (Ibor / OIS / CMS) | {py:class}`pyquantlib.BlackIborCouponPricer`, {py:class}`pyquantlib.CompoundingOvernightIndexedCouponPricer`, {py:class}`pyquantlib.ArithmeticAveragedOvernightIndexedCouponPricer`, {py:class}`pyquantlib.BlackCompoundingOvernightIndexedCouponPricer`, {py:class}`pyquantlib.BlackAveragingOvernightIndexedCouponPricer`, {py:class}`pyquantlib.LinearTsrPricer`, {py:class}`pyquantlib.AnalyticHaganPricer`, {py:class}`pyquantlib.NumericHaganPricer` |
| Coupon pricers (inflation) | {py:class}`pyquantlib.YoYInflationCouponPricer`, {py:class}`pyquantlib.BlackYoYInflationCouponPricer`, {py:class}`pyquantlib.UnitDisplacedBlackYoYInflationCouponPricer`, {py:class}`pyquantlib.BachelierYoYInflationCouponPricer` |
| Enums and singletons | {py:class}`pyquantlib.ReplicationType`, {py:class}`pyquantlib.DurationType`, {py:class}`pyquantlib.YieldCurveModel`, {py:class}`pyquantlib.LinearTsrPricerStrategy`, {py:class}`pyquantlib.IborCouponSettings` |

```{note}
Abstract bases `CashFlow`, `Coupon`, `FloatingRateCouponPricer`, `MeanRevertingPricer`, `CmsCouponPricer`, `HaganPricer`, `InflationCoupon`, and `InflationCouponPricer` live under `pyquantlib.base` for `isinstance` checks and custom subclassing.
```

## Common patterns

### Build a fixed-rate leg with the fluent builder

```python
import pyquantlib as ql

leg = (
    ql.FixedRateLeg(schedule)
      .withNotionals(1_000_000.0)
      .withCouponRates(0.05, ql.Actual365Fixed())
      .build()
)

for cf in leg:
    print(f"{cf.date()}: {cf.amount():.2f}")
```

The `*Leg` builders all share the same fluent shape: construct with the schedule (and index where applicable), chain `withNotionals`, `withSpreads`, `withGearings`, etc., terminate with `.build()` (or `.leg()` for `AverageBMALeg`).

### Build a floating-rate leg and attach a pricer

```python
floating = (
    ql.IborLeg(schedule, ql.Euribor6M(curve))
      .withNotionals(1e6)
      .withSpreads(0.005)
      .build()
)

pricer = ql.BlackIborCouponPricer()
ql.setCouponPricer(floating, pricer)
```

`setCouponPricer(leg, pricer)` walks the leg and sets the pricer on every coupon that needs one. The same function accepts inflation pricers for legs containing `YoYInflationCoupon`.

### Build a capped / floored Ibor coupon

```python
underlying = ql.IborCoupon(payment_date, 1e6, start, end, 2, euribor6m)
capped     = ql.CappedFlooredCoupon(underlying, cap=0.05, floor=0.01)

print(capped.isCapped(), capped.isFloored())
print(capped.effectiveCap(), capped.effectiveFloor())
```

`None` for either `cap` or `floor` removes the corresponding bound. `CappedFlooredIborCoupon` and `CappedFlooredCmsCoupon` are convenience constructors that build the underlying coupon and the cap / floor in one call.

### Build a year-on-year inflation leg

```python
leg = (
    ql.yoyInflationLeg(schedule, calendar, yoy_index, observation_lag)
      .withNotionals(1_000_000.0)
      .withPaymentDayCounter(ql.Actual365Fixed())
      .build()
)

pricer = ql.BlackYoYInflationCouponPricer(yoy_vol_handle)
ql.setCouponPricer(leg, pricer)
```

## Reference

### Cash flows

```{eval-rst}
.. autoclass:: pyquantlib.SimpleCashFlow
```

```python
cf = ql.SimpleCashFlow(1000.0, ql.Date(15, 6, 2026))
print(cf.amount())   # 1000.0
print(cf.date())
```

```{eval-rst}
.. autoclass:: pyquantlib.Redemption
```

```{eval-rst}
.. autoclass:: pyquantlib.AmortizingPayment
```

### Coupons

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateCoupon
```

```python
coupon = ql.FixedRateCoupon(
    payment_date, nominal, rate, day_counter, accrual_start, accrual_end,
)
print(coupon.amount(), coupon.rate())
```

```{eval-rst}
.. autoclass:: pyquantlib.FloatingRateCoupon
```

Base class for coupons paying a variable index-based rate. The optional `fixingConvention` argument (default `Preceding`) controls the business-day adjustment applied when rolling the fixing date to a valid business day. Accessible via `fixingConvention()`.

```python
coupon = ql.FloatingRateCoupon(
    payment_date, nominal, start_date, end_date,
    fixingDays=2, index=euribor6m, gearing=1.0, spread=0.005,
)
print(coupon.gearing(), coupon.spread(), coupon.fixingDate())
print(coupon.fixingConvention())   # BusinessDayConvention.Preceding
```

```{eval-rst}
.. autoclass:: pyquantlib.IborCoupon
```

```python
coupon = ql.IborCoupon(payment_date, 1e6, start_date, end_date, 2, euribor6m)
print(coupon.fixingDate(), coupon.fixingValueDate())
```

```{eval-rst}
.. autoclass:: pyquantlib.OvernightIndexedCoupon
```

```python
coupon = ql.OvernightIndexedCoupon(
    payment_date, 10e6, start_date, end_date,
    overnight_index, spread=0.001,
    averagingMethod=ql.RateAveraging.Type.Compound,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.CmsCoupon
```

```python
coupon = ql.CmsCoupon(
    payment_date, 1e6, start_date, end_date, 2, swap_index,
)
```

### Capped / floored coupons

```{eval-rst}
.. autoclass:: pyquantlib.CappedFlooredCoupon
```

```{eval-rst}
.. autoclass:: pyquantlib.CappedFlooredIborCoupon
```

```{eval-rst}
.. autoclass:: pyquantlib.CappedFlooredCmsCoupon
```

### Digital coupons

```{eval-rst}
.. autoclass:: pyquantlib.DigitalCoupon
```

```python
dc = ql.DigitalCoupon(underlying, callStrike=0.04, putStrike=0.02)
print(dc.hasCall(), dc.hasPut(), dc.hasCollar())
```

```{eval-rst}
.. autoclass:: pyquantlib.DigitalIborCoupon
```

```{eval-rst}
.. autoclass:: pyquantlib.DigitalCmsCoupon
```

```{eval-rst}
.. autoclass:: pyquantlib.DigitalIborLeg
```

```python
leg = (
    ql.DigitalIborLeg(schedule, euribor6m)
      .withNotionals(1e6)
      .withCallStrikes(0.04)
      .withLongCallOption(ql.PositionType.Long)
      .withReplication(ql.DigitalReplication())
      .build()
)
```

```{eval-rst}
.. autoclass:: pyquantlib.DigitalCmsLeg
```

```{eval-rst}
.. autoclass:: pyquantlib.ReplicationType
   :members:
   :undoc-members:
```

| Value | Replication |
|---|---|
| `Sub` | Sub-replication (lower bound) |
| `Central` | Central replication |
| `Super` | Super-replication (upper bound) |

```{eval-rst}
.. autoclass:: pyquantlib.DigitalReplication
```

```python
repl = ql.DigitalReplication(ql.ReplicationType.Central, gap=1e-4)
```

### Coupon pricers

```{eval-rst}
.. autoclass:: pyquantlib.BlackIborCouponPricer
```

```{eval-rst}
.. autoclass:: pyquantlib.LinearTsrPricer
```

```{eval-rst}
.. autoclass:: pyquantlib.LinearTsrPricerSettings
```

```{eval-rst}
.. autoclass:: pyquantlib.LinearTsrPricerStrategy
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.YieldCurveModel
   :members:
   :undoc-members:
```

| Value | Yield-curve model |
|---|---|
| `Standard` | Standard |
| `ExactYield` | Exact-yield |
| `ParallelShifts` | Parallel shifts |
| `NonParallelShifts` | Non-parallel shifts |

```{eval-rst}
.. autoclass:: pyquantlib.HaganPricer
```

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticHaganPricer
```

```python
pricer = ql.AnalyticHaganPricer(
    swaption_vol, ql.YieldCurveModel.Standard, mean_reversion,
)
ql.setCouponPricer(cms_leg, pricer)
```

```{eval-rst}
.. autoclass:: pyquantlib.NumericHaganPricer
```

```python
pricer = ql.NumericHaganPricer(
    swaption_vol, ql.YieldCurveModel.Standard, mean_reversion,
    lowerLimit=0.0, upperLimit=1.0, precision=1e-6,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.CompoundingOvernightIndexedCouponPricer
```

```{eval-rst}
.. autoclass:: pyquantlib.ArithmeticAveragedOvernightIndexedCouponPricer
```

```python
# Default (no convexity adjustment)
pricer = ql.ArithmeticAveragedOvernightIndexedCouponPricer()

# With convexity adjustment parameters
pricer = ql.ArithmeticAveragedOvernightIndexedCouponPricer(
    meanReversion=0.03, volatility=0.01, byApprox=False,
)
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackCompoundingOvernightIndexedCouponPricer
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackAveragingOvernightIndexedCouponPricer
```

Requires `RateAveraging.Type.Simple` on the underlying coupon.

```{eval-rst}
.. autofunction:: pyquantlib.setCouponPricer
```

Accepts inflation pricers for legs containing `YoYInflationCoupon` cash flows.

### Leg builders

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateLeg
```

```{eval-rst}
.. autoclass:: pyquantlib.IborLeg
```

```python
leg = (
    ql.IborLeg(schedule, euribor6m)
      .withNotionals(1e6)
      .withSpreads(0.005)
      .build()
)
```

```{eval-rst}
.. autoclass:: pyquantlib.OvernightLeg
```

```python
leg = (
    ql.OvernightLeg(schedule, overnight_index)
      .withNotionals(10e6)
      .withSpreads(0.001)
      .withAveragingMethod(ql.RateAveraging.Type.Compound)
      .build()
)
```

```{eval-rst}
.. autoclass:: pyquantlib.CmsLeg
```

```python
leg = (
    ql.CmsLeg(schedule, swap_index)
      .withNotionals(1e6)
      .withSpreads(0.001)
      .build()
)
```

### BMA coupons

```{eval-rst}
.. autoclass:: pyquantlib.AverageBMACoupon
```

```{eval-rst}
.. autoclass:: pyquantlib.AverageBMALeg
```

```python
bma = ql.BMAIndex(curve)
leg = (
    ql.AverageBMALeg(schedule, bma)
      .withNotionals(1e6)
      .leg()
)
```

### Settings

```{eval-rst}
.. autoclass:: pyquantlib.IborCouponSettings
```

```python
settings = ql.IborCouponSettings.instance()
settings.createAtParCoupons()    # default
settings.createIndexedCoupons()  # alternative
```

### Inflation coupons

```{eval-rst}
.. autoclass:: pyquantlib.base.InflationCoupon
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.ZeroInflationCashFlow
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationCoupon
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.CappedFlooredYoYInflationCoupon
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.yoyInflationLeg
   :members:
   :undoc-members:
```

### Inflation coupon pricers

```{eval-rst}
.. autoclass:: pyquantlib.base.InflationCouponPricer
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationCouponPricer
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.BlackYoYInflationCouponPricer
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.UnitDisplacedBlackYoYInflationCouponPricer
   :members:
   :undoc-members:
```

```{eval-rst}
.. autoclass:: pyquantlib.BachelierYoYInflationCouponPricer
   :members:
   :undoc-members:
```

### Dividends

```{eval-rst}
.. autoclass:: pyquantlib.FixedDividend
```

```python
div = ql.FixedDividend(2.50, ql.Date(15, 6, 2026))
print(div.amount(), div.date())
```

```{eval-rst}
.. autoclass:: pyquantlib.FractionalDividend
```

Amount equals `rate * nominal`.

```python
div = ql.FractionalDividend(0.03, 100.0, ql.Date(15, 6, 2026))
print(div.rate(), div.nominal())
```

```{eval-rst}
.. autofunction:: pyquantlib.DividendVector
```

```python
divs = ql.DividendVector(
    [ql.Date(15, 6, 2026), ql.Date(15, 12, 2026)],
    [2.50, 2.50],
)
```

### Duration

```{eval-rst}
.. autoclass:: pyquantlib.DurationType
```

| Value | Duration |
|---|---|
| `Simple` | Simple |
| `Macaulay` | Macaulay |
| `Modified` | Modified |

## See also

- {doc}`indexes`: indices that drive floating, OIS, CMS, and inflation coupons
- {doc}`instruments`: bonds and swaps that consume legs
- {doc}`termstructures`: vol surfaces consumed by the Black / Bachelier coupon pricers
