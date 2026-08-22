# Currencies

Bindings for QuantLib's currency framework: a `Currency` is metadata (name, ISO code, symbol, fractional unit, rounding); a `Money` is a `(value, Currency)` pair; an `ExchangeRate` converts one to another; the `ExchangeRateManager` is a singleton that stores known rates.

About 100 country currencies are bound (full ISO 4217 coverage plus a handful of historical and crypto ones). They are constructed by calling the class with no arguments (`ql.USDCurrency()`); the resulting object exposes `.name()`, `.code()`, `.symbol()`, `.fractionsPerUnit()`, and the rounding rule.

## At a glance

| Class | Role |
|---|---|
| {py:class}`pyquantlib.Currency` | Base type. Most user code constructs a concrete subclass like `ql.USDCurrency()`; `Currency` is what helper signatures and `Money.currency()` return. |
| {py:class}`pyquantlib.Money` | An amount in a specific currency. Supports arithmetic with conversion via the `ExchangeRateManager`. |
| {py:class}`pyquantlib.ExchangeRate` | A directed conversion factor between two currencies. |
| {py:class}`pyquantlib.ExchangeRateManager` | Singleton registry of `ExchangeRate`s. Lookup is by date and currency pair; chained lookups are supported. |

### Available currency classes

Concrete `<XYZ>Currency` classes exist for all major and most secondary currencies. The naming convention is `<ISO>Currency` (e.g. `USDCurrency`, `EURCurrency`, `JPYCurrency`).

| Region | Currencies |
|---|---|
| **Americas** | USD, CAD, MXN, BRL, ARS, CLP, COP, PEN, UYU, TTD, VEB |
| **Europe** | EUR, GBP, CHF, SEK, NOK, DKK, PLN, CZK, HUF, RON, RUB, TRY, RSD, BGN, HRK, ISK, UAH, GEL |
| **Asia-Pacific** | JPY, CNY, CNH, HKD, SGD, AUD, NZD, KRW, TWD, INR, THB, MYR, IDR, PHP, VND, BDT, LKR, NPR, PKR |
| **Middle East / Africa** | AED, SAR, ILS, ZAR, EGP, KES, NGN, GHS, MAD, KWD, BHD, JOD, OMR, QAR, IQD, IRR, TND, ZMW, ETB, UGX, AOA, MUR, BWP, XOF |
| **Crypto** | BTC, ETH, LTC, XRP, DASH, ZEC, BCH, ETC |
| **Historical (pre-Euro and others)** | DEM, FRF, ITL, ESP, NLG, BEF, ATS, FIM, IEP, GRD, PTE, LUF, CYP, EEK, SKK, SIT, MTL, BGL, ROL, TRL, BYR, LVL, LTL |

## Common patterns

### Inspect a currency

```python
import pyquantlib as ql

usd = ql.USDCurrency()
print(usd.name())              # "U.S. dollar"
print(usd.code())              # "USD"
print(usd.symbol())            # "$"
print(usd.fractionsPerUnit())  # 100
```

### Construct a `Money` value and read it back

```python
amount = ql.Money(100.0, ql.USDCurrency())
print(amount.value())          # 100.0
print(amount.currency().code())  # "USD"
```

### Convert between currencies via `ExchangeRate`

```python
eur_usd = ql.ExchangeRate(ql.EURCurrency(), ql.USDCurrency(), 1.10)

eur = ql.Money(100.0, ql.EURCurrency())
usd = eur_usd.exchange(eur)
print(usd.value(), usd.currency().code())   # 110.0 USD
```

`ExchangeRate.exchange()` checks the source currency and computes the target value in one step. For chained conversions (e.g. EUR to JPY via USD), register the legs with the `ExchangeRateManager` and let it find the path.

## Reference

### Framework

```{eval-rst}
.. autoclass:: pyquantlib.Currency
```

```{eval-rst}
.. autoclass:: pyquantlib.Money
```

```{eval-rst}
.. autoclass:: pyquantlib.ExchangeRate
```

```{eval-rst}
.. autoclass:: pyquantlib.ExchangeRateManager
```

### Major currencies

```{eval-rst}
.. autoclass:: pyquantlib.USDCurrency
```

```{eval-rst}
.. autoclass:: pyquantlib.EURCurrency
```

```{eval-rst}
.. autoclass:: pyquantlib.GBPCurrency
```

```{eval-rst}
.. autoclass:: pyquantlib.JPYCurrency
```

```{eval-rst}
.. autoclass:: pyquantlib.CHFCurrency
```

```{note}
The ~100 other concrete currency classes (CADCurrency, AUDCurrency, KRWCurrency, ...) follow the same pattern: zero-argument constructor, the same accessor methods (`name`, `code`, `symbol`, `fractionsPerUnit`). They are not autodoc'd individually to keep this page navigable; the catalog table above lists what is bound.
```

## See also

- {doc}`/concepts/term-structures`: how currencies show up in helper and curve constructors
- {doc}`time`: calendars often pair with currencies (e.g. `USDCurrency` + `UnitedStates` calendar)
