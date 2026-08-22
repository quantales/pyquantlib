# Monte Carlo convergence study

Demonstrates the binding pattern for sweeping `requiredSamples` across a range and comparing MT (`pseudorandom`), MT with antithetic variance reduction, and Sobol QMC (`lowdiscrepancy`) against an analytic reference. Each price is one `setPricingEngine()` + `NPV()` call; the loop is in Python.

## Code

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today = ql.Settings.evaluationDate
dc    = ql.Actual365Fixed()

spot = ql.SimpleQuote(100.0)
rf  = ql.FlatForward(today, ql.SimpleQuote(0.05), dc)
dq  = ql.FlatForward(today, ql.SimpleQuote(0.0), dc)
v   = ql.BlackConstantVol(today, ql.TARGET(), ql.SimpleQuote(0.20), dc)
process = ql.GeneralizedBlackScholesProcess(spot, dq, rf, v)

option = ql.VanillaOption(
    ql.PlainVanillaPayoff(ql.Call, 100.0),
    ql.EuropeanExercise(today + ql.Period("1Y")),
)

# Reference: analytic Black-Scholes.
option.setPricingEngine(ql.AnalyticEuropeanEngine(process))
ref = option.NPV()
print(f"Reference (analytic): {ref:.6f}")

# Sweep over sample counts. timeSteps=1 is correct for a European
# payoff: only the terminal value matters.
ns = [1024, 4096, 16384, 65536, 262144]

print()
print(f"{'N':>10}{'MT plain':>12}{'|err|':>10}"
      f"{'MT anti':>12}{'|err|':>10}"
      f"{'Sobol':>12}{'|err|':>10}")
print("-" * 76)
for n in ns:
    option.setPricingEngine(ql.MCEuropeanEngine(
        process, "pseudorandom", timeSteps=1,
        requiredSamples=n, seed=42,
    ))
    mt = option.NPV()

    option.setPricingEngine(ql.MCEuropeanEngine(
        process, "pseudorandom", timeSteps=1,
        antitheticVariate=True, requiredSamples=n, seed=42,
    ))
    anti = option.NPV()

    option.setPricingEngine(ql.MCEuropeanEngine(
        process, "lowdiscrepancy", timeSteps=1, requiredSamples=n,
    ))
    sobol = option.NPV()

    print(
        f"{n:>10}"
        f"{mt:>12.4f}{abs(mt - ref):>10.5f}"
        f"{anti:>12.4f}{abs(anti - ref):>10.5f}"
        f"{sobol:>12.4f}{abs(sobol - ref):>10.5f}"
    )
```

## Output

```
Reference (analytic): 10.450584

         N    MT plain     |err|     MT anti     |err|       Sobol     |err|
----------------------------------------------------------------------------
      1024     10.6423   0.19176     10.6175   0.16695     10.3986   0.05199
      4096     10.4365   0.01404     10.4478   0.00279     10.4358   0.01476
     16384     10.3086   0.14200     10.4334   0.01718     10.4465   0.00413
     65536     10.4277   0.02288     10.4233   0.02732     10.4494   0.00114
    262144     10.4304   0.02022     10.4379   0.01264     10.4503   0.00031
```

(Exact MT numbers depend on the QuantLib build and platform; the pattern, MT noisy at all N while Sobol falls off cleanly, is stable.)

## Key points

- **MT (pseudorandom) error scales as `1/sqrt(N)` *in expectation*.** At any single seed the realised error bounces (the MT row above goes 0.19, 0.01, 0.14, 0.02, 0.02 as N grows). This is statistical noise, not a convergence problem; averaging the absolute error over many seeds at each N would show the `1/sqrt(N)` envelope.
- **Antithetic halves the variance for free on smooth payoffs.** Each random draw is used both as `Z` and `−Z`, so the call payoff (which has odd symmetry around the forward) gets some of its variance cancelled. The "MT anti" column tracks closer to the reference at small N than "MT plain" and rarely worse.
- **Sobol (lowdiscrepancy) converges much faster than MT for smooth, low-dimensional payoffs.** Each 4x increase in N drops the Sobol error roughly 4x (from 0.052 down to 0.0003 over the 256x range above), close to a 1/N rate rather than the 1/sqrt(N) of MT. Sobol is deterministic, so re-running gives bit-identical results; the seed argument is ignored.
- **A single `option` is repriced through six engine swaps per N.** The instrument, payoff, exercise, and process are all built once. `setPricingEngine()` discards the previous engine each time; the loop is the canonical pattern for batch convergence studies.

## Pitfalls

- **`option.errorEstimate()` is not exposed in the binding.** The MC engine internally tracks the standard error of its sample mean, but the option's `OneAssetOption.results` object does not surface it; see the binding gap log. Convergence diagnostics either compute `|MC − analytic|` (when an analytic reference exists) or vary the seed and look at the spread.
- **Comparing MT and Sobol at one seed is misleading.** A single MT run is one realisation of a random sample; a single Sobol run is the deterministic answer. Averaging MT over multiple seeds at each N gives the right picture.
- **Sobol at low dimensions wins; at high dimensions it can lose.** For path-dependent payoffs with hundreds of time steps, Sobol's effective dimensionality erodes the QMC advantage. The fix is the Brownian-bridge variant (`SobolBrownianBridgeRsg` and friends, see {doc}`/concepts/random-numbers`), not switching back to MT.

## See also

- {doc}`mc-engine-kwargs`: the underlying `MCEuropeanEngine` factory and its kwargs
- {doc}`compare-engines`: the same one-instrument-many-engines pattern across analytic / MC / FD
- {doc}`/concepts/random-numbers`: the layered Rng / Rsg / Brownian-bridge architecture
