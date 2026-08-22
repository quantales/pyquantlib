# Python Extensions

Bindings for `pyquantlib.extensions`: pure-Python classes that subclass C++ ABCs and plug into the same `setPricingEngine()` / smile-section / etc. mechanisms as the built-in C++ types. They serve two roles: ship genuinely new functionality without a C++ recompile (e.g. the `ModifiedKirkEngine` skew correction), and demonstrate the trampoline pattern for users writing their own extensions.

## At a glance

| Class | Role |
|---|---|
| {py:class}`pyquantlib.extensions.SviSmileSection` | Pure-Python SVI smile section. Same arithmetic as `ql.SviSmileSection` but driven by Python parameter logic, useful as a reference and as a starting point for custom smiles. |
| {py:class}`pyquantlib.extensions.ModifiedKirkEngine` | Spread-option engine adding the Alos-Leon skew correction on top of Kirk. Plugs into `BasketOption.setPricingEngine()` like a C++ engine. |

Both classes are subclasses of QuantLib C++ ABCs. The trampoline rules apply: override the numeric `*Impl` methods (`calculate(f1, f2, ...)`, not the no-arg `calculate()`); never accept C++ object handles as override parameters. See {doc}`/extending` for how to write a new extension class on the same pattern.

## Common patterns

### Use `ModifiedKirkEngine` like any other engine

```python
import pyquantlib as ql
from pyquantlib.extensions import ModifiedKirkEngine

engine = ModifiedKirkEngine(process1, process2, correlation=0.95)
option.setPricingEngine(engine)
print(f"NPV: {option.NPV():.4f}")
```

From the option's perspective there is no difference between a C++ engine and a Python one. Bind the engine to a name before attaching: a Python engine that gets garbage-collected during pricing will trigger a "tried to call pure virtual function" error. See {doc}`/cookbook/spread-option-engines` for the side-by-side comparison with the built-in `KirkEngine`.

### Build an SVI smile section in Python

```python
from pyquantlib.extensions import SviSmileSection

smile = SviSmileSection(
    time_to_expiry=1.0,
    forward=100.0,
    svi_params=[0.04, 0.1, 0.3, -0.4, 0.0],
)
print(smile.volatility(100.0))
print(smile.a, smile.b, smile.sigma, smile.rho, smile.m)
```

Parameters are stored as Python attributes, so they can be inspected, copied, and modified directly. The class can be validated against the C++ `ql.SviSmileSection` from QuantLib's experimental folder by constructing both with the same parameters and comparing `volatility(K)` over a strike grid.

## Reference

### Smile sections

```{eval-rst}
.. py:class:: pyquantlib.extensions.SviSmileSection(time_to_expiry, forward, svi_params, validate=True)

   Pure-Python implementation of an SVI smile section.

   :param time_to_expiry: Time to expiry in years.
   :type time_to_expiry: float
   :param forward: Forward price.
   :type forward: float
   :param svi_params: SVI parameters ``[a, b, sigma, rho, m]``.
   :type svi_params: list[float]
   :param validate: Whether to validate parameters at construction. Default ``True``.
   :type validate: bool
```

**Helper functions**

```{eval-rst}
.. py:function:: pyquantlib.extensions.svi_total_variance(a, b, sigma, rho, m, k)

   Compute SVI total variance: ``a + b * (rho * (k - m) + sqrt((k - m)^2 + sigma^2))``.

.. py:function:: pyquantlib.extensions.check_svi_parameters(a, b, sigma, rho, m)

   Validate SVI parameters for no-arbitrage conditions. Raises ``ValueError`` if invalid.
```

### Pricing engines

```{eval-rst}
.. py:class:: pyquantlib.extensions.ModifiedKirkEngine(process1, process2, correlation)

   Modified Kirk engine for spread-option pricing. Adds a Malliavin-calculus skew correction
   on top of the standard Kirk approximation. The correction matters when the assets'
   correlation is high (``rho > 0.9``); for low correlations the result is close to plain
   Kirk.

   The spread payoff is ``max(S1 - S2 - K, 0)`` for a call.

   :param process1: Black-Scholes process for the first asset.
   :type process1: GeneralizedBlackScholesProcess
   :param process2: Black-Scholes process for the second asset.
   :type process2: GeneralizedBlackScholesProcess
   :param correlation: Correlation between the two assets, in ``[-1, 1]``.
   :type correlation: float

   **References**

   - Alos, E. and Leon, J.A. (2015). *Quantitative Finance*, 16(1), 31-42.
   - Kirk, E. (1995). "Correlation in the energy markets." *Managing Energy Price Risk.*
```

**Static methods**

```{eval-rst}
.. py:staticmethod:: ModifiedKirkEngine.kirk_volatility(F1, F2, K, sigma1, sigma2, rho)

   Plain Kirk approximation volatility (no skew correction).

.. py:staticmethod:: ModifiedKirkEngine.skew_slope(F1, F2, K, sigma1, sigma2, rho)

   Skew-slope correction term from Alos and Leon (2015).
```

## See also

- {doc}`/extending`: walkthrough of writing a custom extension class on the same trampoline pattern
- {doc}`/cookbook/spread-option-engines`: built-in `KirkEngine` (C++) vs `ModifiedKirkEngine` (Python) on the same instrument
