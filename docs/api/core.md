# Core Module

## Settings

### Settings

Global repository for run-time library settings.

`ql.Settings` is exported as the singleton instance, allowing direct property access.

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `evaluationDate` | `Date` | The evaluation date for pricing calculations |
| `includeReferenceDateEvents` | `bool` | Whether events on the reference date are included |
| `includeTodaysCashFlows` | `bool` or `None` | Whether to include today's cash flows |
| `enforcesTodaysHistoricFixings` | `bool` | Whether to enforce historic fixings for today |

#### Methods

| Method | Description |
|--------|-------------|
| `instance()` | Returns the singleton instance |
| `setEvaluationDate(date)` | Sets the evaluation date |
| `anchorEvaluationDate()` | Prevents the evaluation date from advancing automatically |
| `resetEvaluationDate()` | Resets evaluation date to today and allows automatic advancement |

#### Example

```python
import pyquantlib as ql

# Set evaluation date
ql.Settings.evaluationDate = ql.Date(15, 6, 2025)

# Anchor the date (prevents automatic advancement)
ql.Settings.anchorEvaluationDate()

# Configure cash flow settings
ql.Settings.includeReferenceDateEvents = True
ql.Settings.includeTodaysCashFlows = True
ql.Settings.enforcesTodaysHistoricFixings = False

# Reset to today with automatic advancement
ql.Settings.resetEvaluationDate()
```

```{tip}
Both `ql.Settings.evaluationDate` and `ql.Settings.instance().evaluationDate` work identically.
```

## Interest Rate

### InterestRate

```{eval-rst}
.. autoclass:: pyquantlib.InterestRate
```

```python
rate = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)
df = rate.discountFactor(1.0)
equivalent = rate.equivalentRate(ql.Continuous, ql.NoFrequency, 1.0)
```

## Rounding

### Rounding

```{eval-rst}
.. autoclass:: pyquantlib.Rounding
```

### UpRounding

```{eval-rst}
.. autoclass:: pyquantlib.UpRounding
```

### DownRounding

```{eval-rst}
.. autoclass:: pyquantlib.DownRounding
```

### ClosestRounding

```{eval-rst}
.. autoclass:: pyquantlib.ClosestRounding
```

### CeilingTruncation

```{eval-rst}
.. autoclass:: pyquantlib.CeilingTruncation
```

### FloorTruncation

```{eval-rst}
.. autoclass:: pyquantlib.FloorTruncation
```

## Enumerations

```{eval-rst}
.. autoclass:: pyquantlib.Compounding
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
