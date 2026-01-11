# Time Module

Date arithmetic, calendars, day counters, and schedule generation.

## Date

```{eval-rst}
.. autoclass:: pyquantlib.Date
   :members:
   :undoc-members:
```

## Period

```{eval-rst}
.. autoclass:: pyquantlib.Period
   :members:
   :undoc-members:
```

## Calendar

```{eval-rst}
.. autoclass:: pyquantlib.Calendar
   :members:
   :undoc-members:
```

### Available Calendars

| Region | Calendars |
|--------|-----------|
| **Multi-national** | `TARGET`, `WeekendsOnly`, `NullCalendar`, `JointCalendar`, `BespokeCalendar` |
| **Americas** | `UnitedStates`, `Canada`, `Brazil`, `Mexico`, `Argentina`, `Chile` |
| **Europe** | `UnitedKingdom`, `Germany`, `France`, `Italy`, `Switzerland`, `Sweden`, `Norway`, `Denmark`, `Finland`, `Poland`, `CzechRepublic`, `Hungary`, `Romania`, `Russia`, `Ukraine`, `Turkey`, `Iceland`, `Austria`, `Slovakia` |
| **Asia-Pacific** | `Japan`, `China`, `HongKong`, `Singapore`, `Australia`, `NewZealand`, `India`, `SouthKorea`, `Taiwan`, `Indonesia`, `Thailand` |
| **Middle East/Africa** | `SaudiArabia`, `Israel`, `SouthAfrica`, `Botswana` |

### Usage

```python
import pyquantlib as ql

# Create calendars
target = ql.TARGET()
us = ql.UnitedStates(ql.UnitedStates.NYSE)
uk = ql.UnitedKingdom(ql.UnitedKingdom.Exchange)

# Check if date is a business day
date = ql.Date(25, 12, 2025)
print(target.isBusinessDay(date))  # False (Christmas)

# Get next business day
next_bd = target.adjust(date, ql.Following)

# Count business days
start = ql.Date(1, 6, 2025)
end = ql.Date(30, 6, 2025)
print(target.businessDaysBetween(start, end))

# Joint calendar (holiday if holiday in ANY calendar)
joint = ql.JointCalendar(target, us)
```

### UnitedStates Market Variants

```python
import pyquantlib as ql

# Different US market calendars
nyse = ql.UnitedStates(ql.UnitedStates.NYSE)
govt_bond = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
sofr = ql.UnitedStates(ql.UnitedStates.SOFR)
federal_reserve = ql.UnitedStates(ql.UnitedStates.FederalReserve)
```

### UnitedKingdom Market Variants

```python
import pyquantlib as ql

# Different UK market calendars
exchange = ql.UnitedKingdom(ql.UnitedKingdom.Exchange)
metals = ql.UnitedKingdom(ql.UnitedKingdom.Metals)
settlement = ql.UnitedKingdom(ql.UnitedKingdom.Settlement)
```

## DayCounter

```{eval-rst}
.. autoclass:: pyquantlib.DayCounter
   :members:
   :undoc-members:
```

### Available Day Counters

| Day Counter | Description |
|-------------|-------------|
| `Actual360` | Actual/360 |
| `Actual365Fixed` | Actual/365 (Fixed) |
| `Actual364` | Actual/364 |
| `Actual366` | Actual/366 |
| `ActualActual` | Actual/Actual (various conventions) |
| `Thirty360` | 30/360 (various conventions) |
| `Thirty365` | 30/365 |
| `Business252` | Business/252 |
| `OneDayCounter` | Returns 1 for any period |
| `SimpleDayCounter` | Simple day counter |

### Usage

```python
import pyquantlib as ql

dc = ql.Actual365Fixed()

start = ql.Date(1, 6, 2025)
end = ql.Date(1, 12, 2025)

# Year fraction
yf = dc.yearFraction(start, end)
print(yf)  # ~0.5

# Day count
days = dc.dayCount(start, end)
print(days)  # 183
```

## Schedule

```{eval-rst}
.. autoclass:: pyquantlib.Schedule
   :members:
   :undoc-members:
```

### MakeSchedule

Builder for creating schedules.

```{eval-rst}
.. autoclass:: pyquantlib.MakeSchedule
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

today = ql.Date(15, 6, 2025)

# Build a schedule using MakeSchedule
schedule = ql.MakeSchedule() \
    .fromDate(today) \
    .to(today + ql.Period("5Y")) \
    .withFrequency(ql.Semiannual) \
    .withCalendar(ql.TARGET()) \
    .withConvention(ql.ModifiedFollowing) \
    .withTerminationDateConvention(ql.ModifiedFollowing) \
    .withRule(ql.DateGeneration.Forward) \
    .value()

# Iterate over dates
for date in schedule:
    print(date)
```

## TimeGrid

```{eval-rst}
.. autoclass:: pyquantlib.TimeGrid
   :members:
   :undoc-members:
```

## Enumerations

### TimeUnit

```{eval-rst}
.. autoclass:: pyquantlib.TimeUnit
   :members:
   :undoc-members:
```

### Weekday

```{eval-rst}
.. autoclass:: pyquantlib.Weekday
   :members:
   :undoc-members:
```

### Month

```{eval-rst}
.. autoclass:: pyquantlib.Month
   :members:
   :undoc-members:
```

### BusinessDayConvention

```{eval-rst}
.. autoclass:: pyquantlib.BusinessDayConvention
   :members:
   :undoc-members:
```

| Convention | Description |
|------------|-------------|
| `Unadjusted` | Do not adjust |
| `Following` | Next business day |
| `ModifiedFollowing` | Next business day unless different month, then previous |
| `Preceding` | Previous business day |
| `ModifiedPreceding` | Previous business day unless different month, then next |

### DateGeneration

```{eval-rst}
.. autoclass:: pyquantlib.DateGeneration
   :members:
   :undoc-members:
```

### Frequency

```{eval-rst}
.. autoclass:: pyquantlib.Frequency
   :members:
   :undoc-members:
```

| Frequency | Periods per year |
|-----------|------------------|
| `Annual` | 1 |
| `Semiannual` | 2 |
| `Quarterly` | 4 |
| `Monthly` | 12 |
| `Weekly` | 52 |
| `Daily` | 365 |
