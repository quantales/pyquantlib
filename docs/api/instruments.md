# Instruments Module

## Bonds

### Bond

```{eval-rst}
.. autoclass:: pyquantlib.Bond
   :members:
```

### ZeroCouponBond

```{eval-rst}
.. autoclass:: pyquantlib.ZeroCouponBond
```

```python
bond = ql.ZeroCouponBond(2, ql.TARGET(), 100.0, maturity_date)
bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))
print(bond.cleanPrice())
```

### FixedRateBond

```{eval-rst}
.. autoclass:: pyquantlib.FixedRateBond
```

```python
bond = ql.FixedRateBond(2, 100.0, schedule, [0.05],
                         ql.Thirty360(ql.Thirty360.BondBasis))
bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))
print(bond.cleanPrice())
print(bond.bondYield(ql.Thirty360(ql.Thirty360.BondBasis),
                      ql.Compounded, ql.Annual))
```

### FloatingRateBond

```{eval-rst}
.. autoclass:: pyquantlib.FloatingRateBond
```

```python
bond = ql.FloatingRateBond(2, 100.0, schedule, euribor6m,
                            ql.Actual360(), spreads=[0.005])
bond.setPricingEngine(ql.DiscountingBondEngine(curve_handle))
print(bond.cleanPrice())
```

## Swaps

### VanillaSwap

```{eval-rst}
.. autoclass:: pyquantlib.VanillaSwap
```

### OvernightIndexedSwap

```{eval-rst}
.. autoclass:: pyquantlib.OvernightIndexedSwap
```

Overnight indexed swap: fixed vs overnight floating leg.

```python
sofr = ql.Sofr(curve)
ois = ql.OvernightIndexedSwap(
    ql.SwapType.Receiver, 1_000_000.0, schedule,
    0.035, ql.Actual360(), sofr,
)
ois.setPricingEngine(ql.DiscountingSwapEngine(curve))
print(ois.NPV())
print(ois.fairRate())
```

## Caps, Floors, and Collars

### CapFloor

```{eval-rst}
.. autoclass:: pyquantlib.CapFloor
   :members:
```

### Cap

```{eval-rst}
.. autoclass:: pyquantlib.Cap
```

### Floor

```{eval-rst}
.. autoclass:: pyquantlib.Floor
```

### Collar

```{eval-rst}
.. autoclass:: pyquantlib.Collar
```

```python
leg = ql.IborLeg(schedule, euribor).withNotionals([1_000_000.0]).build()

cap = ql.Cap(leg, [0.05])
floor = ql.Floor(leg, [0.03])
collar = ql.Collar(leg, [0.05], [0.03])

cap.setPricingEngine(ql.BlackCapFloorEngine(curve, 0.20))
print(cap.NPV())
print(cap.impliedVolatility(cap.NPV(), curve_handle, 0.20))
```

## Forward Rate Agreement

### ForwardRateAgreement

```{eval-rst}
.. autoclass:: pyquantlib.ForwardRateAgreement
   :members:
```

```python
fra = ql.ForwardRateAgreement(
    euribor, value_date, ql.PositionType.Long,
    0.04, 1_000_000.0, curve,
)
print(fra.NPV())
print(fra.forwardRate())
```

## Options

### VanillaOption

```{eval-rst}
.. autoclass:: pyquantlib.VanillaOption
```

```python
payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
option = ql.VanillaOption(payoff, exercise)

option.setPricingEngine(engine)
print(f"NPV: {option.NPV():.4f}")
print(f"Delta: {option.delta():.4f}")
```

### BasketOption

```{eval-rst}
.. autoclass:: pyquantlib.BasketOption
```

## Payoffs

### PlainVanillaPayoff

```{eval-rst}
.. autoclass:: pyquantlib.PlainVanillaPayoff
```

| Type | Payoff |
|------|--------|
| `Call` | $\max(S - K, 0)$ |
| `Put` | $\max(K - S, 0)$ |

```python
call_payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
put_payoff = ql.PlainVanillaPayoff(ql.Put, 100.0)
```

### MinBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.MinBasketPayoff
```

### MaxBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.MaxBasketPayoff
```

### AverageBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.AverageBasketPayoff
```

### SpreadBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.SpreadBasketPayoff
```

## Exercise Types

### EuropeanExercise

```{eval-rst}
.. autoclass:: pyquantlib.EuropeanExercise
```

### AmericanExercise

```{eval-rst}
.. autoclass:: pyquantlib.AmericanExercise
```

### BermudanExercise

```{eval-rst}
.. autoclass:: pyquantlib.BermudanExercise
```

```python
european = ql.EuropeanExercise(expiry)
american = ql.AmericanExercise(today, expiry)
bermudan = ql.BermudanExercise([date1, date2, date3])
```
