# Calibration

**Calibration** is the process of fitting a model's free parameters to observed market prices. The goal is a Heston model that prices today's vanilla quotes correctly, or a short-rate model that reprices today's swaption volatility cube. Calibration is the loop that makes that happen.

QuantLib structures it as three collaborating objects: a **calibrated model** holding tunable parameters, a list of **calibration helpers** that compare a model price to a market price, and an **optimization method** that drives the parameters to minimize the loss.

## The triangle

```{mermaid}
flowchart LR
    Market[Market quotes<br/>strikes, vols, swaption matrix]
    Helpers[Calibration helpers<br/>HestonModelHelper, SwaptionHelper, ...]
    Model[Calibrated model<br/>HestonModel, HullWhite, G2, ...]
    Optimizer[Optimization method<br/>LevenbergMarquardt, Simplex, BFGS, ...]
    Criteria[End criteria<br/>maxIterations, tolerance]

    Market --> Helpers
    Helpers --> Model
    Optimizer --> Model
    Criteria --> Model
    Model -- adjusts params --> Helpers
    Helpers -- residuals --> Model
```

## How it looks in code

```python
# 1) Set up the model with initial parameters
process = ql.HestonProcess(risk_free, dividend, spot,
                            v0=0.04, kappa=1.0, theta=0.04, sigma=0.5, rho=-0.7)
model   = ql.HestonModel(process)
engine  = ql.AnalyticHestonEngine(model)

# 2) Build helpers from market quotes (one per strike × expiry)
helpers = []
for expiry, strike, market_vol in market_data:
    helper = ql.HestonModelHelper(
        ql.Period(expiry, ql.Days),
        calendar,
        spot.value(),
        strike,
        ql.QuoteHandle(ql.SimpleQuote(market_vol)),
        risk_free, dividend,
    )
    helper.setPricingEngine(engine)
    helpers.append(helper)

# 3) Run the optimization
optimizer = ql.LevenbergMarquardt(epsfcn=1e-8, xtol=1e-8, gtol=1e-8)
end_crit  = ql.EndCriteria(maxIterations=500, maxStationaryStateIterations=50,
                            rootEpsilon=1e-8, functionEpsilon=1e-8, gradientNormEpsilon=1e-8)
model.calibrate(helpers, optimizer, end_crit)

# 4) Read back fitted parameters
print(f"v0={process.v0()}, kappa={process.kappa()}, theta={process.theta()}, "
      f"sigma={process.sigma()}, rho={process.rho()}")
```

## Common pitfalls

- **Parameter constraints**: parameter bounds (positivity, $|\rho| \le 1$, Feller, ...) are passed via `Constraint` objects (`PositiveConstraint`, `BoundaryConstraint`, `CompositeConstraint`). Without an explicit constraint, the optimizer can stray into invalid regions.
- **Unweighted helpers**: by default each helper contributes equally to the loss. Pass explicit weights to `calibrate(helpers, optimizer, end_crit, weights)` when relevant.
- **Reading parameters from the wrong object**: some models (`HestonModel`) store the process as a sub-object. Read fitted parameters from `model.process()`, not from a stale `process` reference held in user code.

## Calibration is observable too

Because helpers hold handles to term structures, the same Observer cascade ({doc}`quotes-and-observables`) applies. Re-running `calibrate()` after bumping a market quote does the right thing automatically; rebuilding helpers is not required.

## See also

- {doc}`/api/models`: calibratable models (`HestonModel`, `HullWhite`, `G2`, `MarkovFunctional`, ...)
- {doc}`/api/math`: optimizers, constraints, end criteria
- {doc}`/concepts/stochastic-processes`: what each process's parameters mean
- {doc}`/cookbook/index`: Heston calibration recipe
