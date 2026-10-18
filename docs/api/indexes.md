# Indexes

Bindings for the `Index` class hierarchy: market reference rates that feed floating-rate cash flows, swap helpers, and inflation-linked instruments. Each concrete index pre-fills the calendar, day-count, fixing-days, and currency conventions, so user code only has to pass the tenor and (optionally) a forwarding curve.

## At a glance

| Family | Classes |
|---|---|
| Ibor (term) | {py:class}`pyquantlib.IborIndex` plus concrete `Euribor`, `Nibor`, `Bbsw`, `Bkbm`, `Bibor`, `Cdor`, `Jibar`, `Robor`, `Shibor`, `Zibor` |
| LIBOR | {py:class}`pyquantlib.Libor`, {py:class}`pyquantlib.DailyTenorLibor`, {py:class}`pyquantlib.USDLibor`, {py:class}`pyquantlib.DailyTenorUSDLibor`, {py:class}`pyquantlib.USDLiborON` |
| Overnight | {py:class}`pyquantlib.Sofr`, {py:class}`pyquantlib.Eonia`, {py:class}`pyquantlib.Estr`, {py:class}`pyquantlib.Sonia`, {py:class}`pyquantlib.Shir`, {py:class}`pyquantlib.Zaronia`, plus `Aonia`, `Cdi`, `Corra`, `Destr`, `FedFunds`, `Kofr`, `Nzocr`, `Saron`, `Swestr`, `Tonar` |
| Swap | {py:class}`pyquantlib.SwapIndex`, {py:class}`pyquantlib.OvernightIndexedSwapIndex`, plus standard fixings (`EuriborSwapIsdaFixA/B/IfrFix`, `EurLiborSwap*`, `UsdLiborSwap*`, `JpyLiborSwap*`, `GbpLiborSwapIsdaFix`, `ChfLiborSwapIsdaFix`) |
| Special | {py:class}`pyquantlib.BMAIndex`, {py:class}`pyquantlib.SwapSpreadIndex`, {py:class}`pyquantlib.EquityIndex` |
| Inflation | {py:class}`pyquantlib.ZeroInflationIndex`, {py:class}`pyquantlib.YoYInflationIndex`, plus per-region (`USCPI`, `EUHICP`, `UKRPI`, `AUCPI`, `FRHICP`, `ZACPI`) |

```{note}
Abstract base classes `Index` and `InterestRateIndex` are exposed under `pyquantlib.base`.

`Index` exposes: `name()`, `fixingCalendar()`, `isValidFixingDate(date)`, `fixing(date)`, `addFixing(date, value)`.
`InterestRateIndex` adds: `familyName()`, `tenor()`, `currency()`, `dayCounter()`, `fixingDays()`.
```

## Common patterns

### Build a generic Ibor index from a forwarding curve

```python
import pyquantlib as ql

euribor6m = ql.Euribor(ql.Period(6, ql.Months), curve_handle)
```

`Euribor`, `Sofr`, `Eonia`, `Estr`, `Sonia` all support both a no-curve constructor (the index records fixings only) and a curve-handle constructor (the index can also forecast). Helpers and floating coupons consume the index; if no curve is set they pull fixings exclusively from the index's history (added via `addFixing`).

### Use a market-standard swap fixing

```python
swap_index = ql.EuriborSwapIsdaFixA(ql.Period(5, ql.Years))
swap_index = ql.EuriborSwapIsdaFixA(ql.Period(5, ql.Years), forwarding_curve)
swap_index = ql.EuriborSwapIsdaFixA(ql.Period(5, ql.Years),
                                    forwarding_curve, discounting_curve)
```

The `*SwapIsdaFix*` classes are pre-configured for the appropriate ISDA fixing conventions. Three constructor overloads cover (tenor only / + forwarding / + forwarding + discounting).

### Build a custom swap spread index

```python
idx2  = ql.EuriborSwapIsdaFixA(ql.Period("2Y"),  curve)
idx10 = ql.EuriborSwapIsdaFixA(ql.Period("10Y"), curve)
spread = ql.SwapSpreadIndex("CMS2s10s", idx2, idx10)

# Custom gearings: 0.5 * idx2 - 0.5 * idx10
weighted = ql.SwapSpreadIndex("Weighted", idx2, idx10, 0.5, -0.5)
```

### Build an inflation index

```python
zero_idx = ql.USCPI()                          # without term structure
zero_idx = ql.USCPI(zero_inflation_curve)      # with term structure

yoy_idx  = ql.YYUSCPI()
yoy_idx  = ql.YYUSCPI(yoy_inflation_curve)

# YoY can also be derived from a zero index
yoy_from_zero = ql.YoYInflationIndex(zero_idx)
```

CPI / HICP / RPI variants follow the same constructor pattern. The `laggedFixing` static method on `CPI` computes the observation-lagged fixing for inflation cash flows:

```python
fixing = ql.CPI.laggedFixing(index, date, observation_lag, interpolation)
```

## Reference

### Ibor indexes

```{eval-rst}
.. autoclass:: pyquantlib.IborIndex
   :members:
```

```{eval-rst}
.. autoclass:: pyquantlib.Euribor
```

### LIBOR indexes

```{eval-rst}
.. autoclass:: pyquantlib.Libor
   :members:
```

```{eval-rst}
.. autoclass:: pyquantlib.DailyTenorLibor
```

`Libor` applies the ICE date conventions: the value and maturity dates are computed on the joint calendar of the index currency and the financial centre, which `jointCalendar()` exposes.

```{eval-rst}
.. autoclass:: pyquantlib.USDLibor
.. autoclass:: pyquantlib.DailyTenorUSDLibor
.. autoclass:: pyquantlib.USDLiborON
```

```python
usd3m = ql.USDLibor(ql.Period(3, ql.Months))
usd3m = ql.USDLibor(ql.Period(3, ql.Months), forwarding_curve)
overnight = ql.USDLiborON(forwarding_curve)
```

```{note}
USD LIBOR ceased publication in 2023. These indexes remain bound for valuing legacy trades and for reproducing historical results; new curve construction should use {py:class}`pyquantlib.Sofr`.
```

### Overnight indexes

```{eval-rst}
.. autoclass:: pyquantlib.Sofr
```

```{eval-rst}
.. autoclass:: pyquantlib.Eonia
```

```{eval-rst}
.. autoclass:: pyquantlib.Estr
```

```{eval-rst}
.. autoclass:: pyquantlib.Sonia
```

```{eval-rst}
.. autoclass:: pyquantlib.Shir
```

Shekel Overnight Interest Rate, published by the Bank of Israel. Fixes on the
`Israel(SHIR)` calendar.

```{eval-rst}
.. autoclass:: pyquantlib.Zaronia
```

South African Rand Overnight Index Average.

```{eval-rst}
.. autoclass:: pyquantlib.Nibor
```

NOK-NIBOR, a term index: the constructor takes a `Period` tenor before the optional
forwarding curve.

### Regional overnight indexes

| Class | Rate | Currency |
|---|---|---|
| `Aonia` | Australian Overnight Index Average | AUD |
| `Cdi` | Brazilian CDI, on a Business/252 day counter | BRL |
| `Corra` | Canadian Overnight Repo Rate Average | CAD |
| `Destr` | Danish krone short-term rate | DKK |
| `FedFunds` | Federal funds effective rate | USD |
| `Kofr` | Korea Overnight Financing Repo | KRW |
| `Nzocr` | New Zealand Official Cash Rate | NZD |
| `Saron` | Swiss Average Rate Overnight | CHF |
| `Swestr` | Swedish krona short-term rate | SEK |
| `Tonar` | Tokyo Overnight Average Rate | JPY |

All share the constructor overloads of `Sofr`: no argument, a `YieldTermStructureHandle`, or a
yield term structure (wrapped in a handle internally).

```python
saron = ql.Saron(forwarding_curve)
```

### Regional term indexes

| Class | Rate | Currency | Fixed-tenor subclasses |
|---|---|---|---|
| `Bbsw` | Bank Bill Swap Rate (AFMA) | AUD | `Bbsw1M` to `Bbsw6M` |
| `Bkbm` | Bank Bill Benchmark Rate | NZD | `Bkbm1M` to `Bkbm6M` |
| `Bibor` | Bangkok Interbank Offered Rate | THB | `BiborSW`, `Bibor1M`, `Bibor2M`, `Bibor3M`, `Bibor6M`, `Bibor1Y` |
| `Cdor` | Canadian Dollar Offered Rate | CAD | none |
| `Jibar` | Johannesburg Interbank Agreed Rate | ZAR | none |
| `Robor` | Romanian Interbank Offered Rate | RON | none |
| `Shibor` | Shanghai Interbank Offered Rate | CNY | none |
| `Zibor` | Zurich Interbank Offered Rate | CHF | none |

Each base class takes a `Period` tenor before the optional forwarding curve, following `Nibor`.
`Bbsw`, `Bkbm`, and `Bibor` reject daily tenors; `Shibor` and `Robor` accept a 1-day tenor and
settle on the same day.

```python
bbsw3m = ql.Bbsw(ql.Period(3, ql.Months), forwarding_curve)
bbsw3m = ql.Bbsw3M(forwarding_curve)   # fixed-tenor subclass
```

### Swap indexes

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

```{eval-rst}
.. autoclass:: pyquantlib.OvernightIndexedSwapIndex
```

```python
estr     = ql.Estr(curve)
ois_index = ql.OvernightIndexedSwapIndex(
    "EstrSwap", ql.Period(1, ql.Years), 2,
    ql.EURCurrency(), estr,
)
```

#### Standard market swap fixings

```{eval-rst}
.. autoclass:: pyquantlib.EuriborSwapIsdaFixA
.. autoclass:: pyquantlib.EuriborSwapIsdaFixB
.. autoclass:: pyquantlib.EuriborSwapIfrFix
.. autoclass:: pyquantlib.EurLiborSwapIsdaFixA
.. autoclass:: pyquantlib.EurLiborSwapIsdaFixB
.. autoclass:: pyquantlib.EurLiborSwapIfrFix
.. autoclass:: pyquantlib.UsdLiborSwapIsdaFixAm
.. autoclass:: pyquantlib.UsdLiborSwapIsdaFixPm
.. autoclass:: pyquantlib.JpyLiborSwapIsdaFixAm
.. autoclass:: pyquantlib.JpyLiborSwapIsdaFixPm
.. autoclass:: pyquantlib.GbpLiborSwapIsdaFix
.. autoclass:: pyquantlib.ChfLiborSwapIsdaFix
```

### Special-purpose indexes

```{eval-rst}
.. autoclass:: pyquantlib.BMAIndex
```

Bond Market Association index (tax-exempt municipal reference rate). Fixes weekly on Wednesdays.

```python
bma   = ql.BMAIndex()
bma   = ql.BMAIndex(curve)
sched = bma.fixingSchedule(start, end)
```

```{eval-rst}
.. autoclass:: pyquantlib.SwapSpreadIndex
```

```{eval-rst}
.. autoclass:: pyquantlib.EquityIndex
```

```python
eq = ql.EquityIndex("SPX", ql.UnitedStates(ql.UnitedStates.NYSE),
                    ql.USDCurrency())
eq = ql.EquityIndex("SPX", ql.UnitedStates(ql.UnitedStates.NYSE),
                    ql.USDCurrency(), interest_ts, dividend_ts, spot)
```

### Regions (for inflation indexes)

```{eval-rst}
.. autoclass:: pyquantlib.Region
   :members:
```

```{eval-rst}
.. autoclass:: pyquantlib.CustomRegion
```

| Concrete region | Name | Code |
|---|---|---|
| `AustraliaRegion` | Australia | AU |
| `EURegion` | EU | EU |
| `FranceRegion` | France | FR |
| `UKRegion` | UK | UK |
| `USRegion` | USA | US |
| `ZARegion` | South Africa | ZA |

### Inflation indexes

```{eval-rst}
.. autoclass:: pyquantlib.base.InflationIndex
   :members:
```

```{eval-rst}
.. autoclass:: pyquantlib.CPI
   :members:
   :undoc-members:
```

`CPI` exposes interpolation flags (`AsIndex`, `Flat`, `Linear`) and the `laggedFixing` static method.

```{eval-rst}
.. autoclass:: pyquantlib.ZeroInflationIndex
```

```{eval-rst}
.. autoclass:: pyquantlib.YoYInflationIndex
```

#### Concrete inflation indexes

**US CPI**
```{eval-rst}
.. autoclass:: pyquantlib.USCPI
.. autoclass:: pyquantlib.YYUSCPI
```

**EU HICP**
```{eval-rst}
.. autoclass:: pyquantlib.EUHICP
.. autoclass:: pyquantlib.EUHICPXT
.. autoclass:: pyquantlib.YYEUHICP
.. autoclass:: pyquantlib.YYEUHICPXT
```

**UK RPI**
```{eval-rst}
.. autoclass:: pyquantlib.UKRPI
.. autoclass:: pyquantlib.YYUKRPI
```

**Australian CPI**
```{eval-rst}
.. autoclass:: pyquantlib.AUCPI
.. autoclass:: pyquantlib.YYAUCPI
```

**French HICP**
```{eval-rst}
.. autoclass:: pyquantlib.FRHICP
.. autoclass:: pyquantlib.YYFRHICP
```

**South African CPI**
```{eval-rst}
.. autoclass:: pyquantlib.ZACPI
.. autoclass:: pyquantlib.YYZACPI
```

## See also

- {doc}`time`: calendars and day-counters that the indexes consume
- {doc}`termstructures`: forwarding and discounting curves attached to indexes
- {doc}`cashflows`: floating coupons that price off these indexes
