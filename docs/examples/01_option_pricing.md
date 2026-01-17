# Hello PyQuantLib

European option pricing with Black-Scholes.

```{note}
View the full notebook: [01_option_pricing.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/01_option_pricing.ipynb)
```

PyQuantLib offers a cleaner API than QuantLib-Python (SWIG) with hidden handles: pass objects directly without wrapping in handles.

## Quick Preview

```python
import pyquantlib as ql

# Setup
today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today

# Market data
spot = ql.SimpleQuote(100.0)
rate = ql.SimpleQuote(0.05)
vol = ql.SimpleQuote(0.20)

# Term structures (pass quotes directly, handles created internally)
dc = ql.Actual365Fixed()
risk_free = ql.FlatForward(today, rate, dc)
dividend = ql.FlatForward(today, 0.0, dc)
volatility = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)

# Process (pass objects directly)
process = ql.GeneralizedBlackScholesProcess(spot, dividend, risk_free, volatility)

# Option
payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
option = ql.VanillaOption(payoff, exercise)

# Price
option.setPricingEngine(ql.AnalyticEuropeanEngine(process))

print(f"NPV:   {option.NPV():.4f}")
print(f"Delta: {option.delta():.4f}")
print(f"Gamma: {option.gamma():.4f}")
print(f"Vega:  {option.vega():.4f}")
print(f"Theta: {option.theta():.4f}")
```

Output:
```
NPV:   10.4506
Delta: 0.6368
Gamma: 0.0188
Vega:  37.5240
Theta: -6.4140
```

## Live Updates

Changing a quote triggers automatic repricing. This works seamlessly with hidden handles:

```python
spot.setValue(105.0)
print(option.NPV())  # Automatically updated
```

## Spot Ladder

The full notebook includes spot ladder visualization showing:
- Option value vs intrinsic value
- Delta convergence to 0/1 for deep OTM/ITM and Gamma peak at ATM

Download the [full notebook](https://github.com/quantales/pyquantlib/blob/main/examples/01_option_pricing.ipynb) to run the plots.
