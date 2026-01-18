# Cash Flows Module

## Classes

### SimpleCashFlow

A simple cash flow with a fixed amount and payment date.

```{eval-rst}
.. autoclass:: pyquantlib.SimpleCashFlow
   :members:
   :undoc-members:
```

```python
cf = ql.SimpleCashFlow(1000.0, ql.Date(15, 6, 2026))
print(cf.amount())  # 1000.0
print(cf.date())    # June 15th, 2026
```

### Redemption

A redemption (principal) cash flow.

```{eval-rst}
.. autoclass:: pyquantlib.Redemption
   :members:
   :undoc-members:
```

### AmortizingPayment

An amortizing payment cash flow.

```{eval-rst}
.. autoclass:: pyquantlib.AmortizingPayment
   :members:
   :undoc-members:
```

### FixedRateCoupon

A coupon with a fixed interest rate.

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateCoupon
   :members:
   :undoc-members:
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

Builder for a leg (sequence) of fixed rate coupons.

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateLeg
   :members:
   :undoc-members:
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
