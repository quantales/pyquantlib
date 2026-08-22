# Quotes and Observables

A **quote** is a single market data point (a spot price, a rate, a volatility) wrapped in an object that broadcasts changes. When the quote's value updates, every dependent calculation knows about it and re-prices on demand. This is QuantLib's reactive backbone, and understanding it is the difference between writing scripts that work and scripts that re-price correctly.

## The Observer pattern

Quotes are **Observables**. Term structures, processes, and pricing engines that depend on them are **Observers**. When `setValue()` is called, the quote notifies its observers, who mark themselves dirty. The next time anyone asks for an NPV, the dependency graph re-evaluates only the dirty parts.

```{mermaid}
sequenceDiagram
    participant User
    participant Q as SimpleQuote
    participant C as FlatForward
    participant P as BSProcess
    participant E as AnalyticEngine
    participant V as VanillaOption

    User->>Q: setValue 0.06
    Q-->>C: notify
    C-->>P: notify
    P-->>E: notify
    E-->>V: notify
    Note over V: marked dirty
    User->>V: NPV
    V->>E: calculate
    Note over E, V: re-prices using new rate
    E-->>V: result
    V-->>User: 11.2304
```

The cascade is **lazy**: notifications mark observers dirty but don't trigger work. The work only happens when a result is read. This is what makes scenario analysis cheap. Calling `setValue()` on ten quotes in a loop incurs only one re-pricing at the end.

## Quote variants

| Class | Purpose |
|---|---|
| `SimpleQuote` | The everyday workhorse. Holds a value, supports `setValue()` and `reset()`. |
| `DerivedQuote` | A function of one input quote (e.g., a quote that's always 2× another). |
| `CompositeQuote` | A function of two input quotes (e.g., a spread between two rates). |

For more complex live-feed integration, the abstract `Quote` base from `pyquantlib.base` can be subclassed with `value()` and `isValid()` overrides; see {doc}`/extending`.

## Why this matters in practice

**Scenario analysis without rebuilding the world**:

```python
spot = ql.SimpleQuote(100.0)
# ... build process, engine, option using `spot` directly ...

# Bump-and-reprice for delta
base = option.NPV()
spot.setValue(100.5)
up   = option.NPV()
spot.setValue(99.5)
down = option.NPV()
spot.setValue(100.0)             # reset

delta = (up - down) / 1.0        # finite-difference delta
```

No rebuild of the curve, the process, or the engine. The observer chain handles it.

**Calibration loops**:

Calibration helpers (e.g. `HestonModelHelper`) use the same machinery internally. The optimizer adjusts model parameters; each adjustment notifies the helper's term structure observers; the helper recomputes its model price; the loss function reads the new value. All automatic.

## Handles and observability

A `Handle<T>` is itself observable. When a `RelinkableHandle` is `linkTo()`'d a different object, observers see a single notification, which is the whole point of the relink mechanism. This is why "swap out the curve" works without rebuilding anything downstream.

The hidden-handle convenience (passing a `SimpleQuote` directly where a `Handle<Quote>` is expected) preserves this: PyQuantLib creates a non-relinkable handle internally, and the underlying quote remains mutable through `setValue()`. An explicit `RelinkableHandle` is only required when the entire object needs to be swapped, not just its value.

## Common pitfalls

- **Mutating shared state**: `SimpleQuote` is mutable. Passing the same quote into two unrelated calculations and bumping it updates both. Usually intended; sometimes a footgun.
- **Forgetting `setValue()` is silent**: there's no return value or error if the quote isn't observed by anything. The cascade just doesn't happen. Always verify that the intended object actually re-prices.
- **Custom Quote subclasses with broken `isValid()`**: term structures call `isValid()` and will silently use stale values if it returns `True` when the quote isn't ready.

## See also

- {doc}`/api/quotes`: full class reference
- {doc}`/handles`: `Handle` and `RelinkableHandle` semantics
- {doc}`/extending`: subclassing `Quote` for custom data sources
