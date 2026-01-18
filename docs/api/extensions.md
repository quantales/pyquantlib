# Python Extensions

The `pyquantlib.extensions` module contains pure Python implementations that extend QuantLib's functionality.

```{seealso}
{doc}`/extending` for how to create custom extensions.
```

## Available Extensions

### ModifiedKirkEngine

```{eval-rst}
.. py:class:: pyquantlib.extensions.ModifiedKirkEngine(process1, process2, correlation)

   Modified Kirk engine for spread option pricing.

   This engine implements the Modified Kirk approximation which adds a
   volatility skew correction to the standard Kirk formula. The correction
   is derived using Malliavin calculus and significantly improves accuracy
   when the correlation between the two underlying assets is high (ρ > 0.9).

   The spread option payoff is: max(S₁ - S₂ - K, 0) for a call.

   :param process1: Black-Scholes process for the first asset (S₁)
   :type process1: GeneralizedBlackScholesProcess
   :param process2: Black-Scholes process for the second asset (S₂)
   :type process2: GeneralizedBlackScholesProcess
   :param correlation: Correlation between the two assets, in [-1, 1]
   :type correlation: float

   **References:**

   - Alòs, E., & León, J.A. (2015). Quantitative Finance, 16(1), 31-42.
   - Kirk, E. (1995). "Correlation in the energy markets." Managing Energy Price Risk.

   **Example:**

   .. code-block:: python

      from pyquantlib.extensions import ModifiedKirkEngine

      engine = ModifiedKirkEngine(process1, process2, correlation=0.95)
      option.setPricingEngine(engine)
      print(f"NPV: {option.NPV():.4f}")
```

#### Static Methods

```{eval-rst}
.. py:staticmethod:: ModifiedKirkEngine.kirk_volatility(F1, F2, K, sigma1, sigma2, rho)

   Calculate Kirk's approximation volatility (without skew correction).

   :param F1: Forward price of asset 1
   :param F2: Forward price of asset 2
   :param K: Strike price
   :param sigma1: Volatility of asset 1
   :param sigma2: Volatility of asset 2
   :param rho: Correlation
   :return: Kirk's implied volatility
   :rtype: float
```

```{eval-rst}
.. py:staticmethod:: ModifiedKirkEngine.skew_slope(F1, F2, K, sigma1, sigma2, rho)

   Calculate the skew slope correction term from Alòs & León (2015).

   :param F1: Forward price of asset 1
   :param F2: Forward price of asset 2
   :param K: Strike price
   :param sigma1: Volatility of asset 1
   :param sigma2: Volatility of asset 2
   :param rho: Correlation
   :return: Skew slope correction
   :rtype: float
```

## Usage Example

```python
import pyquantlib as ql
from pyquantlib.extensions import ModifiedKirkEngine

# Setup
today = ql.Date(15, 1, 2025)
ql.Settings.instance().evaluationDate = today

dc = ql.Actual365Fixed()
cal = ql.NullCalendar()

# Create processes
def make_process(spot, vol):
    rate_ts = ql.FlatForward(today, 0.0, dc)
    div_ts = ql.FlatForward(today, 0.0, dc)
    vol_ts = ql.BlackConstantVol(today, cal, vol, dc)
    return ql.GeneralizedBlackScholesProcess(
        ql.SimpleQuote(spot), div_ts, rate_ts, vol_ts
    )

process1 = make_process(100.0, 0.30)
process2 = make_process(100.0, 0.20)

# Create spread option
maturity = today + ql.Period(6, ql.Months)
payoff = ql.PlainVanillaPayoff(ql.Option.Call, 5.0)
spread_payoff = ql.SpreadBasketPayoff(payoff)
exercise = ql.EuropeanExercise(maturity)
option = ql.BasketOption(spread_payoff, exercise)

# Compare engines
kirk_engine = ql.KirkEngine(process1, process2, 0.90)
option.setPricingEngine(kirk_engine)
kirk_price = option.NPV()

mod_kirk_engine = ModifiedKirkEngine(process1, process2, 0.90)
option.setPricingEngine(mod_kirk_engine)
mod_kirk_price = option.NPV()

print(f"Kirk:          {kirk_price:.6f}")
print(f"Modified Kirk: {mod_kirk_price:.6f}")
```

## Creating New Extensions

See {doc}`/extending` for a guide on creating custom Python extensions by subclassing QuantLib base classes.
