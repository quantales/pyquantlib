# Calibrate a Heston model

Demonstrates the binding pattern for model calibration: build a `HestonModel` with an initial guess, wrap each market quote in a `HestonModelHelper`, attach a model-based pricing engine to every helper, then call `calibrate()` with an `OptimizationMethod` and an `EndCriteria`.

## Code

```python
import pyquantlib as ql

ql.Settings.evaluationDate = ql.Date(15, 6, 2025)
today    = ql.Settings.evaluationDate
calendar = ql.TARGET()
dc       = ql.Actual365Fixed()

s0 = 100.0
r  = 0.05
q  = 0.0

spot = ql.QuoteHandle(ql.SimpleQuote(s0))
rf   = ql.YieldTermStructureHandle(ql.FlatForward(today, ql.SimpleQuote(r), dc))
dq   = ql.YieldTermStructureHandle(ql.FlatForward(today, ql.SimpleQuote(q), dc))

# Synthetic market: 4 expiries x 5 strikes of Black implied vols.
expiries = ["3M", "6M", "1Y", "2Y"]
strikes  = [80.0, 90.0, 100.0, 110.0, 120.0]
vol_data = [
    [0.30, 0.27, 0.26, 0.27, 0.30],
    [0.28, 0.25, 0.24, 0.25, 0.28],
    [0.26, 0.23, 0.22, 0.23, 0.26],
    [0.25, 0.22, 0.21, 0.22, 0.25],
]

# Initial Heston parameters. The optimiser refines from here.
v0, kappa, theta, sigma, rho = 0.04, 1.5, 0.04, 0.5, -0.5

process = ql.HestonProcess(rf, dq, spot, v0, kappa, theta, sigma, rho)
model   = ql.HestonModel(process)
engine  = ql.AnalyticHestonEngine(model)

# One helper per quote. Each helper carries its own market vol; the
# engine attached to it uses the *model* to produce the model price.
helpers = []
for i, exp_str in enumerate(expiries):
    for j, k in enumerate(strikes):
        h = ql.HestonModelHelper(
            ql.Period(exp_str), calendar, s0, k,
            ql.QuoteHandle(ql.SimpleQuote(vol_data[i][j])),
            rf, dq,
        )
        h.setPricingEngine(engine)
        helpers.append(h)

# Optimisation: Levenberg-Marquardt with reasonable tolerances.
lm = ql.LevenbergMarquardt(1e-8, 1e-8, 1e-8)
ec = ql.EndCriteria(
    maxIterations=500,
    maxStationaryStateIterations=50,
    rootEpsilon=1e-8,
    functionEpsilon=1e-8,
    gradientNormEpsilon=1e-8,
)

model.calibrate(helpers, lm, ec)

# Read calibrated parameters via the named accessors. params() returns
# them in (theta, kappa, sigma, rho, v0) order, which differs from the
# constructor order. Use the named accessors to avoid confusion.
print("Calibrated parameters:")
print(f"  v0    = {model.v0():.4f}")
print(f"  kappa = {model.kappa():.4f}")
print(f"  theta = {model.theta():.4f}")
print(f"  sigma = {model.sigma():.4f}")
print(f"  rho   = {model.rho():.4f}")

# Calibration error per helper, then root-mean-square.
errors = [h.calibrationError() for h in helpers]
rmse   = (sum(e * e for e in errors) / len(errors)) ** 0.5
print(f"\nRMSE over {len(helpers)} quotes:  {rmse:.6f}")
```

## Output

```
Calibrated parameters:
  v0    = 0.0804
  kappa = 0.9813
  theta = 0.0634
  sigma = 0.9996
  rho   = 0.1394

RMSE over 20 quotes:  0.048665
```

(Exact values are sensitive to the initial guess and to the optimiser tolerances; the patterns are stable. With a non-symmetric smile the calibrated `rho` would carry the same sign as the skew.)

## Key points

- **Helpers are the canonical observation interface.** A `HestonModelHelper` knows three things: the market quote (`vol`), how to compute the model price (via the `engine` attached to it), and how to compare the two (`calibrationError()`). The optimiser does not see the model directly: it sees the helpers.
- **Every helper needs an engine.** `engine = ql.AnalyticHestonEngine(model)` is constructed once and attached to every helper. The engine reads the model's *current* parameter vector at each pricing call, so the same engine instance produces different prices as `calibrate()` updates the parameters.
- **`calibrate()` is the main loop.** It hands the parameter vector to the optimiser, asks the optimiser for a step, pushes the new parameters back into the model, re-prices every helper, and aggregates the errors. This loop is hidden behind the single `calibrate()` call.
- **`EndCriteria` is multi-axis.** Iterations, stationary iterations, root step, function step, gradient norm: any of them tripping ends the optimisation. Loose tolerances exit faster but accept worse fits; tight ones often run to `maxIterations`.

## Pitfalls

- **`params()` order is alphabetical, not the constructor order.** `model.params()` returns `(theta, kappa, sigma, rho, v0)`, but `HestonProcess(...)` takes them as `(v0, kappa, theta, sigma, rho)`. Use the named accessors (`model.v0()`, `model.kappa()`, etc.) to avoid silent unpacking bugs.
- **Forgetting `setPricingEngine` on the helpers** raises `"calibration helper has no pricing engine"` at the first model price. Every helper needs the engine; build a list, loop, set, then pass.
- **Heston has weak corner identifiability.** A symmetric smile (left wing == right wing) leaves `rho` near zero with weak gradient; the optimiser may stall or land at a positive value if the initial guess is positive. For real fits, seed `rho` with the sign of the observed skew (negative for equity, positive for some commodities).
- **The optimiser is local, not global.** `LevenbergMarquardt` finds a local minimum; the result depends on the initial guess. For production calibration, run from several starting points and keep the lowest RMSE, or use a global wrapper (`DifferentialEvolution`, simulated annealing) before refining locally.

## See also

- {doc}`/api/models`: `HestonModel`, `HestonModelHelper`, related calibrated models
- {doc}`/api/pricingengines`: Heston engines (`AnalyticHestonEngine`, `COSHestonEngine`, FD variants) that can drive the helpers
- {doc}`/concepts/calibration`: optimisers, end criteria, and constraints in PyQuantLib
- {doc}`vol-surface`: building the input quote grid that feeds calibration
