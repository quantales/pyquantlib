# Stochastic Processes

A **stochastic process** is the mathematical model of how a market quantity evolves through time. Every Monte Carlo and finite-difference engine in QuantLib is built on top of one: the process supplies the drift and diffusion, and the engine evolves it through time to compute a payoff.

In code, a process is just an object with `drift(t, x)`, `diffusion(t, x)`, and `evolve(t, x, dt, dW)` methods. Concrete processes implement specific dynamics: geometric Brownian motion for Black-Scholes, mean-reverting variance for Heston, two-factor short rate for G2.

## The hierarchy

```{mermaid}
classDiagram
    class StochasticProcess {
        +drift(t, x) Array
        +diffusion(t, x) Matrix
        +evolve(t, x, dt, dw) Array
    }
    class StochasticProcess1D {
        +drift(t, x) Real
        +diffusion(t, x) Real
    }
    StochasticProcess <|-- StochasticProcess1D

    class GeneralizedBlackScholesProcess
    class HestonProcess
    class BatesProcess
    class HullWhiteProcess
    class GsrProcess
    class G2Process
    class HybridHestonHullWhiteProcess
    class StochasticProcessArray

    StochasticProcess1D <|-- GeneralizedBlackScholesProcess
    StochasticProcess1D <|-- HullWhiteProcess
    StochasticProcess1D <|-- GsrProcess
    StochasticProcess <|-- HestonProcess
    StochasticProcess <|-- BatesProcess
    StochasticProcess <|-- G2Process
    StochasticProcess <|-- HybridHestonHullWhiteProcess
    StochasticProcess <|-- StochasticProcessArray
```

`StochasticProcess1D` is the single-factor specialization (scalar `x`, scalar drift). Multi-factor processes return arrays. `StochasticProcessArray` is a container that wraps multiple 1D processes with a correlation matrix, the standard way to build basket, spread, and multi-asset models.

## How processes plug in

The process is the **input** to a model or to an MC engine. A few common shapes:

```python
# 1) Process feeds an analytic engine directly
process = ql.GeneralizedBlackScholesProcess(spot, dividend, risk_free, vol)
engine  = ql.AnalyticEuropeanEngine(process)

# 2) Process wrapped in a model, model feeds an engine
heston_process = ql.HestonProcess(risk_free, dividend, spot, v0, kappa, theta, sigma, rho)
heston_model   = ql.HestonModel(heston_process)
engine         = ql.AnalyticHestonEngine(heston_model)

# 3) Multiple processes assembled into an array for MC
processes  = [bs_process_1, bs_process_2]
correl     = ql.Matrix([[1.0, 0.7], [0.7, 1.0]])
basket_p   = ql.StochasticProcessArray(processes, correl)
engine     = ql.MCEuropeanBasketEngine(basket_p, ...)
```

Processes and term structures are linked through **handles**. When the underlying yield curve changes, the process re-prices through the same Observer cascade described in {doc}`quotes-and-observables`.

## Local volatility via the same binding

`GeneralizedBlackScholesProcess` accepts a `BlackVolTermStructure`. The same Python class drives both Black-Scholes (with a flat `BlackConstantVol`) and local volatility (with a strike-dependent surface). The choice of vol-structure object passed in determines the dynamics; the process binding is identical. `BlackScholesProcess` and `BlackScholesMertonProcess` are convenience aliases for the constant-rate-and-dividend specializations.

## Common pitfalls

- **Process built once, used long-term**: processes hold *handles* to term structures. As long as the underlying quotes update through the observer chain, the process picks up the changes. Rebuilding is not required.
- **Wrong process for the engine**: an MC engine expects a specific process type. `MCEuropeanEngine` wants `GeneralizedBlackScholesProcess`; `MCEuropeanHestonEngine` wants `HestonProcess`. The error at engine construction is usually clear.
- **Forgetting correlation**: `StochasticProcessArray` requires a correlation matrix that's positive semi-definite. A non-PSD matrix raises at construction.

## See also

- {doc}`/api/processes`: full process reference
- {doc}`/api/models`: process-derived models (Heston, HW, Gsr, G2, etc.)
- {doc}`/concepts/pricing-engines`: which engine accepts which process
- {doc}`calibration`: how to tune process parameters to market data
