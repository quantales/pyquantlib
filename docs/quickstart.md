# Quick Start

This guide walks through a first PyQuantLib program: pricing a European call option using the Black-Scholes model.

```{note}
This guide assumes PyQuantLib is installed. See {doc}`installation` for setup instructions.
```

## Basic Usage

### Import and Setup

```python
import pyquantlib as ql

# Set the global evaluation date
today = ql.Date(15, 6, 2025)
ql.Settings.instance().evaluationDate = today
```

The evaluation date is a global setting that determines "today" for all pricing calculations. Always set this before creating term structures or pricing instruments.

### Market Data with Quotes

PyQuantLib uses `Quote` objects to represent market observables:

```python
# Create quotes for market data
spot = ql.SimpleQuote(100.0)    # Underlying price
rate = ql.SimpleQuote(0.05)     # Risk-free rate (5%)
vol = ql.SimpleQuote(0.20)      # Volatility (20%)
```

Quotes are observable: when a quote's value changes, any dependent calculations automatically update.

### Term Structures

Term structures describe how rates or volatilities vary over time:

```python
dc = ql.Actual365Fixed()  # Day counter for year fractions

# Flat risk-free rate curve
risk_free = ql.FlatForward(today, ql.QuoteHandle(rate), dc)

# Flat dividend yield curve
dividend = ql.FlatForward(today, 0.0, dc)

# Flat volatility surface
volatility = ql.BlackConstantVol(today, ql.TARGET(), ql.QuoteHandle(vol), dc)
```

Note the use of `QuoteHandle`: handles provide a layer of indirection that enables the observer pattern.

### The Black-Scholes Process

Combine market data into a stochastic process:

```python
process = ql.GeneralizedBlackScholesProcess(spot, dividend, risk_free, volatility)
```

That's it. PyQuantLib wraps the term structures in handles internally, providing a clean, Pythonic API.

```{note}
For advanced use cases requiring relinkable handles, explicit handle constructors are also available:

    process = ql.GeneralizedBlackScholesProcess(
        ql.QuoteHandle(spot),
        ql.YieldTermStructureHandle(dividend),
        ql.YieldTermStructureHandle(risk_free),
        ql.BlackVolTermStructureHandle(volatility),
    )
```

### Creating an Option

Define the option's payoff and exercise:

```python
# Call option with strike = 100
payoff = ql.PlainVanillaPayoff(ql.Call, 100.0)

# European exercise, 1 year to expiry
exercise = ql.EuropeanExercise(today + ql.Period("1Y"))

# Create the option instrument
option = ql.VanillaOption(payoff, exercise)
```

### Pricing with an Engine

Assign a pricing engine and compute results:

```python
# Use analytic Black-Scholes formula
engine = ql.AnalyticEuropeanEngine(process)
option.setPricingEngine(engine)

# Get results
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

## Responding to Market Changes

Because we used `Quote` objects, the option automatically reprices when market data changes:

```python
# Spot moves from 100 to 105
spot.setValue(105.0)
print(f"New NPV: {option.NPV():.4f}")  # Automatically updated

# Vol increases to 25%
vol.setValue(0.25)
print(f"New NPV: {option.NPV():.4f}")  # Updated again
```

## Module Organization

PyQuantLib exposes QuantLib classes in a flat namespace:

```python
import pyquantlib as ql

# Time
ql.Date, ql.Period, ql.Calendar, ql.Schedule, ql.DayCounter

# Market data
ql.SimpleQuote, ql.QuoteHandle

# Term structures
ql.FlatForward, ql.ZeroCurve, ql.BlackConstantVol, ql.BlackVarianceSurface

# Processes
ql.GeneralizedBlackScholesProcess, ql.HestonProcess

# Instruments
ql.VanillaOption, ql.BasketOption

# Pricing engines
ql.AnalyticEuropeanEngine, ql.MCEuropeanEngine, ql.AnalyticHestonEngine
```

### Abstract Base Classes

For subclassing QuantLib abstractions, import from `pyquantlib.base`:

```python
from pyquantlib.base import Observer, Observable, LazyObject
```

## Alternative Pricing Engines

### Monte Carlo

```python
# Monte Carlo with 100,000 paths
mc_engine = ql.MCEuropeanEngine(
    process,
    timeSteps=100,
    requiredSamples=100000,
    seed=42,
)
option.setPricingEngine(mc_engine)
print(f"MC NPV: {option.NPV():.4f}")
```

### Heston Stochastic Volatility

```python
# Heston model parameters
v0 = 0.04      # Initial variance
kappa = 1.0    # Mean reversion speed
theta = 0.04   # Long-term variance
sigma = 0.5    # Vol of vol
rho = -0.7     # Correlation

heston_process = ql.HestonProcess(
    risk_free, dividend, spot,
    v0, kappa, theta, sigma, rho,
)

heston_model = ql.HestonModel(heston_process)
heston_engine = ql.AnalyticHestonEngine(heston_model)

option.setPricingEngine(heston_engine)
print(f"Heston NPV: {option.NPV():.4f}")
```
