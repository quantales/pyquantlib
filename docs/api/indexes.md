# Indexes Module

Interest rate indexes and other market indexes.

## Overview

Indexes represent market rates used for floating-rate instruments. PyQuantLib provides the abstract base classes for index implementations.

## Usage

```python
import pyquantlib as ql
from pyquantlib.base import Index, InterestRateIndex

# Indexes are typically used with floating-rate instruments
# and term structure construction
```

## Abstract Base Classes

The following abstract classes are available in `pyquantlib.base`:

### Index

Base class for all indexes.

```python
from pyquantlib.base import Index
```

Key methods:
- `name()` — Returns the index name
- `fixingCalendar()` — Returns the calendar for fixing dates
- `isValidFixingDate(date)` — Checks if a date is a valid fixing date
- `fixing(date)` — Returns the fixing for a given date
- `addFixing(date, value)` — Adds a historical fixing

### InterestRateIndex

Base class for interest rate indexes (e.g., LIBOR, EURIBOR, SOFR).

```python
from pyquantlib.base import InterestRateIndex
```

Additional methods:
- `familyName()` — Returns the index family name
- `tenor()` — Returns the index tenor
- `currency()` — Returns the index currency
- `dayCounter()` — Returns the day counter
- `fixingDays()` — Returns the number of fixing days

## Example: Working with Fixings

```python
import pyquantlib as ql

# Historical fixings can be added to indexes
# index.addFixing(ql.Date(15, 6, 2025), 0.05)

# Retrieve a fixing
# rate = index.fixing(ql.Date(15, 6, 2025))
```

```{note}
Concrete index implementations (SOFR, ESTR, etc.) may be added in future releases.
```
