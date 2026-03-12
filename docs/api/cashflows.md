# Cash Flows Module

## Cash Flows

### SimpleCashFlow

```{eval-rst}
.. autoclass:: pyquantlib.SimpleCashFlow
```

```python
cf = ql.SimpleCashFlow(1000.0, ql.Date(15, 6, 2026))
print(cf.amount())  # 1000.0
print(cf.date())    # June 15th, 2026
```

### Redemption

```{eval-rst}
.. autoclass:: pyquantlib.Redemption
```

### AmortizingPayment

```{eval-rst}
.. autoclass:: pyquantlib.AmortizingPayment
```

## Coupons

### FixedRateCoupon

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateCoupon
```

```python
coupon = ql.FixedRateCoupon(
    payment_date, nominal, rate, day_counter, accrual_start, accrual_end
)
print(coupon.amount())
print(coupon.rate())
```

### FloatingRateCoupon

```{eval-rst}
.. autoclass:: pyquantlib.FloatingRateCoupon
```

Base class for coupons paying a variable index-based rate.

```python
coupon = ql.FloatingRateCoupon(
    payment_date, nominal, start_date, end_date,
    fixingDays=2, index=euribor6m, gearing=1.0, spread=0.005
)
print(coupon.gearing())     # 1.0
print(coupon.spread())      # 0.005
print(coupon.fixingDate())
```

### IborCoupon

```{eval-rst}
.. autoclass:: pyquantlib.IborCoupon
```

Coupon paying a Libor-type index (e.g., Euribor, USD LIBOR).

```python
coupon = ql.IborCoupon(
    payment_date, 1e6, start_date, end_date,
    2, euribor6m
)
print(coupon.fixingDate())
print(coupon.fixingValueDate())
```

### OvernightIndexedCoupon

```{eval-rst}
.. autoclass:: pyquantlib.OvernightIndexedCoupon
```

Coupon paying the compounded (or simple average) daily overnight rate.

```python
coupon = ql.OvernightIndexedCoupon(
    payment_date, 10e6, start_date, end_date,
    overnight_index, spread=0.001,
    averagingMethod=ql.RateAveraging.Type.Compound
)
```

### CmsCoupon

```{eval-rst}
.. autoclass:: pyquantlib.CmsCoupon
```

Coupon paying a CMS (Constant Maturity Swap) rate.

```python
coupon = ql.CmsCoupon(
    payment_date, 1e6, start_date, end_date,
    2, swap_index
)
```

## Capped/Floored Coupons

### CappedFlooredCoupon

```{eval-rst}
.. autoclass:: pyquantlib.CappedFlooredCoupon
```

Wraps a floating-rate coupon with optional cap and/or floor. Use `None` for absent cap or floor.

```python
underlying = ql.IborCoupon(payment_date, 1e6, start, end, 2, euribor6m)
cf = ql.CappedFlooredCoupon(underlying, cap=0.05, floor=0.01)
print(cf.isCapped(), cf.isFloored())  # True True
print(cf.effectiveCap(), cf.effectiveFloor())
```

### CappedFlooredIborCoupon

```{eval-rst}
.. autoclass:: pyquantlib.CappedFlooredIborCoupon
```

Convenience class that builds a capped/floored Ibor coupon in a single constructor.

### CappedFlooredCmsCoupon

```{eval-rst}
.. autoclass:: pyquantlib.CappedFlooredCmsCoupon
```

Convenience class that builds a capped/floored CMS coupon in a single constructor.

## Digital Coupons

### DigitalCoupon

```{eval-rst}
.. autoclass:: pyquantlib.DigitalCoupon
```

Floating-rate coupon with embedded digital (binary) call and/or put option.

```python
dc = ql.DigitalCoupon(underlying, callStrike=0.04, putStrike=0.02)
print(dc.hasCall(), dc.hasPut(), dc.hasCollar())  # True True True
```

### DigitalIborCoupon

```{eval-rst}
.. autoclass:: pyquantlib.DigitalIborCoupon
```

Digital coupon specialized for Ibor underlyings.

### DigitalCmsCoupon

```{eval-rst}
.. autoclass:: pyquantlib.DigitalCmsCoupon
```

Digital coupon specialized for CMS underlyings.

### DigitalIborLeg

```{eval-rst}
.. autoclass:: pyquantlib.DigitalIborLeg
```

Fluent builder for a leg of digital Ibor coupons.

```python
leg = ql.DigitalIborLeg(schedule, euribor6m) \
    .withNotionals(1e6) \
    .withCallStrikes(0.04) \
    .withLongCallOption(ql.PositionType.Long) \
    .withReplication(ql.DigitalReplication()) \
    .build()
```

### DigitalCmsLeg

```{eval-rst}
.. autoclass:: pyquantlib.DigitalCmsLeg
```

Fluent builder for a leg of digital CMS coupons. Same API as `DigitalIborLeg` but takes a `SwapIndex`.

### ReplicationType

```{eval-rst}
.. autoclass:: pyquantlib.ReplicationType
   :members:
   :undoc-members:
```

| Value | Description |
|-------|-------------|
| `Sub` | Sub-replication (lower bound) |
| `Central` | Central replication |
| `Super` | Super-replication (upper bound) |

### DigitalReplication

```{eval-rst}
.. autoclass:: pyquantlib.DigitalReplication
```

Configuration for digital option replication strategy.

```python
repl = ql.DigitalReplication(ql.ReplicationType.Central, gap=1e-4)
```

## Coupon Pricers

### BlackIborCouponPricer

```{eval-rst}
.. autoclass:: pyquantlib.BlackIborCouponPricer
```

Black-formula pricer for Ibor coupons. Attach to a leg with `setCouponPricer`.

```python
pricer = ql.BlackIborCouponPricer()
ql.setCouponPricer(floating_leg, pricer)
```

### LinearTsrPricer

```{eval-rst}
.. autoclass:: pyquantlib.LinearTsrPricer
```

Linear Terminal Swap Rate pricer for CMS coupons.

```python
pricer = ql.LinearTsrPricer(swaption_vol, mean_reversion)
ql.setCouponPricer(cms_leg, pricer)
```

### LinearTsrPricerSettings

```{eval-rst}
.. autoclass:: pyquantlib.LinearTsrPricerSettings
```

### LinearTsrPricerStrategy

```{eval-rst}
.. autoclass:: pyquantlib.LinearTsrPricerStrategy
   :members:
   :undoc-members:
```

### YieldCurveModel

```{eval-rst}
.. autoclass:: pyquantlib.YieldCurveModel
   :members:
   :undoc-members:
```

| Value | Description |
|-------|-------------|
| `Standard` | Standard yield curve model |
| `ExactYield` | Exact yield model |
| `ParallelShifts` | Parallel shifts model |
| `NonParallelShifts` | Non-parallel shifts model |

### HaganPricer

```{eval-rst}
.. autoclass:: pyquantlib.HaganPricer
```

Abstract base class for Hagan-style CMS coupon pricers using static replication. Inherits from both `CmsCouponPricer` and `MeanRevertingPricer`.

### AnalyticHaganPricer

```{eval-rst}
.. autoclass:: pyquantlib.AnalyticHaganPricer
```

Analytic CMS coupon pricer based on the Hagan formula.

```python
pricer = ql.AnalyticHaganPricer(
    swaption_vol, ql.YieldCurveModel.Standard, mean_reversion
)
ql.setCouponPricer(cms_leg, pricer)
```

### NumericHaganPricer

```{eval-rst}
.. autoclass:: pyquantlib.NumericHaganPricer
```

Numeric CMS coupon pricer using Hagan integration with configurable limits.

```python
pricer = ql.NumericHaganPricer(
    swaption_vol, ql.YieldCurveModel.Standard, mean_reversion,
    lowerLimit=0.0, upperLimit=1.0, precision=1e-6
)
```

### CompoundingOvernightIndexedCouponPricer

```{eval-rst}
.. autoclass:: pyquantlib.CompoundingOvernightIndexedCouponPricer
```

Pricer for compounded overnight indexed coupons.

### ArithmeticAveragedOvernightIndexedCouponPricer

```{eval-rst}
.. autoclass:: pyquantlib.ArithmeticAveragedOvernightIndexedCouponPricer
```

Pricer for arithmetically averaged overnight indexed coupons with optional convexity adjustment.

```python
# Default (no convexity adjustment)
pricer = ql.ArithmeticAveragedOvernightIndexedCouponPricer()

# With convexity adjustment parameters
pricer = ql.ArithmeticAveragedOvernightIndexedCouponPricer(
    meanReversion=0.03, volatility=0.01, byApprox=False
)
```

### BlackCompoundingOvernightIndexedCouponPricer

```{eval-rst}
.. autoclass:: pyquantlib.BlackCompoundingOvernightIndexedCouponPricer
```

Black pricer for capped/floored compounded overnight coupons.

### BlackAveragingOvernightIndexedCouponPricer

```{eval-rst}
.. autoclass:: pyquantlib.BlackAveragingOvernightIndexedCouponPricer
```

Black pricer for capped/floored averaged overnight coupons. Requires `RateAveraging.Type.Simple`.

### setCouponPricer

```{eval-rst}
.. autofunction:: pyquantlib.setCouponPricer
```

Also accepts inflation coupon pricers for legs containing `YoYInflationCoupon` cashflows.

## Leg Builders

### FixedRateLeg

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateLeg
```

```python
leg = ql.FixedRateLeg(schedule) \
    .withNotionals(1000000.0) \
    .withCouponRates(0.05, ql.Actual365Fixed()) \
    .build()

for cf in leg:
    print(f"{cf.date()}: {cf.amount():.2f}")
```

### IborLeg

```{eval-rst}
.. autoclass:: pyquantlib.IborLeg
```

```python
leg = ql.IborLeg(schedule, euribor6m) \
    .withNotionals(1e6) \
    .withSpreads(0.005) \
    .build()
```

### OvernightLeg

```{eval-rst}
.. autoclass:: pyquantlib.OvernightLeg
```

```python
leg = ql.OvernightLeg(schedule, overnight_index) \
    .withNotionals(10e6) \
    .withSpreads(0.001) \
    .withAveragingMethod(ql.RateAveraging.Type.Compound) \
    .build()
```

### CmsLeg

```{eval-rst}
.. autoclass:: pyquantlib.CmsLeg
```

```python
leg = ql.CmsLeg(schedule, swap_index) \
    .withNotionals(1e6) \
    .withSpreads(0.001) \
    .build()
```

## BMA Coupons

### AverageBMACoupon

```{eval-rst}
.. autoclass:: pyquantlib.AverageBMACoupon
```

Coupon paying the weighted average of BMA fixings.

### AverageBMALeg

```{eval-rst}
.. autoclass:: pyquantlib.AverageBMALeg
```

Builder for a sequence of average BMA coupons.

```python
bma = ql.BMAIndex(curve)
leg = ql.AverageBMALeg(schedule, bma) \
    .withNotionals(1e6) \
    .leg()
```

## Settings

### IborCouponSettings

```{eval-rst}
.. autoclass:: pyquantlib.IborCouponSettings
```

Controls whether IborCoupons are created as par or indexed coupons.

```python
settings = ql.IborCouponSettings.instance()
settings.createAtParCoupons()    # default
settings.createIndexedCoupons()  # alternative
```

## Inflation Coupons

### InflationCoupon

```{eval-rst}
.. autoclass:: pyquantlib.base.InflationCoupon
   :members:
   :undoc-members:
```

Abstract base class for coupons linked to an inflation index.

### ZeroInflationCashFlow

```{eval-rst}
.. autoclass:: pyquantlib.ZeroInflationCashFlow
   :members:
   :undoc-members:
```

Cash flow paying the zero-inflation rate between two dates.

### YoYInflationCoupon

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationCoupon
   :members:
   :undoc-members:
```

Coupon paying the year-on-year inflation rate.

### CappedFlooredYoYInflationCoupon

```{eval-rst}
.. autoclass:: pyquantlib.CappedFlooredYoYInflationCoupon
   :members:
   :undoc-members:
```

Year-on-year inflation coupon with cap and/or floor.

### yoyInflationLeg

```{eval-rst}
.. autoclass:: pyquantlib.yoyInflationLeg
   :members:
   :undoc-members:
```

Builder class for constructing a leg of year-on-year inflation coupons.

```python
leg = ql.yoyInflationLeg(schedule, calendar, yoy_index, observation_lag) \
    .withNotionals(1_000_000.0) \
    .withPaymentDayCounter(ql.Actual365Fixed()) \
    .build()
```

## Inflation Coupon Pricers

### InflationCouponPricer

```{eval-rst}
.. autoclass:: pyquantlib.base.InflationCouponPricer
   :members:
   :undoc-members:
```

Abstract base class for inflation coupon pricers.

### YoYInflationCouponPricer

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationCouponPricer
   :members:
   :undoc-members:
```

Base pricer for year-on-year inflation coupons.

### BlackYoYInflationCouponPricer

```{eval-rst}
.. autoclass:: pyquantlib.BlackYoYInflationCouponPricer
   :members:
   :undoc-members:
```

Black-formula pricer for YoY inflation coupons (lognormal volatility).

### UnitDisplacedBlackYoYInflationCouponPricer

```{eval-rst}
.. autoclass:: pyquantlib.UnitDisplacedBlackYoYInflationCouponPricer
   :members:
   :undoc-members:
```

Unit-displaced Black-formula pricer for YoY inflation coupons.

### BachelierYoYInflationCouponPricer

```{eval-rst}
.. autoclass:: pyquantlib.BachelierYoYInflationCouponPricer
   :members:
   :undoc-members:
```

Bachelier (normal volatility) pricer for YoY inflation coupons.

```python
pricer = ql.BlackYoYInflationCouponPricer(yoy_vol_handle)
ql.setCouponPricer(yoy_leg, pricer)
```

## Dividends

### FixedDividend

```{eval-rst}
.. autoclass:: pyquantlib.FixedDividend
```

Fixed cash dividend.

```python
div = ql.FixedDividend(2.50, ql.Date(15, 6, 2026))
print(div.amount())  # 2.5
print(div.date())    # June 15th, 2026
```

### FractionalDividend

```{eval-rst}
.. autoclass:: pyquantlib.FractionalDividend
```

Fractional (proportional) dividend: amount = rate * nominal.

```python
div = ql.FractionalDividend(0.03, 100.0, ql.Date(15, 6, 2026))
print(div.rate())     # 0.03
print(div.nominal())  # 100.0
```

### DividendVector

```{eval-rst}
.. autofunction:: pyquantlib.DividendVector
```

Builds a sequence of fixed dividends from dates and amounts.

```python
divs = ql.DividendVector(
    [ql.Date(15, 6, 2026), ql.Date(15, 12, 2026)],
    [2.50, 2.50],
)
```

## Duration

### DurationType

```{eval-rst}
.. autoclass:: pyquantlib.DurationType
```

| Value | Description |
|-------|-------------|
| `Simple` | Simple duration |
| `Macaulay` | Macaulay duration |
| `Modified` | Modified duration |

```{note}
Abstract base classes `CashFlow`, `Coupon`, `FloatingRateCouponPricer`, `MeanRevertingPricer`, `CmsCouponPricer`, `HaganPricer`, `InflationCoupon`, and `InflationCouponPricer` are available in `pyquantlib.base` for `isinstance` checks and custom implementations.
```
