# Quotes Module

## Classes

### SimpleQuote

The most common quote type: a value that can be set and observed.

```{eval-rst}
.. autoclass:: pyquantlib.SimpleQuote
   :members:
   :undoc-members:
```

```python
spot = ql.SimpleQuote(100.0)
spot.setValue(105.0)
print(spot.value())  # 105.0
```

### DerivedQuote

A quote whose value is computed from another quote.

```{eval-rst}
.. autoclass:: pyquantlib.DerivedQuote
   :members:
   :undoc-members:
```

### CompositeQuote

A quote whose value is computed from two other quotes.

```{eval-rst}
.. autoclass:: pyquantlib.CompositeQuote
   :members:
   :undoc-members:
```

## Handles

Handles provide a layer of indirection for quotes and term structures, enabling the observer pattern.

### QuoteHandle

```{eval-rst}
.. autoclass:: pyquantlib.QuoteHandle
   :members:
   :undoc-members:
```

### RelinkableQuoteHandle

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableQuoteHandle
   :members:
   :undoc-members:
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
