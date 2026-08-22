# Term Structures

A **term structure** is a time-dependent function that returns a number: a discount factor, a forward rate, a volatility, a hazard rate. They're the foundation of QuantLib's pricing model. Instruments don't store rates and vols directly; they hold references to term structures and ask them for values at the dates they care about.

## The three families

QuantLib has three independent term structure hierarchies, one per market data domain:

```{mermaid}
classDiagram
    class TermStructure
    class YieldTermStructure {
        +discount(date)
        +zeroRate(date)
        +forwardRate(d1, d2)
    }
    class BlackVolTermStructure {
        +blackVol(time, strike)
        +blackVariance(time, strike)
    }
    class DefaultProbabilityTermStructure {
        +survivalProbability(date)
        +defaultProbability(date)
        +hazardRate(date)
    }
    TermStructure <|-- YieldTermStructure
    TermStructure <|-- BlackVolTermStructure
    TermStructure <|-- DefaultProbabilityTermStructure

    class FlatForward
    class ZeroCurve
    class ForwardCurve
    class PiecewiseYieldCurve
    YieldTermStructure <|-- FlatForward
    YieldTermStructure <|-- ZeroCurve
    YieldTermStructure <|-- ForwardCurve
    YieldTermStructure <|-- PiecewiseYieldCurve

    class BlackConstantVol
    class BlackVarianceSurface
    class BlackVarianceCurve
    BlackVolTermStructure <|-- BlackConstantVol
    BlackVolTermStructure <|-- BlackVarianceSurface
    BlackVolTermStructure <|-- BlackVarianceCurve

    class FlatHazardRate
    class PiecewiseDefaultCurve
    DefaultProbabilityTermStructure <|-- FlatHazardRate
    DefaultProbabilityTermStructure <|-- PiecewiseDefaultCurve
```

## How instruments use them

Pricing engines never receive raw rates. They receive **handles** to term structures, so when the underlying curve changes, all dependents re-price automatically through the Observer pattern.

```python
risk_free = ql.FlatForward(today, rate_quote, ql.Actual365Fixed())
process   = ql.GeneralizedBlackScholesProcess(spot, dividend, risk_free, vol)
engine    = ql.AnalyticEuropeanEngine(process)
option.setPricingEngine(engine)

option.NPV()           # uses risk_free, vol, etc.
rate_quote.setValue(0.06)
option.NPV()           # automatically re-prices
```

The {doc}`/handles` page covers the explicit-handle / hidden-handle distinction. The core design rationale is in {doc}`/architecture` ("Hidden Handles" section).

## Reference dates and day counters

Every term structure has a **reference date** (the date at which it's anchored) and a **day counter** that converts dates to year fractions internally. There are two reference-date conventions:

- **Fixed**: pass an explicit `Date` at construction. The structure is anchored to that date forever.
- **Floating** (relative to evaluation date): the structure tracks `Settings.evaluationDate`, so changing the eval date shifts everything.

Most concrete classes have constructor overloads for both. Use floating when a curve should follow the eval date in a multi-date analysis; fixed when the curve represents a frozen historical state.

## Common pitfalls

- **`evaluationDate` not set**: term structures default to *today* if it is never set. Always set `Settings.evaluationDate` explicitly at the top of any script.
- **Discount-before-reference errors**: requesting a discount factor for a date before the structure's reference date throws. Curves don't extrapolate backwards.
- **Empty handles**: a `Handle<YieldTermStructure>()` with no linked structure throws on use. The {doc}`/troubleshooting` page covers the symptoms.

## See also

- {doc}`/api/termstructures`: full class reference
- {doc}`/handles`: hidden-handles vs explicit handles
- {doc}`/cookbook/index`: bootstrapping recipe
