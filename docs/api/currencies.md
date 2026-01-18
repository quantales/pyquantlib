# Currencies Module

## Classes

### Currency

```{eval-rst}
.. autoclass:: pyquantlib.Currency
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

```{eval-rst}
.. autoclass:: pyquantlib.Money
```

```python
usd_amount = ql.Money(100.0, ql.USDCurrency())
print(usd_amount.value())
print(usd_amount.currency())
```

### ExchangeRate

```{eval-rst}
.. autoclass:: pyquantlib.ExchangeRate
```

```python
rate = ql.ExchangeRate(ql.EURCurrency(), ql.USDCurrency(), 1.10)
usd_amount = rate.exchange(eur_amount)
```

### ExchangeRateManager

```{eval-rst}
.. autoclass:: pyquantlib.ExchangeRateManager
```

## Major Currency Classes

### USDCurrency

```{eval-rst}
.. autoclass:: pyquantlib.USDCurrency
```

### EURCurrency

```{eval-rst}
.. autoclass:: pyquantlib.EURCurrency
```

### GBPCurrency

```{eval-rst}
.. autoclass:: pyquantlib.GBPCurrency
```

### JPYCurrency

```{eval-rst}
.. autoclass:: pyquantlib.JPYCurrency
```

### CHFCurrency

```{eval-rst}
.. autoclass:: pyquantlib.CHFCurrency
```
