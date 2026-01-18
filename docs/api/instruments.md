# Instruments Module

## Options

### VanillaOption

A standard European or American option on a single underlying.

```{eval-rst}
.. autoclass:: pyquantlib.VanillaOption
   :members:
   :undoc-members:
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

An option on a basket of underlyings.

```{eval-rst}
.. autoclass:: pyquantlib.BasketOption
   :members:
   :undoc-members:
```

## Payoffs

### PlainVanillaPayoff

Standard call/put payoff.

```{eval-rst}
.. autoclass:: pyquantlib.PlainVanillaPayoff
   :members:
   :undoc-members:
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
   :members:
```

### MaxBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.MaxBasketPayoff
   :members:
```

### AverageBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.AverageBasketPayoff
   :members:
```

### SpreadBasketPayoff

```{eval-rst}
.. autoclass:: pyquantlib.SpreadBasketPayoff
   :members:
```

## Exercise Types

### EuropeanExercise

Exercise only at expiration.

```{eval-rst}
.. autoclass:: pyquantlib.EuropeanExercise
   :members:
   :undoc-members:
```

### AmericanExercise

Exercise at any time up to expiration.

```{eval-rst}
.. autoclass:: pyquantlib.AmericanExercise
   :members:
   :undoc-members:
```

### BermudanExercise

Exercise on specific dates.

```{eval-rst}
.. autoclass:: pyquantlib.BermudanExercise
   :members:
   :undoc-members:
```

```python
european = ql.EuropeanExercise(expiry)
american = ql.AmericanExercise(today, expiry)
bermudan = ql.BermudanExercise([date1, date2, date3])
```
