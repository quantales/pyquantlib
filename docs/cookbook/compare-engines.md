# One option, three engines

Demonstrates the binding pattern of swapping pricing engines on a single instrument. The same `VanillaOption` is priced with an analytic engine, a Monte Carlo engine, and a finite-difference engine via three `setPricingEngine()` calls.

## Code

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today = ql.Settings.evaluationDate
dc    = ql.Actual365Fixed()

# Market data and process
spot = ql.SimpleQuote(100.0)
rate = ql.SimpleQuote(0.05)
div  = ql.SimpleQuote(0.0)
vol  = ql.SimpleQuote(0.20)

risk_free  = ql.FlatForward(today, rate, dc)
dividend   = ql.FlatForward(today, div, dc)
volatility = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)
process    = ql.GeneralizedBlackScholesProcess(spot, dividend, risk_free, volatility)

# Instrument: 1Y at-the-money European call
payoff   = ql.PlainVanillaPayoff(ql.Call, 100.0)
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))
option   = ql.VanillaOption(payoff, exercise)

# Engine 1: analytic Black-Scholes
analytic = ql.AnalyticEuropeanEngine(process)
option.setPricingEngine(analytic)
print(f"Analytic   NPV: {option.NPV():.4f}   delta: {option.delta():.4f}")

# Engine 2: Monte Carlo (pseudo-random)
mc = ql.MCEuropeanEngine(
    process,
    "pseudorandom",
    timeSteps=100,
    requiredSamples=100_000,
    seed=42,
)
option.setPricingEngine(mc)
print(f"MC         NPV: {option.NPV():.4f}")

# Engine 3: finite difference
fd = ql.FdBlackScholesVanillaEngine(process, tGrid=100, xGrid=100)
option.setPricingEngine(fd)
print(f"FD         NPV: {option.NPV():.4f}   delta: {option.delta():.4f}")
```

## Output

```
Analytic   NPV: 10.4506   delta: 0.6368
MC         NPV: 10.4119
FD         NPV: 10.4569   delta: 0.6373
```

## Key points

- **The instrument is built once.** `payoff`, `exercise`, and `option` never change. Only the engine is swapped.
- **Each engine takes the same `process`.** `GeneralizedBlackScholesProcess` is the input to all three; the engine decides what to do with it.
- **`setPricingEngine()` discards the previous engine.** Calling it again replaces the binding without rebuilding the instrument.
- **Greeks availability differs by engine.** Analytic and FD expose `option.delta()` directly. The MC engine here doesn't (MC Greeks need bumping or pathwise sensitivities, via different engine constructors).

## Pitfalls

- **Engine objects must outlive the option.** When `setPricingEngine(...)` is called with an inline temporary, the engine can be garbage-collected before `NPV()` runs. Bind the engine to a name first (as above), then attach.
- **Wrong process for the engine.** `MCEuropeanEngine` expects a `GeneralizedBlackScholesProcess`. Other MC engines exist for other processes (e.g. `MCEuropeanHestonEngine` for `HestonProcess`). Mismatched constructors raise at engine construction.

## See also

- {doc}`/concepts/pricing-engines`: the instrument/engine separation explained
- {doc}`/api/pricingengines`: all engine bindings
- {doc}`mc-engine-kwargs`: deeper look at MC engine arguments
- {doc}`/troubleshooting`: "Tried to call pure virtual function" errors when an engine is collected too early
