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

## Equity Indexes

### EquityIndex

```{eval-rst}
.. autoclass:: pyquantlib.EquityIndex
```

Equity index for total return swap pricing. Supports interest rate and dividend curves.

```python
eq_index = ql.EquityIndex("SPX", ql.UnitedStates(ql.UnitedStates.NYSE),
                           ql.USDCurrency())

# With term structures
eq_index = ql.EquityIndex("SPX", ql.UnitedStates(ql.UnitedStates.NYSE),
                           ql.USDCurrency(), interest_ts, dividend_ts, spot)
```

## Regions

Regions identify the geographic area for inflation indexes.

### Region

```{eval-rst}
.. autoclass:: pyquantlib.Region
   :members:
```

### CustomRegion

```{eval-rst}
.. autoclass:: pyquantlib.CustomRegion
```

```python
region = ql.CustomRegion("Brazil", "BR")
print(region.name(), region.code())
```

### Concrete Regions

| Class | Name | Code |
|-------|------|------|
| `AustraliaRegion` | Australia | AU |
| `EURegion` | EU | EU |
| `FranceRegion` | France | FR |
| `UKRegion` | UK | UK |
| `USRegion` | USA | US |
| `ZARegion` | South Africa | ZA |

```python
us = ql.USRegion()
print(us.name(), us.code())  # "USA" "US"
```

## Inflation Indexes

### InflationIndex

```{eval-rst}
.. autoclass:: pyquantlib.base.InflationIndex
   :members:
```

Base class for all inflation indexes. Provides `familyName()`, `region()`, `revised()`, `frequency()`, `availabilityLag()`, and `currency()`.

### CPI

```{eval-rst}
.. autoclass:: pyquantlib.CPI
   :members:
   :undoc-members:
```

CPI interpolation types and the `laggedFixing` static method.

```python
# Interpolation types
ql.CPI.AsIndex          # use index's built-in interpolation
ql.CPI.Flat             # flat (no interpolation within period)
ql.CPI.Linear           # linear interpolation between fixings

# Compute lagged fixing
fixing = ql.CPI.laggedFixing(index, date, observationLag, interpolation)
```

### ZeroInflationIndex

```{eval-rst}
.. autoclass:: pyquantlib.ZeroInflationIndex
```

```python
# Without term structure
idx = ql.ZeroInflationIndex("CPI", ql.USRegion(), False, ql.Monthly,
                            ql.Period(3, ql.Months), ql.USDCurrency())

# With term structure (hidden handle)
idx = ql.ZeroInflationIndex("CPI", ql.USRegion(), False, ql.Monthly,
                            ql.Period(3, ql.Months), ql.USDCurrency(),
                            zero_inflation_curve)
```

### YoYInflationIndex

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationIndex
```

```python
# Ratio-based from a zero inflation index
yoy = ql.YoYInflationIndex(zero_index)

# Quoted year-on-year index
yoy = ql.YoYInflationIndex("YYUS", ql.USRegion(), False, False,
                           ql.Monthly, ql.Period(3, ql.Months),
                           ql.USDCurrency())
```

### Concrete Inflation Indexes

#### US CPI

```{eval-rst}
.. autoclass:: pyquantlib.USCPI
.. autoclass:: pyquantlib.YYUSCPI
```

```python
cpi = ql.USCPI()                          # without term structure
cpi = ql.USCPI(zero_inflation_curve)      # with term structure

yy = ql.YYUSCPI()                         # without term structure
yy = ql.YYUSCPI(yoy_inflation_curve)      # with term structure
```

#### EU HICP

```{eval-rst}
.. autoclass:: pyquantlib.EUHICP
.. autoclass:: pyquantlib.EUHICPXT
.. autoclass:: pyquantlib.YYEUHICP
.. autoclass:: pyquantlib.YYEUHICPXT
```

#### UK RPI

```{eval-rst}
.. autoclass:: pyquantlib.UKRPI
.. autoclass:: pyquantlib.YYUKRPI
```

#### Australian CPI

```{eval-rst}
.. autoclass:: pyquantlib.AUCPI
.. autoclass:: pyquantlib.YYAUCPI
```

```python
cpi = ql.AUCPI(ql.Quarterly, False)          # frequency and revised flag
cpi = ql.AUCPI(ql.Quarterly, False, zero_inflation_curve)
```

#### French HICP

```{eval-rst}
.. autoclass:: pyquantlib.FRHICP
.. autoclass:: pyquantlib.YYFRHICP
```

#### South African CPI

```{eval-rst}
.. autoclass:: pyquantlib.ZACPI
.. autoclass:: pyquantlib.YYZACPI
```
