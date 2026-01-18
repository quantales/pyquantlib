# Python Extensions

The `pyquantlib.extensions` module contains pure Python implementations that extend QuantLib's functionality.

```{seealso}
{doc}`/extending` for how to create custom extensions.
```

## Classes

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
```

```python
from pyquantlib.extensions import ModifiedKirkEngine

engine = ModifiedKirkEngine(process1, process2, correlation=0.95)
option.setPricingEngine(engine)
print(f"NPV: {option.NPV():.4f}")
```

#### Static Methods

```{eval-rst}
.. py:staticmethod:: ModifiedKirkEngine.kirk_volatility(F1, F2, K, sigma1, sigma2, rho)

   Calculate Kirk's approximation volatility (without skew correction).

.. py:staticmethod:: ModifiedKirkEngine.skew_slope(F1, F2, K, sigma1, sigma2, rho)

   Calculate the skew slope correction term from Alòs & León (2015).
```
