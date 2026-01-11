# Instruments Module

Financial instruments: options, payoffs, and exercise types.

## Options

### VanillaOption

A standard European or American option on a single underlying.

```{eval-rst}
.. autoclass:: pyquantlib.VanillaOption
   :members:
   :undoc-members:
```

### BasketOption

An option on a basket of underlyings.

```{eval-rst}
.. autoclass:: pyquantlib.BasketOption
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today

# Create a European call option
payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)  # Call with K=100
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
option = ql.VanillaOption(payoff, exercise)

# Assign engine and price
option.setPricingEngine(engine)
print(f"NPV:   {option.NPV():.4f}")
print(f"Delta: {option.delta():.4f}")
print(f"Gamma: {option.gamma():.4f}")
print(f"Vega:  {option.vega():.4f}")
print(f"Theta: {option.theta():.4f}")
print(f"Rho:   {option.rho():.4f}")
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

### Option Type

Use `ql.Call` or `ql.Put` directly, or `ql.OptionType` enum:

```python
import pyquantlib as ql

# Direct usage
call_payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
put_payoff = ql.PlainVanillaPayoff(ql.Put, 100.0)

# Using OptionType enum
call_payoff = ql.PlainVanillaPayoff(ql.OptionType.Call, 100.0)
```

### Basket Payoffs

```{eval-rst}
.. autoclass:: pyquantlib.MinBasketPayoff
   :members:

.. autoclass:: pyquantlib.MaxBasketPayoff
   :members:

.. autoclass:: pyquantlib.AverageBasketPayoff
   :members:

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

### Usage

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)
expiry = today + ql.Period("1Y")

# European: exercise only at expiry
european = ql.EuropeanExercise(expiry)

# American: exercise anytime from today to expiry
american = ql.AmericanExercise(today, expiry)

# Bermudan: exercise on specific dates
dates = [today + ql.Period(f"{i}M") for i in range(3, 13, 3)]
bermudan = ql.BermudanExercise(dates)
```

## Instrument Workflow

1. Create payoff and exercise
2. Create instrument
3. Create pricing engine
4. Assign engine to instrument
5. Query results (NPV, Greeks)

```python
import pyquantlib as ql

# 1. Payoff and exercise
payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(ql.Date(15, 6, 2026))

# 2. Instrument
option = ql.VanillaOption(payoff, exercise)

# 3. Engine (requires process setup)
engine = ql.AnalyticEuropeanEngine(process)

# 4. Assign
option.setPricingEngine(engine)

# 5. Results
print(option.NPV())
print(option.delta())
```
