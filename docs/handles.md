# QuantLib Handles

QuantLib uses handles extensively for term structures, quotes, and other market data. PyQuantLib provides both explicit handle usage and a simplified "hidden handles" API.

## What Are Handles?

A `Handle<T>` is a smart pointer that can be *relinked* to point to a different object. This enables lazy evaluation: when market data changes, all dependent calculations automatically update.

```python
import pyquantlib as ql

# Create a relinkable handle
rate_handle = ql.RelinkableQuoteHandle(ql.SimpleQuote(0.05))

# Use it in a term structure
curve = ql.FlatForward(ql.Date(15, 6, 2025), rate_handle, ql.Actual365Fixed())

# Later, relink to new data (curve automatically updates)
rate_handle.linkTo(ql.SimpleQuote(0.06))
```

## Hidden Handles (Pythonic API)

For simple use cases where relinking is not needed, PyQuantLib accepts raw objects directly and creates handles internally:

```python
# Hidden handles (simple)
spot = ql.SimpleQuote(100.0)
dividend = ql.FlatForward(today, 0.02, dc)
risk_free = ql.FlatForward(today, 0.05, dc)
volatility = ql.BlackConstantVol(today, calendar, 0.20, dc)

process = ql.GeneralizedBlackScholesProcess(
    spot, dividend, risk_free, volatility
)
```

Compared to explicit handles:

```python
# Explicit handles (verbose but relinkable)
spot_handle = ql.QuoteHandle(ql.SimpleQuote(100.0))
div_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.02, dc))
rf_handle = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, dc))
vol_handle = ql.BlackVolTermStructureHandle(
    ql.BlackConstantVol(today, calendar, 0.20, dc)
)

process = ql.GeneralizedBlackScholesProcess(
    spot_handle, div_handle, rf_handle, vol_handle
)
```

## Example: Option Pricing

### With Hidden Handles

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today

# Market data (raw objects)
spot = ql.SimpleQuote(100.0)
risk_free = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
dividend = ql.FlatForward(today, 0.02, ql.Actual365Fixed())
volatility = ql.BlackConstantVol(today, ql.TARGET(), 0.20, ql.Actual365Fixed())

# Process with hidden handles
process = ql.GeneralizedBlackScholesProcess(
    spot, dividend, risk_free, volatility
)

# Option
exercise = ql.EuropeanExercise(today + ql.Period(6, ql.Months))
payoff = ql.PlainVanillaPayoff(ql.Option.Call, 100.0)
option = ql.VanillaOption(payoff, exercise)

# Price
option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
print(f"NPV: {option.NPV():.4f}")
```

### With Relinkable Handles

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today

# Relinkable handles for market data
spot = ql.SimpleQuote(100.0)
spot_handle = ql.RelinkableQuoteHandle(spot)

rf_curve = ql.FlatForward(today, 0.05, ql.Actual365Fixed())
rf_handle = ql.RelinkableYieldTermStructureHandle(rf_curve)

div_curve = ql.FlatForward(today, 0.02, ql.Actual365Fixed())
div_handle = ql.RelinkableYieldTermStructureHandle(div_curve)

vol_surface = ql.BlackConstantVol(today, ql.TARGET(), 0.20, ql.Actual365Fixed())
vol_handle = ql.RelinkableBlackVolTermStructureHandle(vol_surface)

# Process with explicit handles
process = ql.GeneralizedBlackScholesProcess(
    spot_handle, div_handle, rf_handle, vol_handle
)

# Option setup (same as before)
exercise = ql.EuropeanExercise(today + ql.Period(6, ql.Months))
payoff = ql.PlainVanillaPayoff(ql.Option.Call, 100.0)
option = ql.VanillaOption(payoff, exercise)
option.setPricingEngine(ql.AnalyticEuropeanEngine(process))

# Initial price
print(f"NPV at spot=100: {option.NPV():.4f}")

# Update spot and reprice (no need to rebuild process or engine)
spot.setValue(105.0)
print(f"NPV at spot=105: {option.NPV():.4f}")

# Update volatility
vol_handle.linkTo(ql.BlackConstantVol(today, ql.TARGET(), 0.25, ql.Actual365Fixed()))
print(f"NPV at vol=25%: {option.NPV():.4f}")
```

## Summary

- **Hidden handles**: Simpler code, suitable for one-off pricing and simple scripts
- **Explicit handles**: Required when market data changes and dependent objects should auto-update
