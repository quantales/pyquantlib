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

```{note}
Concrete index implementations (SOFR, ESTR, etc.) may be added in future releases.
```
