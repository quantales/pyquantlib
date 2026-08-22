# Spread option: built-in vs pure-Python engine

Demonstrates the binding pattern for pure-Python pricing engines from `pyquantlib.extensions`. The same spread option is priced with the built-in `ql.KirkEngine` (C++) and `ModifiedKirkEngine` (pure Python, in `pyquantlib.extensions`). Both attach via `setPricingEngine()`.

## Code

```python
import pyquantlib as ql
from pyquantlib.extensions import ModifiedKirkEngine

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today = ql.Settings.evaluationDate
dc    = ql.Actual365Fixed()

# Two underlyings
spot1 = ql.SimpleQuote(100.0)
spot2 = ql.SimpleQuote(110.0)
rate  = ql.SimpleQuote(0.05)
div   = ql.SimpleQuote(0.0)
vol1  = ql.SimpleQuote(0.20)
vol2  = ql.SimpleQuote(0.25)

risk_free = ql.FlatForward(today, rate, dc)
dividend  = ql.FlatForward(today, div, dc)
v1 = ql.BlackConstantVol(today, ql.TARGET(), vol1, dc)
v2 = ql.BlackConstantVol(today, ql.TARGET(), vol2, dc)

p1 = ql.GeneralizedBlackScholesProcess(spot1, dividend, risk_free, v1)
p2 = ql.GeneralizedBlackScholesProcess(spot2, dividend, risk_free, v2)

# Instrument: 1Y call on (S1 - S2) with strike 5
payoff   = ql.SpreadBasketPayoff(ql.PlainVanillaPayoff(ql.Call, 5.0))
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
option   = ql.BasketOption(payoff, exercise)

correlation = 0.5

# Engine 1: built-in C++ Kirk approximation
kirk = ql.KirkEngine(p1, p2, correlation)
option.setPricingEngine(kirk)
print(f"Kirk           NPV: {option.NPV():.4f}")

# Engine 2: pure-Python Modified Kirk (Alos-Leon skew correction)
modified_kirk = ModifiedKirkEngine(p1, p2, correlation)
option.setPricingEngine(modified_kirk)
print(f"Modified Kirk  NPV: {option.NPV():.4f}")
```

## Output

```
Kirk           NPV: 3.8864
Modified Kirk  NPV: 3.8758
```

## Key points

- **`pyquantlib.extensions` ships pure-Python engines** that subclass C++ ABCs and plug into the same `setPricingEngine()` mechanism. From the option's perspective, there's no difference between a C++ engine and a Python one.
- **The Python engine subclasses `SpreadBlackScholesVanillaEngine`** from `pyquantlib.base`. The C++ base class extracts forwards, variances, strike, and discount factor from the instrument; the Python override receives them as `float` and returns a price. See {doc}`/extending`.
- **Same instrument, same processes.** `payoff`, `exercise`, `option`, `p1`, `p2` are unchanged across the two engines.

## Pitfalls

- **The engine must outlive the option.** As with any pricing engine, bind to a name before attaching: `engine = ModifiedKirkEngine(...); option.setPricingEngine(engine)`.

## See also

- {doc}`/extending`: writing custom engines in Python
- {doc}`/api/extensions`: full pure-Python extensions reference
- {doc}`compare-engines`: the same one-instrument-multiple-engines pattern with vanilla options
