# Cookbook

Self-contained recipes for the workflows that show up in real binding usage. Each recipe is a complete, runnable script: paste into a Python REPL with PyQuantLib installed and it works.

Where the {doc}`/quickstart` shows the basics and the {doc}`/api/index` is a reference, recipes sit in between: real tasks with real numbers and the binding-level patterns that go with them.

```{toctree}
:maxdepth: 1

compare-engines
mc-engine-kwargs
mc-convergence
spread-option-engines
scenario-analysis
bootstrap-yield-curve
piecewise-mixed-helpers
vol-surface
heston-calibration
american-fd
numpy-interop
```

## Recipe index

| Recipe | What it shows |
|---|---|
| {doc}`compare-engines` | Swap analytic, MC, and FD engines on a single `VanillaOption` via `setPricingEngine()`. |
| {doc}`mc-engine-kwargs` | The `MCEuropeanEngine` factory: `rngType`, seed reproducibility, antithetic, `requiredTolerance`. |
| {doc}`mc-convergence` | Sweep `requiredSamples` across MT, MT-antithetic, and Sobol; compare convergence rates against the analytic reference. |
| {doc}`spread-option-engines` | Built-in `KirkEngine` (C++) vs pure-Python `ModifiedKirkEngine` from `pyquantlib.extensions`, attached the same way. |
| {doc}`scenario-analysis` | `RelinkableHandle` to swap market data without rebuilding the option, process, or engine. |
| {doc}`bootstrap-yield-curve` | Build a `PiecewiseLogLinearDiscount` curve from deposit + swap rate helpers and inspect DFs / zero / forward rates. |
| {doc}`piecewise-mixed-helpers` | The same `PiecewiseLogLinearDiscount` curve fed with deposits, FRAs (`FraRateHelper`), and swaps together; pillar-ordering rules. |
| {doc}`vol-surface` | Build a `BlackVarianceSurface` from an expiry-by-strike vol grid and use it inside a `GeneralizedBlackScholesProcess`. |
| {doc}`heston-calibration` | Calibrate `HestonModel` to a vol grid with `HestonModelHelper` and `LevenbergMarquardt`. |
| {doc}`american-fd` | Price an American put with `FdBlackScholesVanillaEngine`; cross-check against analytic approximations and a binomial tree. |
| {doc}`numpy-interop` | The narrow binding-level interop (`Array` / `Matrix` ↔ ndarray) plus the scalar-loop pattern for getting QuantLib results into NumPy arrays. |

