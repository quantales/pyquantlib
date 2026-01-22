# Python Extensions

The `pyquantlib.extensions` module contains pure Python implementations that extend QuantLib's functionality. These demonstrate how to prototype new features without C++ compilation.

```{seealso}
{doc}`/extending` for how to create custom extensions.
```

## Smile Sections

### SviSmileSection

```{eval-rst}
.. py:class:: pyquantlib.extensions.SviSmileSection(time_to_expiry, forward, svi_params, validate=True)

   Pure Python implementation of SVI smile section.

   This class demonstrates extending QuantLib in Python without C++ compilation.
   It can be validated against ``ql.SviSmileSection`` from QuantLib's experimental folder.

   :param time_to_expiry: Time to expiry in years
   :type time_to_expiry: float
   :param forward: Forward price
   :type forward: float
   :param svi_params: SVI parameters [a, b, sigma, rho, m]
   :type svi_params: list[float]
   :param validate: Whether to validate parameters (default True)
   :type validate: bool
```

```python
from pyquantlib.extensions import SviSmileSection

# Pure Python - same results as C++ ql.SviSmileSection
py_smile = SviSmileSection(1.0, 100.0, [0.04, 0.1, 0.3, -0.4, 0.0])
print(py_smile.volatility(100.0))

# Access parameters
print(py_smile.a, py_smile.b, py_smile.sigma, py_smile.rho, py_smile.m)
```

#### Helper Functions

```{eval-rst}
.. py:function:: pyquantlib.extensions.svi_total_variance(a, b, sigma, rho, m, k)

   Compute SVI total variance: a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))

.. py:function:: pyquantlib.extensions.check_svi_parameters(a, b, sigma, rho, m)

   Validate SVI parameters for no-arbitrage conditions. Raises ValueError if invalid.
```

## Pricing Engines

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
