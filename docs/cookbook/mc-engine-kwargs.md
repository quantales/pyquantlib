# MC engine kwargs

The `MCEuropeanEngine` factory takes a string `rngType` plus several variance-reduction and sample-control kwargs. This recipe shows what each does at the binding level: pseudo-random vs low-discrepancy, antithetic, seed reproducibility, sample-count vs tolerance.

## Code

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today = ql.Settings.evaluationDate
dc    = ql.Actual365Fixed()

spot = ql.SimpleQuote(100.0)
rate = ql.SimpleQuote(0.05)
vol  = ql.SimpleQuote(0.20)
risk_free  = ql.FlatForward(today, rate, dc)
dividend   = ql.FlatForward(today, ql.SimpleQuote(0.0), dc)
volatility = ql.BlackConstantVol(today, ql.TARGET(), vol, dc)
process    = ql.GeneralizedBlackScholesProcess(spot, dividend, risk_free, volatility)

option = ql.VanillaOption(
    ql.PlainVanillaPayoff(ql.Call, 100.0),
    ql.EuropeanExercise(today + ql.Period("1Y")),
)

# Reference: analytic Black-Scholes
option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
analytic_npv = option.NPV()
print(f"Analytic                                {analytic_npv:.4f}")

# Pseudo-random with seed=42 (reproducible).
# timeSteps=1 is appropriate for a European payoff: only the
# terminal value matters, so a single jump to maturity suffices.
mc_pr = ql.MCEuropeanEngine(
    process, "pseudorandom",
    timeSteps=1, requiredSamples=100_000, seed=42,
)
option.setPricingEngine(mc_pr)
print(f"PR  100k 1-step, seed=42                 {option.NPV():.4f}")

# Same kwargs, same seed: identical result (binding is reproducible)
option.setPricingEngine(ql.MCEuropeanEngine(
    process, "pseudorandom",
    timeSteps=1, requiredSamples=100_000, seed=42,
))
print(f"PR  100k 1-step, seed=42 (rerun)         {option.NPV():.4f}")

# Different seed: different result
option.setPricingEngine(ql.MCEuropeanEngine(
    process, "pseudorandom",
    timeSteps=1, requiredSamples=100_000, seed=7,
))
print(f"PR  100k 1-step, seed=7                  {option.NPV():.4f}")

# Antithetic variance reduction
mc_anti = ql.MCEuropeanEngine(
    process, "pseudorandom",
    timeSteps=1, antitheticVariate=True, requiredSamples=100_000, seed=42,
)
option.setPricingEngine(mc_anti)
print(f"PR  100k 1-step, antithetic, seed=42     {option.NPV():.4f}")

# Low-discrepancy (Sobol). seed is ignored here.
mc_qmc = ql.MCEuropeanEngine(
    process, "lowdiscrepancy",
    timeSteps=1, requiredSamples=16_384,
)
option.setPricingEngine(mc_qmc)
print(f"QMC 16k 1-step (Sobol)                   {option.NPV():.4f}")

# Sobol again with 4x the samples: convergence keeps improving deterministically.
mc_qmc2 = ql.MCEuropeanEngine(
    process, "lowdiscrepancy",
    timeSteps=1, requiredSamples=65_536,
)
option.setPricingEngine(mc_qmc2)
print(f"QMC 64k 1-step (Sobol)                   {option.NPV():.4f}")

# Tolerance-driven instead of fixed sample count
mc_tol = ql.MCEuropeanEngine(
    process, "pseudorandom",
    timeSteps=1, requiredTolerance=0.02, maxSamples=1_000_000, seed=42,
)
option.setPricingEngine(mc_tol)
print(f"PR  tolerance=0.02 (auto-stops)          {option.NPV():.4f}")
```

## Output

```
Analytic                                 10.4506
PR  100k 1-step, seed=42                 10.4201
PR  100k 1-step, seed=42 (rerun)         10.4201
PR  100k 1-step, seed=7                  10.4745
PR  100k 1-step, antithetic, seed=42     10.4295
QMC 16k 1-step (Sobol)                   10.4465
QMC 64k 1-step (Sobol)                   10.4494
PR  tolerance=0.02 (auto-stops)          10.4726
```

(Exact values depend on the QuantLib build and platform; only the *patterns* (same-seed reproducibility, antithetic variance reduction, QMC accuracy at low N) are stable across runs.)

## Key points

- **`rngType`** picks the random-number pipeline. `"pseudorandom"` uses Mersenne Twister; `"lowdiscrepancy"` uses Sobol. The string is lowercase; the binding does not accept other casings.
- **`seed` only affects `"pseudorandom"`.** Same seed + same kwargs gives byte-identical results across runs. The Sobol pipeline ignores `seed` (it's a deterministic sequence anyway).
- **`antitheticVariate=True`** is a cheap variance reduction: each random draw is used both as $Z$ and $-Z$. Almost always worth turning on for `"pseudorandom"`. For `"lowdiscrepancy"` it's typically unnecessary.
- **`requiredSamples` and `requiredTolerance` are mutually exclusive** at the C++ level. Pass one or the other (the binding accepts both as kwargs but the engine uses whichever is non-`None`). With `requiredTolerance`, the engine grows the sample count until the standard error drops below the target, capped by `maxSamples`.
- **`timeSteps` vs `timeStepsPerYear`** are also alternatives. The Python kwargs accept `None` for "unused"; the engine picks based on which is set.

## Pitfalls

- **The engine reference must be kept alive.** Inline construction inside `setPricingEngine(...)` lets Python collect the engine; subsequent `NPV()` calls then "tried to call pure virtual function". Bind to a name first.
- **Don't compare prices across `rngType` at the same `requiredSamples`.** A price difference between MT and Sobol at $N = 10^5$ is convergence noise of MT, not a bug. Sobol at $N = 16{,}384$ often beats MT at $N = 10^6$ for vanilla payoffs.
- **`seed=0` means "random seed"** in the binding (per the function docstring). For reproducibility, pass any nonzero seed.

## See also

- {doc}`/concepts/random-numbers`: the Rng vs Rsg layered architecture and what's exposed at each layer
- {doc}`/api/pricingengines`: all MC engine bindings
- {doc}`compare-engines`: comparing MC against analytic and FD on the same option
