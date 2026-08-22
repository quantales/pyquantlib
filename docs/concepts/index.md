# Concepts

Mental models for working with PyQuantLib. Each page is a short, self-contained explanation of one quantitative-finance concept and how it maps to the library.

These pages assume basic familiarity with derivatives pricing. Readers new to QuantLib should start with {doc}`/quickstart` first.

```{toctree}
:maxdepth: 1

term-structures
quotes-and-observables
pricing-engines
stochastic-processes
calibration
random-numbers
finite-difference
bridge-pattern-types
```

## What's covered

| Page | What it explains |
|---|---|
| {doc}`term-structures` | Yield curves, vol surfaces, credit curves; the abstract base hierarchy and when to pick which concrete class. |
| {doc}`quotes-and-observables` | The Observer pattern, how `setValue()` cascades, why this matters for repricing and calibration. |
| {doc}`pricing-engines` | Analytic vs Monte Carlo vs finite-difference vs lattice; decision matrix by instrument. |
| {doc}`stochastic-processes` | BSM, Heston, Bates, Hull-White, G2, hybrid; what each model captures. |
| {doc}`calibration` | The helper / model / optimizer triangle; how calibration loops actually work. |
| {doc}`random-numbers` | Pseudo-random vs quasi-random, MT vs Sobol vs Halton, Brownian bridge, antithetic variance reduction. |
| {doc}`finite-difference` | Mesher, operator, scheme, boundary conditions; when FD beats MC. |
| {doc}`bridge-pattern-types` | Why `Calendar` and `DayCounter` aren't quite value types, and the import-time traps that follow. |
