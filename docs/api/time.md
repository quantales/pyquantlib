# Time

Bindings for QuantLib's time framework: `Date`, `Period`, `TimeGrid`, ~50 country `Calendar`s, ~10 `DayCounter` conventions, the `Schedule` / `MakeSchedule` builders, and the supporting enums (`TimeUnit`, `Weekday`, `Month`, `BusinessDayConvention`, `DateGeneration`, `Frequency`).

## At a glance

| Group | Classes |
|---|---|
| Date primitives | {py:class}`pyquantlib.Date`, {py:class}`pyquantlib.Period`, {py:class}`pyquantlib.TimeGrid` |
| Calendars | {py:class}`pyquantlib.Calendar` (abstract) plus ~50 concrete subclasses (`TARGET`, `UnitedStates`, `UnitedKingdom`, `Japan`, ...) |
| Day counters | {py:class}`pyquantlib.DayCounter` (abstract) plus `Actual360`, `Actual365Fixed`, `Actual364`, `Actual366`, `ActualActual`, `Thirty360`, `Thirty365`, `Business252`, `OneDayCounter`, `SimpleDayCounter` |
| Schedules | {py:class}`pyquantlib.Schedule`, {py:class}`pyquantlib.MakeSchedule` |
| Enums | {py:class}`pyquantlib.TimeUnit`, {py:class}`pyquantlib.Weekday`, {py:class}`pyquantlib.Month`, {py:class}`pyquantlib.BusinessDayConvention`, {py:class}`pyquantlib.DateGeneration`, {py:class}`pyquantlib.Frequency` |

`Date` arithmetic, calendar adjustments, day-count year fractions, and schedule generation are the four operations that show up in nearly every PyQuantLib script.

## Common patterns

### Construct a date and add a tenor

```python
import pyquantlib as ql

today    = ql.Date(15, 6, 2025)
maturity = today + ql.Period("1Y")
```

`Date` arithmetic with `Period` returns a new `Date` (calendar-unaware: it does not adjust for business days).

### Pick a calendar and check business days

```python
target = ql.TARGET()
us     = ql.UnitedStates(ql.UnitedStates.NYSE)

xmas = ql.Date(25, 12, 2025)
print(target.isBusinessDay(xmas))                  # False
next_bd = target.adjust(xmas, ql.Following)        # next BD with the convention
```

`Calendar.adjust(date, convention)` is the canonical way to roll a non-business date forward or back. Multi-currency products often combine calendars via `JointCalendar`.

### Compute a year fraction

```python
dc    = ql.Actual365Fixed()
start = ql.Date(1, 6, 2025)
end   = ql.Date(1, 12, 2025)
yf    = dc.yearFraction(start, end)                # ~0.5042
```

Each helper / instrument carries its own day counter; the year fraction it computes only matters for that helper. The curve's own day counter (passed to `Piecewise*` constructors) is for output only.

### Build a schedule with `MakeSchedule`

```python
schedule = (
    ql.MakeSchedule()
      .fromDate(today)
      .to(today + ql.Period("5Y"))
      .withFrequency(ql.Semiannual)
      .withCalendar(ql.TARGET())
      .withConvention(ql.ModifiedFollowing)
      .value()
)
```

`MakeSchedule` is the keyword-argument builder for `Schedule`. The chain ends with `.value()` to materialise the schedule.

## Reference

### Date primitives

```{eval-rst}
.. autoclass:: pyquantlib.Date
```

```{eval-rst}
.. autoclass:: pyquantlib.Period
```

```{eval-rst}
.. autoclass:: pyquantlib.TimeGrid
```

### Calendars

```{eval-rst}
.. autoclass:: pyquantlib.Calendar
```

#### Available calendars

| Region | Calendars |
|--------|-----------|
| **Multi-national** | `TARGET`, `WeekendsOnly`, `NullCalendar`, `JointCalendar`, `BespokeCalendar` |
| **Americas** | `UnitedStates`, `Canada`, `Brazil`, `Mexico`, `Argentina`, `Chile` |
| **Europe** | `UnitedKingdom`, `Germany`, `France`, `Italy`, `Switzerland`, `Sweden`, `Norway`, `Denmark`, `Finland`, `Poland`, `CzechRepublic`, `Hungary`, `Romania`, `Russia`, `Ukraine`, `Turkey`, `Iceland`, `Austria`, `Slovakia` |
| **Asia-Pacific** | `Japan`, `China`, `HongKong`, `Singapore`, `Australia`, `NewZealand`, `India`, `SouthKorea`, `Taiwan`, `Indonesia`, `Thailand` |
| **Middle East / Africa** | `SaudiArabia`, `Israel`, `SouthAfrica`, `Botswana` |

#### `UnitedStates` variants

`NYSE`, `GovernmentBond`, `SOFR`, `FederalReserve`

#### `UnitedKingdom` variants

`Exchange`, `Metals`, `Settlement`

### Day counters

```{eval-rst}
.. autoclass:: pyquantlib.DayCounter
```

| Day counter | Description |
|---|---|
| `Actual360` | Actual / 360 |
| `Actual365Fixed` | Actual / 365 (fixed) |
| `Actual364` | Actual / 364 |
| `Actual366` | Actual / 366 |
| `ActualActual` | Actual / Actual (various conventions) |
| `Thirty360` | 30 / 360 (various conventions) |
| `Thirty365` | 30 / 365 |
| `Business252` | Business / 252 |
| `OneDayCounter` | Returns 1 for any period |
| `SimpleDayCounter` | Simple day counter |

### Schedules

```{eval-rst}
.. autoclass:: pyquantlib.Schedule
```

```{eval-rst}
.. autoclass:: pyquantlib.MakeSchedule
```

### Enumerations

```{eval-rst}
.. autoclass:: pyquantlib.TimeUnit
```

```{eval-rst}
.. autoclass:: pyquantlib.Weekday
```

```{eval-rst}
.. autoclass:: pyquantlib.Month
```

```{eval-rst}
.. autoclass:: pyquantlib.BusinessDayConvention
```

| Convention | Effect |
|---|---|
| `Unadjusted` | No adjustment |
| `Following` | Next business day |
| `ModifiedFollowing` | Next business day unless that crosses a month boundary, then previous |
| `Preceding` | Previous business day |
| `ModifiedPreceding` | Previous business day unless that crosses a month boundary, then next |

```{eval-rst}
.. autoclass:: pyquantlib.DateGeneration
```

```{eval-rst}
.. autoclass:: pyquantlib.Frequency
```

| Frequency | Periods per year |
|---|---|
| `Annual` | 1 |
| `Semiannual` | 2 |
| `Quarterly` | 4 |
| `Monthly` | 12 |
| `Weekly` | 52 |
| `Daily` | 365 |

## See also

- {doc}`core`: the `Settings` singleton that holds the global evaluation date
- {doc}`indexes`: indices that consume calendars and day counters
