# Currencies Module

Currency definitions, exchange rates, and money.

## Currency

```{eval-rst}
.. autoclass:: pyquantlib.Currency
   :members:
   :undoc-members:
```

### Available Currencies

PyQuantLib provides currency definitions for major currencies:

| Region | Currencies |
|--------|------------|
| Americas | USD, CAD, MXN, BRL, ARS, CLP, COP, PEN |
| Europe | EUR, GBP, CHF, SEK, NOK, DKK, PLN, CZK, HUF, RON |
| Asia-Pacific | JPY, CNY, CNH, HKD, SGD, AUD, NZD, KRW, TWD, INR, THB, MYR, IDR, PHP |
| Middle East/Africa | AED, SAR, ILS, ZAR, EGP, KES, NGN |
| Crypto | BTC, ETH, LTC, XRP, DASH, ZEC |

### Usage

```python
import pyquantlib as ql

# Create currency
usd = ql.USDCurrency()
eur = ql.EURCurrency()

print(usd.name())           # "U.S. dollar"
print(usd.code())           # "USD"
print(usd.numericCode())    # 840
print(usd.symbol())         # "$"
```

## Money

Represents an amount in a specific currency.

```{eval-rst}
.. autoclass:: pyquantlib.Money
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

# Create money amounts
usd_amount = ql.Money(100.0, ql.USDCurrency())
eur_amount = ql.Money(85.0, ql.EURCurrency())

print(usd_amount.value())      # 100.0
print(usd_amount.currency())   # USDCurrency
```

## ExchangeRate

Represents an exchange rate between two currencies.

```{eval-rst}
.. autoclass:: pyquantlib.ExchangeRate
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

# Create exchange rate: 1 EUR = 1.10 USD
eur = ql.EURCurrency()
usd = ql.USDCurrency()
rate = ql.ExchangeRate(eur, usd, 1.10)

# Convert money
eur_amount = ql.Money(100.0, eur)
usd_amount = rate.exchange(eur_amount)
```

## ExchangeRateManager

Global manager for exchange rates.

```{eval-rst}
.. autoclass:: pyquantlib.ExchangeRateManager
   :members:
   :undoc-members:
```

## Currency Classes

### Major Currencies

```{eval-rst}
.. autoclass:: pyquantlib.USDCurrency
   :members:

.. autoclass:: pyquantlib.EURCurrency
   :members:

.. autoclass:: pyquantlib.GBPCurrency
   :members:

.. autoclass:: pyquantlib.JPYCurrency
   :members:

.. autoclass:: pyquantlib.CHFCurrency
   :members:
```
