# Cash Flows Module

Cash flows, coupons, and leg construction.

## SimpleCashFlow

A simple cash flow with a fixed amount and payment date.

```{eval-rst}
.. autoclass:: pyquantlib.SimpleCashFlow
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

# Create a simple cash flow
payment_date = ql.Date(15, 6, 2026)
amount = 1000.0
cf = ql.SimpleCashFlow(amount, payment_date)

print(cf.amount())  # 1000.0
print(cf.date())    # June 15th, 2026
```

## Redemption

A redemption (principal) cash flow.

```{eval-rst}
.. autoclass:: pyquantlib.Redemption
   :members:
   :undoc-members:
```

## AmortizingPayment

An amortizing payment cash flow.

```{eval-rst}
.. autoclass:: pyquantlib.AmortizingPayment
   :members:
   :undoc-members:
```

## FixedRateCoupon

A coupon with a fixed interest rate.

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateCoupon
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

# Create a fixed rate coupon
payment_date = ql.Date(15, 6, 2026)
nominal = 1000000.0  # 1M notional
rate = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
accrual_start = ql.Date(15, 6, 2025)
accrual_end = ql.Date(15, 6, 2026)

coupon = ql.FixedRateCoupon(
    payment_date,
    nominal,
    rate.rate(),
    rate.dayCounter(),
    accrual_start,
    accrual_end
)

print(coupon.amount())      # Coupon payment amount
print(coupon.rate())        # 0.05
print(coupon.nominal())     # 1000000.0
print(coupon.accrualPeriod())  # Year fraction
```

## FixedRateLeg

Builder for a leg (sequence) of fixed rate coupons.

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateLeg
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

# Set evaluation date
today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today

# Create a schedule
schedule = ql.MakeSchedule() \
    .fromDate(today) \
    .to(today + ql.Period("5Y")) \
    .withFrequency(ql.Semiannual) \
    .withCalendar(ql.TARGET()) \
    .withConvention(ql.ModifiedFollowing) \
    .value()

# Build fixed rate leg
leg = ql.FixedRateLeg(schedule) \
    .withNotionals(1000000.0) \
    .withCouponRates(0.05, ql.Actual365Fixed()) \
    .build()

# leg is a list of cash flows
for cf in leg:
    print(f"{cf.date()}: {cf.amount():.2f}")
```

```{note}
Abstract base classes `CashFlow` and `Coupon` are available in `pyquantlib.base` for custom implementations.
```
