# Core

Bindings for the small set of process-wide primitives every PyQuantLib script touches: the `Settings` singleton, `InterestRate` for compounding conversions, the `Rounding` family, and a handful of enums and numeric sentinels.

## At a glance

| Class | Role |
|---|---|
| {py:class}`pyquantlib.Settings` | Process-wide singleton. Holds the evaluation date and a few cash-flow flags. The first thing most scripts touch. |
| {py:class}`pyquantlib.InterestRate` | A `(rate, day-count, compounding, frequency)` quadruple. Converts between compounding conventions and computes discount factors. |
| {py:class}`pyquantlib.Rounding` (and variants) | Money-rounding rules used by `Currency` and `Money`. |
| {py:class}`pyquantlib.Compounding` | Enum: `Simple`, `Compounded`, `Continuous`, `SimpleThenCompounded`, `CompoundedThenSimple`. |
| {py:class}`pyquantlib.PositionType` | Enum: `Long`, `Short`. |
| {py:class}`pyquantlib.ProtectionSide` | Enum: `Buyer`, `Seller`. |

`ql.Settings` is exported as the live singleton instance. Both `ql.Settings.evaluationDate` and `ql.Settings.instance().evaluationDate` work and refer to the same state.

## Common patterns

### Pin the evaluation date at the top of the script

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
```

The evaluation date drives every calendar lookup, every term-structure default reference date, and every fixing query. Setting it once at the top of a script (or at the start of a function that does pricing) is the standard idiom.

### Anchor the date during a long-running calculation

```python
ql.Settings.anchorEvaluationDate()
# ... long sweep that must not cross a midnight boundary ...
ql.Settings.resetEvaluationDate()
```

By default the evaluation date can advance with the wall clock; anchoring locks it. Useful in scenario sweeps and overnight jobs.

### Convert between compounding conventions

```python
rate = ql.InterestRate(0.05, ql.Actual365Fixed(), ql.Compounded, ql.Annual)

df  = rate.discountFactor(1.0)                            # 0.95238...
eq  = rate.equivalentRate(ql.Continuous, ql.NoFrequency, 1.0)
print(eq.rate())                                          # ~0.04879
```

`InterestRate` is a value type. The `equivalentRate` returns a fresh `InterestRate` in the requested compounding; the original is unchanged.

## Reference

### Settings

`ql.Settings` is the singleton process-wide configuration.

**Properties**

| Property | Type | Description |
|---|---|---|
| `evaluationDate` | `Date` | The reference date used by everything that looks up market data or schedules. |
| `includeReferenceDateEvents` | `bool` | Whether events on the reference date count as future events. |
| `includeTodaysCashFlows` | `bool` or `None` | Whether today's cash flows show up in pricing. `None` defers to per-instrument defaults. |
| `enforcesTodaysHistoricFixings` | `bool` | Whether index fixings for today are required to come from history rather than being forecast. |

**Methods**

| Method | Description |
|---|---|
| `instance()` | Returns the singleton (same object as the `ql.Settings` module attribute). |
| `setEvaluationDate(date)` | Equivalent to assigning to `evaluationDate`. |
| `anchorEvaluationDate()` | Pins the evaluation date so it does not drift with the system clock. |
| `resetEvaluationDate()` | Resets to today and re-enables automatic advancement. |

### Interest rates

```{eval-rst}
.. autoclass:: pyquantlib.InterestRate
```

### Rounding

```{eval-rst}
.. autoclass:: pyquantlib.Rounding
```

```{eval-rst}
.. autoclass:: pyquantlib.UpRounding
```

```{eval-rst}
.. autoclass:: pyquantlib.DownRounding
```

```{eval-rst}
.. autoclass:: pyquantlib.ClosestRounding
```

```{eval-rst}
.. autoclass:: pyquantlib.CeilingTruncation
```

```{eval-rst}
.. autoclass:: pyquantlib.FloorTruncation
```

### Enumerations

```{eval-rst}
.. autoclass:: pyquantlib.Compounding
```

| Value | Discount factor at time $t$ |
|---|---|
| `Simple` | $1 / (1 + r \cdot t)$ |
| `Compounded` | $1 / (1 + r/n)^{n t}$ |
| `Continuous` | $e^{-r t}$ |
| `SimpleThenCompounded` | Simple for $t < 1/n$, then compounded |
| `CompoundedThenSimple` | Compounded for $t \geq 1/n$, then simple |

```{eval-rst}
.. autoclass:: pyquantlib.PositionType
```

| Value | Meaning |
|---|---|
| `Long` | Long position |
| `Short` | Short position |

```{eval-rst}
.. autoclass:: pyquantlib.ProtectionSide
```

| Value | Meaning |
|---|---|
| `Buyer` | Protection buyer |
| `Seller` | Protection seller |

### Numeric sentinels

| Constant | Use |
|---|---|
| `ql.EPSILON` | Machine epsilon for floating point. |
| `ql.NullReal` | Sentinel for "no value" in a `Real` (`double`) slot. |
| `ql.NullSize` | Sentinel for "no value" in a `Size` / integer slot. |
| `ql.MAX_REAL`, `ql.MIN_REAL` | Range bounds on `Real`. |
| `ql.MIN_POSITIVE_REAL` | Smallest strictly positive `Real`. |
| `ql.MAX_INTEGER`, `ql.MIN_INTEGER` | Range bounds on `Integer`. |

```python
if value == ql.NullReal:
    print("Value not available")
```

These appear in helper signatures (e.g. `tGrid: int = ql.NullSize` in many FD engine constructors) to mark unused alternatives where two parameters are mutually exclusive.

## See also

- {doc}`time`: dates, calendars, day-counters, schedules
- {doc}`quotes`: market-data quotes that consume `Settings.evaluationDate`
