# Core Module

Settings, constants, interest rates, and fundamental types.

## Settings

The global `Settings` singleton controls evaluation date and other global parameters.

```{eval-rst}
.. autoclass:: pyquantlib.Settings
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

# Get the singleton instance
settings = ql.Settings.instance()

# Set evaluation date
settings.evaluationDate = ql.Date(15, 6, 2025)

# Read evaluation date
today = settings.evaluationDate
```

## InterestRate

```{eval-rst}
.. autoclass:: pyquantlib.InterestRate
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

# Create a 5% rate, annually compounded, Actual/365
rate = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)

# Compute discount factor for 1 year
df = rate.discountFactor(1.0)

# Compute compound factor
cf = rate.compoundFactor(1.0)

# Convert to equivalent rate with different compounding
equivalent = rate.equivalentRate(ql.Continuous, ql.NoFrequency, 1.0)
```

## Compounding

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

## Rounding

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

## Constants

Mathematical and financial constants available at the top level:

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

### Usage

```python
import pyquantlib as ql

# Check for null values
value = option.delta()
if value == ql.NullReal:
    print("Delta not available")

# Numerical limits
print(ql.EPSILON)      # Machine epsilon
print(ql.MAX_REAL)     # Max float value
```
