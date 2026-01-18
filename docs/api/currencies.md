# Currencies Module

## Classes

### Currency

```{eval-rst}
.. autoclass:: pyquantlib.Currency
   :members:
   :undoc-members:
```

```python
usd = ql.USDCurrency()
print(usd.name())   # "U.S. dollar"
print(usd.code())   # "USD"
print(usd.symbol()) # "$"
```

#### Available Currencies

| Region | Currencies |
|--------|------------|
| Americas | USD, CAD, MXN, BRL, ARS, CLP, COP, PEN |
| Europe | EUR, GBP, CHF, SEK, NOK, DKK, PLN, CZK, HUF, RON |
| Asia-Pacific | JPY, CNY, CNH, HKD, SGD, AUD, NZD, KRW, TWD, INR, THB, MYR, IDR, PHP |
| Middle East/Africa | AED, SAR, ILS, ZAR, EGP, KES, NGN |
| Crypto | BTC, ETH, LTC, XRP, DASH, ZEC |

### Money

Represents an amount in a specific currency.

```{eval-rst}
.. autoclass:: pyquantlib.Money
   :members:
   :undoc-members:
```

```python
usd_amount = ql.Money(100.0, ql.USDCurrency())
print(usd_amount.value())
print(usd_amount.currency())
```

### ExchangeRate

Represents an exchange rate between two currencies.

```{eval-rst}
.. autoclass:: pyquantlib.ExchangeRate
   :members:
   :undoc-members:
```

```python
rate = ql.ExchangeRate(ql.EURCurrency(), ql.USDCurrency(), 1.10)
usd_amount = rate.exchange(eur_amount)
```

### ExchangeRateManager

Global manager for exchange rates.

```{eval-rst}
.. autoclass:: pyquantlib.ExchangeRateManager
   :members:
   :undoc-members:
```

## Major Currency Classes

### USDCurrency

```{eval-rst}
.. autoclass:: pyquantlib.USDCurrency
   :members:
```

### EURCurrency

```{eval-rst}
.. autoclass:: pyquantlib.EURCurrency
   :members:
```

### GBPCurrency

```{eval-rst}
.. autoclass:: pyquantlib.GBPCurrency
   :members:
```

### JPYCurrency

```{eval-rst}
.. autoclass:: pyquantlib.JPYCurrency
   :members:
```

### CHFCurrency

```{eval-rst}
.. autoclass:: pyquantlib.CHFCurrency
   :members:
```
