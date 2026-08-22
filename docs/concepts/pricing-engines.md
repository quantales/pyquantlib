# Pricing Engines

QuantLib separates **what an instrument is** from **how it's priced**. A `VanillaOption` describes the contract: payoff, exercise, expiry. A `PricingEngine` knows how to value it. An engine is attached to an instrument via `setPricingEngine()`, and the same instrument can be valued multiple ways by swapping engines.

This is one of QuantLib's most important design choices: it allows comparing an analytic price to a Monte Carlo price to a finite-difference price for the *same* contract, with a one-line change.

## The three engine families

```{mermaid}
graph TB
    Instrument[Instrument]
    Engine{PricingEngine}
    Instrument -- setPricingEngine --> Engine

    Engine --> Analytic[Analytic engines<br/>closed-form solutions]
    Engine --> MC[Monte Carlo engines<br/>simulate paths, average payoffs]
    Engine --> FD[Finite-difference engines<br/>solve the pricing PDE on a grid]
    Engine --> Tree[Lattice / tree engines<br/>backward induction on a tree]

    Analytic --> A1[AnalyticEuropeanEngine]
    Analytic --> A2[AnalyticHestonEngine]
    Analytic --> A3[QdPlusAmericanEngine]

    MC --> M1[MCEuropeanEngine]
    MC --> M2[MCBarrierEngine]
    MC --> M3[MCAmericanEngine]

    FD --> F1[FdBlackScholesVanillaEngine]
    FD --> F2[FdHestonVanillaEngine]
    FD --> F3[FdHestonBarrierEngine]

    Tree --> T1[BinomialVanillaEngine]
    Tree --> T2[BinomialBarrierEngine]
```

## How an engine attaches

```python
option = ql.VanillaOption(payoff, exercise)

# Same option, three engines, three answers (which should agree)
option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
analytic_npv = option.NPV()

option.setPricingEngine(ql.MCEuropeanEngine(process, "PseudoRandom",
                                            timeSteps=100, requiredSamples=100_000, seed=42))
mc_npv = option.NPV()

option.setPricingEngine(ql.FdBlackScholesVanillaEngine(process,
                                                       tGrid=100, xGrid=100))
fd_npv = option.NPV()
```

This pattern of one instrument with multiple engines is the standard way to sanity-check exotic pricers, build benchmark tables, and discover modelling bugs. If three engines disagree on a vanilla, one of them has a bug.

## Custom engines in Python

Engines can be written in pure Python by subclassing the appropriate base from `pyquantlib.base`. The `pyquantlib.extensions` module ships two examples (`SviSmileSection`, `ModifiedKirkEngine`) that work as templates.

There's a critical design rule for Python-subclassed engines: **only override the calculation method that takes numeric parameters**, not the parameter-extraction method. The C++ base class extracts parameters from the instrument and passes them as floats to the override, which computes and returns a price. See {doc}`/extending` for the rationale: the rule is enforced because the alternative causes hard-to-debug dangling references.

## See also

- {doc}`/api/pricingengines`: full engine catalog
- {doc}`/extending`: building custom engines in Python
- {doc}`/cookbook/index`: engine comparison recipe
