# Indexes Module

Indexes represent market rates used for floating-rate instruments.

## Abstract Base Classes

The following abstract classes are available in `pyquantlib.base`:

### Index

Base class for all indexes.

Key methods:
- `name()`: Returns the index name
- `fixingCalendar()`: Returns the calendar for fixing dates
- `isValidFixingDate(date)`: Checks if a date is a valid fixing date
- `fixing(date)`: Returns the fixing for a given date
- `addFixing(date, value)`: Adds a historical fixing

### InterestRateIndex

Base class for interest rate indexes (e.g., LIBOR, EURIBOR, SOFR).

Additional methods:
- `familyName()`: Returns the index family name
- `tenor()`: Returns the index tenor
- `currency()`: Returns the index currency
- `dayCounter()`: Returns the day counter
- `fixingDays()`: Returns the number of fixing days

```python
from pyquantlib.base import Index, InterestRateIndex
```

## IBOR Indexes

### IborIndex

```{eval-rst}
.. autoclass:: pyquantlib.IborIndex
   :members:
```

### Euribor

```{eval-rst}
.. autoclass:: pyquantlib.Euribor
```

```python
euribor6m = ql.Euribor(ql.Period(6, ql.Months), curve)
```

## Overnight Indexes

### Sofr

```{eval-rst}
.. autoclass:: pyquantlib.Sofr
```

Secured Overnight Financing Rate (USD).

```python
sofr = ql.Sofr()           # without curve
sofr = ql.Sofr(curve)      # with forwarding curve
```

### Eonia

```{eval-rst}
.. autoclass:: pyquantlib.Eonia
```

Euro Overnight Index Average (EONIA) rate fixed by the ECB.

```python
eonia = ql.Eonia()           # without curve
eonia = ql.Eonia(curve)      # with forwarding curve
```

### Estr

```{eval-rst}
.. autoclass:: pyquantlib.Estr
```

Euro Short-Term Rate (EUR).

```python
estr = ql.Estr(curve)
```

### Sonia

```{eval-rst}
.. autoclass:: pyquantlib.Sonia
```

Sterling Overnight Index Average (GBP).

```python
sonia = ql.Sonia(curve)
```

## Swap Indexes

### SwapIndex

```{eval-rst}
.. autoclass:: pyquantlib.SwapIndex
```

```python
euribor6m = ql.Euribor(ql.Period(6, ql.Months), curve)
swap_index = ql.SwapIndex(
    "EurSwap", ql.Period(5, ql.Years), 2,
    ql.EURCurrency(), ql.TARGET(),
    ql.Period(1, ql.Years), ql.Unadjusted,
    ql.Thirty360(ql.Thirty360.BondBasis), euribor6m,
)
```

### OvernightIndexedSwapIndex

```{eval-rst}
.. autoclass:: pyquantlib.OvernightIndexedSwapIndex
```

```python
estr = ql.Estr(curve)
ois_index = ql.OvernightIndexedSwapIndex(
    "EstrSwap", ql.Period(1, ql.Years), 2,
    ql.EURCurrency(), estr,
)
```

### Concrete Swap Index Subclasses

Standard market swap indexes with pre-configured conventions.

#### EuriborSwapIsdaFixA

```{eval-rst}
.. autoclass:: pyquantlib.EuriborSwapIsdaFixA
```

#### EuriborSwapIsdaFixB

```{eval-rst}
.. autoclass:: pyquantlib.EuriborSwapIsdaFixB
```

#### EuriborSwapIfrFix

```{eval-rst}
.. autoclass:: pyquantlib.EuriborSwapIfrFix
```

#### EurLiborSwapIsdaFixA

```{eval-rst}
.. autoclass:: pyquantlib.EurLiborSwapIsdaFixA
```

#### EurLiborSwapIsdaFixB

```{eval-rst}
.. autoclass:: pyquantlib.EurLiborSwapIsdaFixB
```

#### EurLiborSwapIfrFix

```{eval-rst}
.. autoclass:: pyquantlib.EurLiborSwapIfrFix
```

#### UsdLiborSwapIsdaFixAm

```{eval-rst}
.. autoclass:: pyquantlib.UsdLiborSwapIsdaFixAm
```

#### UsdLiborSwapIsdaFixPm

```{eval-rst}
.. autoclass:: pyquantlib.UsdLiborSwapIsdaFixPm
```

#### JpyLiborSwapIsdaFixAm

```{eval-rst}
.. autoclass:: pyquantlib.JpyLiborSwapIsdaFixAm
```

#### JpyLiborSwapIsdaFixPm

```{eval-rst}
.. autoclass:: pyquantlib.JpyLiborSwapIsdaFixPm
```

#### GbpLiborSwapIsdaFix

```{eval-rst}
.. autoclass:: pyquantlib.GbpLiborSwapIsdaFix
```

#### ChfLiborSwapIsdaFix

```{eval-rst}
.. autoclass:: pyquantlib.ChfLiborSwapIsdaFix
```

```python
swap_index = ql.EuriborSwapIsdaFixA(ql.Period(5, ql.Years))
swap_index = ql.EuriborSwapIsdaFixA(ql.Period(5, ql.Years), forwarding_curve)
swap_index = ql.EuriborSwapIsdaFixA(ql.Period(5, ql.Years), forwarding_curve, discounting_curve)
```
