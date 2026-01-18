# Modified Kirk Engine

Spread option pricing with a custom Python engine.

```{note}
View the full notebook: [03_modified_kirk_engine.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/03_modified_kirk_engine.ipynb)
```

## Overview

This example demonstrates the `ModifiedKirkEngine` from `pyquantlib.extensions`: a pure Python pricing engine that improves Kirk's approximation for spread options.

The engine is implemented by subclassing `SpreadBlackScholesVanillaEngine`, showing how PyQuantLib enables rapid prototyping without C++ compilation.

## Background

Kirk's approximation (1995) is widely used for spread options but can be inaccurate when:
- Correlation between assets is high (ρ → 1)
- Strike is large relative to forward prices

The **Modified Kirk approximation** (Alòs & León, 2015) adds a volatility skew correction, significantly improving accuracy for high-correlation cases.

## Quick Example

```python
import pyquantlib as ql
from pyquantlib.extensions import ModifiedKirkEngine

# Setup
today = ql.Date(15, 1, 2025)
ql.Settings.instance().evaluationDate = today

# Processes for two assets
process1 = make_process(spot=100.0, vol=0.30)
process2 = make_process(spot=100.0, vol=0.20)

# Spread call option: max(S1 - S2 - K, 0)
payoff = ql.PlainVanillaPayoff(ql.Option.Call, 5.0)
spread_payoff = ql.SpreadBasketPayoff(payoff)
exercise = ql.EuropeanExercise(expiry)
option = ql.BasketOption(spread_payoff, exercise)

# Compare Kirk vs Modified Kirk
kirk_engine = ql.KirkEngine(process1, process2, rho=0.90)
option.setPricingEngine(kirk_engine)
print(f"Kirk: {option.NPV():.6f}")

mod_kirk_engine = ModifiedKirkEngine(process1, process2, correlation=0.90)
option.setPricingEngine(mod_kirk_engine)
print(f"Modified Kirk: {option.NPV():.6f}")
```

## How It Works

The `ModifiedKirkEngine` subclasses `SpreadBlackScholesVanillaEngine`:

```python
from pyquantlib.base import SpreadBlackScholesVanillaEngine

class ModifiedKirkEngine(SpreadBlackScholesVanillaEngine):
    def __init__(self, process1, process2, correlation):
        super().__init__(process1, process2, correlation)
        # Store parameters...
    
    def calculate(self):
        # Get instrument arguments
        args = self.getArguments()
        
        # Compute Modified Kirk price
        price = self._compute_price(...)
        
        # Set results
        results = self.getResults()
        results.value = price
```

## Reproducing Paper Results

The full notebook reproduces Figures 1-5 from Harutyunyan & Masip Borrás (2018), showing:
- Kirk's approximation error grows exponentially with correlation
- Modified Kirk remains stable even at ρ = 0.999
- Comparison against Monte Carlo benchmark

Download the [full notebook](https://github.com/quantales/pyquantlib/blob/main/examples/03_modified_kirk_engine.ipynb) for the complete analysis with visualizations.

## References

1. Kirk, E. (1995). "Correlation in the energy markets." Managing Energy Price Risk.
2. Alòs, E., & León, J.A. (2015). Quantitative Finance, 16(1), 31-42.
3. Harutyunyan & Masip Borrás (2018). arXiv:1812.04272

## See Also

- {doc}`/extending` for how to create custom engines
- {doc}`/api/extensions` for API reference
