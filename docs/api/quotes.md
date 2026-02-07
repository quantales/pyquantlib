# Quotes Module

## Quotes

### SimpleQuote

```{eval-rst}
.. autoclass:: pyquantlib.SimpleQuote
```

```python
spot = ql.SimpleQuote(100.0)
spot.setValue(105.0)
print(spot.value())  # 105.0
```

### DerivedQuote

```{eval-rst}
.. autoclass:: pyquantlib.DerivedQuote
```

### CompositeQuote

```{eval-rst}
.. autoclass:: pyquantlib.CompositeQuote
```

### QuoteHandle

```{eval-rst}
.. autoclass:: pyquantlib.QuoteHandle
```

### RelinkableQuoteHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableQuoteHandle
```

```python
spot = ql.SimpleQuote(100.0)
handle = ql.QuoteHandle(spot)

# Relinkable handles can be redirected
relinkable = ql.RelinkableQuoteHandle(spot)
new_spot = ql.SimpleQuote(105.0)
relinkable.linkTo(new_spot)
```

## Observer Pattern

Quotes participate in QuantLib's observer pattern. When a quote's value changes, all dependent calculations are automatically invalidated:

```python
spot = ql.SimpleQuote(100.0)
# ... create option using spot handle ...

npv1 = option.NPV()  # computed with spot = 100
spot.setValue(105.0)
npv2 = option.NPV()  # automatically recomputed with spot = 105
```
