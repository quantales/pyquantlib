# Quotes

Bindings for QuantLib's market-data primitives. A `Quote` is a scalar observable that holds a number and notifies its observers when that number changes; a `QuoteHandle` is the smart pointer downstream code (term structures, processes, helpers) consumes. `RelinkableQuoteHandle` adds the ability to swap the underlying `Quote` object atomically.

The `Quote` base class itself is not bound directly for instantiation. The classes below are what user code constructs.

## At a glance

| Class | Role |
|---|---|
| {py:class}`pyquantlib.SimpleQuote` | A mutable holder for one number. The default choice for a market quote that gets `setValue()`d as the market moves. |
| {py:class}`pyquantlib.DerivedQuote` | A read-only quote whose value is `f(other_quote)` for a Python callable `f`. Recomputes lazily when the source notifies. |
| {py:class}`pyquantlib.CompositeQuote` | A read-only quote whose value is `f(quote1, quote2)` for a Python callable `f`. Same recomputation semantics. |
| {py:class}`pyquantlib.MultiCompositeQuote` | A read-only quote whose value is `f(*input_quotes)` for a Python callable `f` and an arbitrary number of input quotes. |
| {py:class}`pyquantlib.DeltaVolQuote` | An FX market-data quote holding a volatility associated with a delta and maturity. Carries `DeltaType` and `AtmType` convention enums. |
| {py:class}`pyquantlib.QuoteHandle` | Smart-pointer wrapper consumed by term structures, processes, helpers. The standard form used in pricing pipelines. |
| {py:class}`pyquantlib.RelinkableQuoteHandle` | A `QuoteHandle` whose underlying `Quote` can be replaced via `linkTo(new_quote)`. Use it when scenarios swap the entire quote object, not just its value. |

Quotes are `Observable`s; everything that reads them through a handle re-prices automatically when the value changes or the link is replaced. See {doc}`/concepts/quotes-and-observables` for the full observer-cascade model.

## Common patterns

### Update a market value through the observer cascade

```python
import pyquantlib as ql

spot = ql.SimpleQuote(100.0)
# ... build process, option, engine using ql.QuoteHandle(spot) ...

npv1 = option.NPV()       # priced with spot = 100
spot.setValue(105.0)
npv2 = option.NPV()       # automatically re-priced with spot = 105
```

`setValue()` is the canonical way to walk a quote across a scenario or shock. It mutates the underlying number; downstream observers (handles, processes, engines) are notified once.

### Build a derived quote from a Python callable

```python
spot    = ql.SimpleQuote(100.0)
shifted = ql.DerivedQuote(ql.QuoteHandle(spot), lambda x: x + 5.0)

print(spot.value(), shifted.value())   # 100.0 105.0
spot.setValue(120.0)
print(shifted.value())                 # 125.0
```

`DerivedQuote` and `CompositeQuote` accept any Python callable. The callable runs every time the derived quote is evaluated; results are not cached at the binding level. For an expensive `f`, cache externally.

### Swap the entire underlying quote with `RelinkableQuoteHandle`

```python
spot       = ql.SimpleQuote(100.0)
relinkable = ql.RelinkableQuoteHandle(spot)
# ... build process, option, engine using `relinkable` ...

relinkable.linkTo(ql.SimpleQuote(105.0))   # everything re-prices
```

`linkTo()` replaces the `Quote` object that the handle points at; observers are notified once. Use this when the structure of the quote itself changes (e.g. swap a `SimpleQuote` for a `CompositeQuote`); use `setValue()` when only the number changes. See {doc}`/cookbook/scenario-analysis` for the full pattern with curves and surfaces.

## Reference

### Mutable quotes

```{eval-rst}
.. autoclass:: pyquantlib.SimpleQuote
```

### Derived quotes

```{eval-rst}
.. autoclass:: pyquantlib.DerivedQuote
```

```{eval-rst}
.. autoclass:: pyquantlib.CompositeQuote
```

```{eval-rst}
.. autoclass:: pyquantlib.MultiCompositeQuote
```

```python
s1 = ql.SimpleQuote(100.0)
s2 = ql.SimpleQuote(110.0)
s3 = ql.SimpleQuote(120.0)

avg = ql.MultiCompositeQuote(
    [ql.QuoteHandle(s1), ql.QuoteHandle(s2), ql.QuoteHandle(s3)],
    lambda vals: sum(vals) / len(vals),
)
print(avg.value())    # 110.0
```

### FX vol quotes

```{eval-rst}
.. autoclass:: pyquantlib.DeltaVolQuote
```

`DeltaVolQuote` holds an FX volatility tied to a specific delta and maturity. Two constructors are available: one for delta quotes and one for ATM quotes. `DeltaType` and `AtmType` enums encode the market conventions.

```python
# Delta quote (e.g. 25-delta put, spot-delta convention)
q = ql.DeltaVolQuote(
    delta=-0.25, vol=ql.QuoteHandle(ql.SimpleQuote(0.12)),
    maturity=1.0, deltaType=ql.DeltaVolQuote.Spot,
)

# ATM quote
atm = ql.DeltaVolQuote(
    vol=ql.QuoteHandle(ql.SimpleQuote(0.10)),
    deltaType=ql.DeltaVolQuote.Spot, maturity=1.0,
    atmType=ql.DeltaVolQuote.AtmDeltaNeutral,
)
```

`DeltaVolQuote` instances are the input quotes for {py:class}`pyquantlib.BlackVolatilitySurfaceDelta`.

### Handles

```{eval-rst}
.. autoclass:: pyquantlib.QuoteHandle
```

```{eval-rst}
.. autoclass:: pyquantlib.RelinkableQuoteHandle
```

## See also

- {doc}`/concepts/quotes-and-observables`: hidden vs relinkable handles, the observer cascade
- {doc}`/handles`: handle ownership rules and lifetime
- {doc}`/cookbook/scenario-analysis`: relinking handles for scenario sweeps
