# Cash Flows Module

## Classes

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

### setCouponPricer

```{eval-rst}
.. autofunction:: pyquantlib.setCouponPricer
```

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

```{note}
Abstract base classes `CashFlow`, `Coupon`, and `FloatingRateCouponPricer` are available in `pyquantlib.base` for custom implementations.
```
