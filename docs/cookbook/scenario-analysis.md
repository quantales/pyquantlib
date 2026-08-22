# Scenario analysis with `RelinkableHandle`

Demonstrates the binding pattern for swapping market data without rebuilding the option, the process, or the engine. `RelinkableHandle` wraps a term structure (or quote), and `linkTo(new_object)` atomically replaces the underlying. The observer cascade re-prices on the next `NPV()` call.

## Code

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today = ql.Settings.evaluationDate
dc    = ql.Actual365Fixed()

# All four market-data inputs go in via relinkable handles.
spot_h = ql.RelinkableQuoteHandle(ql.SimpleQuote(100.0))
rf_h   = ql.RelinkableYieldTermStructureHandle(
    ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
)
dq_h   = ql.RelinkableYieldTermStructureHandle(
    ql.FlatForward(today, ql.SimpleQuote(0.0), dc)
)
vol_h  = ql.RelinkableBlackVolTermStructureHandle(
    ql.BlackConstantVol(today, ql.TARGET(), ql.SimpleQuote(0.20), dc)
)

# Process and engine consume the handles, not the underlying objects.
process = ql.GeneralizedBlackScholesProcess(spot_h, dq_h, rf_h, vol_h)
option  = ql.VanillaOption(
    ql.PlainVanillaPayoff(ql.Call, 100.0),
    ql.EuropeanExercise(today + ql.Period("1Y")),
)
engine = ql.AnalyticEuropeanEngine(process)
option.setPricingEngine(engine)

# Base case
print(f"Base case (S=100, vol=20%):              {option.NPV():.4f}")

# Scenario 1: spot up
spot_h.linkTo(ql.SimpleQuote(105.0))
print(f"After spot to 105:                       {option.NPV():.4f}")

# Scenario 2: spot down
spot_h.linkTo(ql.SimpleQuote(95.0))
print(f"After spot to 95:                        {option.NPV():.4f}")

# Scenario 3: vol shock (swap the whole vol structure)
spot_h.linkTo(ql.SimpleQuote(100.0))
vol_h.linkTo(ql.BlackConstantVol(today, ql.TARGET(), ql.SimpleQuote(0.30), dc))
print(f"Spot back to 100, vol up to 30%:         {option.NPV():.4f}")

# Scenario 4: rate shock
vol_h.linkTo(ql.BlackConstantVol(today, ql.TARGET(), ql.SimpleQuote(0.20), dc))
rf_h.linkTo(ql.FlatForward(today, ql.SimpleQuote(0.10), dc))
print(f"Vol back to 20%, rate up to 10%:         {option.NPV():.4f}")
```

## Output

```
Base case (S=100, vol=20%):              10.4506
After spot to 105:                       13.8579
After spot to 95:                        7.5109
Spot back to 100, vol up to 30%:         14.2313
Vol back to 20%, rate up to 10%:         13.2697
```

## Key points

- **The option, the process, and the engine are built once.** No rebuild is needed across scenarios; `linkTo()` triggers the observer cascade and the next `NPV()` re-prices.
- **`RelinkableHandle` swaps the entire object behind the handle.** This differs from `SimpleQuote.setValue()`, which only updates the value within an existing quote. Use `linkTo` when the structure itself changes (e.g. swap a flat vol surface for a smile surface, or swap one curve for another); use `setValue` when only a number changes.
- **All four market inputs are relinkable.** `spot_h`, `rf_h`, `dq_h`, `vol_h` are all `Relinkable*Handle`. `GeneralizedBlackScholesProcess` accepts them because the binding overload takes handle types.

## Pitfalls

- **Mixing relinkable and non-relinkable handles in one process constructor will not dispatch.** The pybind11 overload set is resolved by handle type. Pass either *all* relinkable handles or *all* hidden handles (where bare `SimpleQuote` / `FlatForward` objects are auto-wrapped). Mixing the two raises a no-matching-overload error. See {doc}`/concepts/quotes-and-observables` for the hidden-handle pattern.
- **The replacement object must outlive the handle.** `vol_h.linkTo(ql.BlackConstantVol(...))` works because the handle takes shared ownership; the temporary survives. Storing the replacement in a Python variable first is also fine and clearer in long scenario loops.
- **`linkTo` notifies observers; `Settings.evaluationDate = ...` does too.** A scenario sweep that changes the evaluation date shifts the discount curve out from under the engine, even if no handle is touched. Pin the eval date before the sweep, or relink the curves to fresh structures dated from each scenario's date.

## See also

- {doc}`/concepts/quotes-and-observables`: hidden vs relinkable handles, the observer cascade
- {doc}`/concepts/term-structures`: what `YieldTermStructure` and `BlackVolTermStructure` expose
- {doc}`compare-engines`: the same option, different engines (no handles needed)
