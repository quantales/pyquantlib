# Quotes Module

Market observables and handles for lazy evaluation.

## Quote Classes

### SimpleQuote

The most common quote type — a value that can be set and observed.

```{eval-rst}
.. autoclass:: pyquantlib.SimpleQuote
   :members:
   :undoc-members:
```

### Usage

```python
import pyquantlib as ql

# Create a quote
spot = ql.SimpleQuote(100.0)

# Read value
print(spot.value())  # 100.0

# Update value (triggers observers)
spot.setValue(105.0)
print(spot.value())  # 105.0

# Check if value is set
print(spot.isValid())  # True
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

### Usage

```python
import pyquantlib as ql

# Create quote and handle
spot = ql.SimpleQuote(100.0)
handle = ql.QuoteHandle(spot)

# Use in term structures, processes, etc.
process = ql.GeneralizedBlackScholesProcess(
    handle,  # spot handle
    ...
)

# Relinkable handles can be redirected
relinkable = ql.RelinkableQuoteHandle(spot)
new_spot = ql.SimpleQuote(105.0)
relinkable.linkTo(new_spot)  # Now points to new_spot
```

## Observer Pattern

Quotes participate in QuantLib's observer pattern. When a quote's value changes, all dependent calculations are automatically invalidated:

```python
import pyquantlib as ql

# Setup
spot = ql.SimpleQuote(100.0)
# ... create option using spot handle ...

# Option NPV computed with spot = 100
npv1 = option.NPV()

# Change spot
spot.setValue(105.0)

# Option NPV automatically recomputed with spot = 105
npv2 = option.NPV()
```
