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

```{note}
Abstract base classes `CashFlow` and `Coupon` are available in `pyquantlib.base` for custom implementations.
```
