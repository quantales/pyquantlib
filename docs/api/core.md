# Core Module

## Classes

### Settings

The global `Settings` singleton controls evaluation date and other global parameters.

```{eval-rst}
.. autoclass:: pyquantlib.Settings
   :members:
   :undoc-members:
```

```python
import pyquantlib as ql

settings = ql.Settings.instance()
settings.evaluationDate = ql.Date(15, 6, 2025)
today = settings.evaluationDate
```

### InterestRate

```{eval-rst}
.. autoclass:: pyquantlib.InterestRate
   :members:
   :undoc-members:
```

```python
rate = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
df = rate.discountFactor(1.0)
equivalent = rate.equivalentRate(ql.Continuous, ql.NoFrequency, 1.0)
```

### Rounding

```{eval-rst}
.. autoclass:: pyquantlib.Rounding
   :members:
   :undoc-members:

.. autoclass:: pyquantlib.UpRounding
   :members:

.. autoclass:: pyquantlib.DownRounding
   :members:

.. autoclass:: pyquantlib.ClosestRounding
   :members:

.. autoclass:: pyquantlib.CeilingTruncation
   :members:

.. autoclass:: pyquantlib.FloorTruncation
   :members:
```

## Enumerations

### Compounding

```{eval-rst}
.. autoclass:: pyquantlib.Compounding
   :members:
   :undoc-members:
```

| Value | Description |
|-------|-------------|
| `Simple` | $(1 + r \cdot t)$ |
| `Compounded` | $(1 + r/n)^{nt}$ |
| `Continuous` | $e^{rt}$ |
| `SimpleThenCompounded` | Simple for $t < 1/n$, then compounded |
| `CompoundedThenSimple` | Compounded for $t \geq 1/n$, then simple |

## Constants

| Constant | Description |
|----------|-------------|
| `ql.EPSILON` | Machine epsilon for floating point |
| `ql.NullReal` | Null value for Real (indicates "no value") |
| `ql.NullSize` | Null value for Size/Integer |
| `ql.MAX_REAL` | Maximum Real value |
| `ql.MIN_REAL` | Minimum Real value |
| `ql.MIN_POSITIVE_REAL` | Minimum positive Real value |
| `ql.MAX_INTEGER` | Maximum Integer value |
| `ql.MIN_INTEGER` | Minimum Integer value |

```python
if value == ql.NullReal:
    print("Value not available")
```
