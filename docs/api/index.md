# API Reference

This section provides documentation for PyQuantLib classes and functions.

```{seealso}
{doc}`/quickstart` for a tutorial, {doc}`/installation` for setup.
```

## Module Overview

PyQuantLib organizes QuantLib classes into logical groups:

- **Time**: Date arithmetic, calendars, day counters, schedules
- **Core**: Settings, constants, rounding, interest rates
- **Math**: Arrays, matrices, optimization
- **Quotes**: Market observables (spot, rates, vol)
- **Currencies**: Currency definitions and exchange rates
- **Cash Flows**: Coupon and cash flow implementations
- **Indexes**: Interest rate and other indexes
- **Term Structures**: Yield curves, volatility surfaces
- **Processes**: Stochastic processes (Black-Scholes, Heston)
- **Models**: Pricing models (Heston, etc.)
- **Instruments**: Financial instruments (options, etc.)
- **Pricing Engines**: Analytic, Monte Carlo, finite difference
- **Experimental**: Experimental QuantLib features (SVI, etc.)

## Import Conventions

Most classes are available directly from the top-level namespace:

```python
import pyquantlib as ql

# Use classes directly
date = ql.Date(15, 6, 2025)
calendar = ql.TARGET()
quote = ql.SimpleQuote(100.0)
```

### Abstract Base Classes

For subclassing, import from `pyquantlib.base`:

```python
from pyquantlib.base import (
    Observer,
    Observable,
    LazyObject,
    CashFlow,
    Coupon,
    PricingEngine,
    StochasticProcess,
    # ... etc
)
```

## Quick Reference

### Time

```{eval-rst}
.. currentmodule:: pyquantlib

.. autosummary::
   :nosignatures:

   Date
   Period
   Calendar
   Schedule
   DayCounter
   TimeUnit
   Weekday
   Month
   BusinessDayConvention
   DateGeneration
```

### Market Data

```{eval-rst}
.. autosummary::
   :nosignatures:

   SimpleQuote
   QuoteHandle
   RelinkableQuoteHandle
```

### Term Structures

```{eval-rst}
.. autosummary::
   :nosignatures:

   FlatForward
   YieldTermStructureHandle
   RelinkableYieldTermStructureHandle
   BlackConstantVol
   BlackVarianceSurface
   BlackVolTermStructureHandle
   RelinkableBlackVolTermStructureHandle
```

### Processes

```{eval-rst}
.. autosummary::
   :nosignatures:

   GeneralizedBlackScholesProcess
   BlackScholesProcess
   BlackScholesMertonProcess
   HestonProcess
```

### Instruments

```{eval-rst}
.. autosummary::
   :nosignatures:

   VanillaOption
   BasketOption
   PlainVanillaPayoff
   EuropeanExercise
   AmericanExercise
   BermudanExercise
```

### Pricing Engines

```{eval-rst}
.. autosummary::
   :nosignatures:

   AnalyticEuropeanEngine
   AnalyticHestonEngine
   BaroneAdesiWhaleyApproximationEngine
   BjerksundStenslandApproximationEngine
   BinomialVanillaEngine
   FdBlackScholesVanillaEngine
   MCEuropeanEngine
   MCAmericanEngine
   MCEuropeanBasketEngine
   Fd2dBlackScholesVanillaEngine
```

## Detailed Documentation

```{toctree}
:maxdepth: 2

time
core
math
quotes
currencies
cashflows
indexes
termstructures
processes
models
instruments
pricingengines
experimental
extensions
```

```{note}
API documentation is auto-generated from docstrings in the C++ bindings. Abstract base classes are available in `pyquantlib.base`.
```
