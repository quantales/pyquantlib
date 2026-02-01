# Equity Option Pricing

Pricing European, Bermudan, and American options with multiple engines.

```{note}
View the full notebook: [03_equity_option.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/03_equity_option.ipynb)
```

This notebook replicates the QuantLib `EquityOption` example, demonstrating various pricing engines for vanilla options.

## Engines Covered

- **Analytic**: Black-Scholes, Heston, Bates, Black-Vasicek
- **Approximation**: Barone-Adesi-Whaley, Bjerksund-Stensland
- **Numerical**: Integral, Finite Differences, Binomial Trees
- **Monte Carlo**: European MC, American MC (Longstaff-Schwartz)

## Quick Preview

```python
import pyquantlib as ql

# Setup
calendar = ql.TARGET()
today = ql.Date(15, ql.May, 1998)
settlement = ql.Date(17, ql.May, 1998)
maturity = ql.Date(17, ql.May, 1999)
ql.Settings.instance().evaluationDate = today

# Option parameters
option_type = ql.OptionType.Put
underlying = 36.0
strike = 40.0
risk_free_rate = 0.06
volatility = 0.20

# Term structures
dc = ql.Actual365Fixed()
spot = ql.SimpleQuote(underlying)
flat_rate = ql.FlatForward(settlement, risk_free_rate, dc)
flat_div = ql.FlatForward(settlement, 0.0, dc)
flat_vol = ql.BlackConstantVol(settlement, calendar, volatility, dc)

# Black-Scholes-Merton process
bsm_process = ql.BlackScholesMertonProcess(spot, flat_div, flat_rate, flat_vol)

# Create options with different exercise styles
payoff = ql.PlainVanillaPayoff(option_type, strike)

european_option = ql.VanillaOption(payoff, ql.EuropeanExercise(maturity))
american_option = ql.VanillaOption(payoff, ql.AmericanExercise(settlement, maturity))

# Price with different engines
european_option.setPricingEngine(ql.AnalyticEuropeanEngine(bsm_process))
print(f"European (Black-Scholes): {european_option.NPV():.6f}")

american_option.setPricingEngine(ql.BaroneAdesiWhaleyApproximationEngine(bsm_process))
print(f"American (Barone-Adesi):  {american_option.NPV():.6f}")
```

Output:
```
European (Black-Scholes): 3.844308
American (Barone-Adesi):  4.459628
```

## Results Summary

The full notebook compares 18 different pricing methods:

| Method | European | Bermudan | American |
|--------|----------|----------|----------|
| Black-Scholes | 3.844308 | N/A | N/A |
| Finite differences | 3.844330 | 4.360765 | 4.486113 |
| Binomial Leisen-Reimer | 3.844308 | 4.360713 | 4.486076 |
| MC (Longstaff-Schwartz) | N/A | N/A | 4.456935 |

The early exercise premium makes American puts worth more than European puts.

Download the [full notebook](https://github.com/quantales/pyquantlib/blob/main/examples/03_equity_option.ipynb) to see all engines and results.
