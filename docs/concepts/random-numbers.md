# Random Number Generation

The MC pricing pipeline composes several layers: uniform generator, transformation to Gaussians, optional Brownian bridge, path generator, engine. PyQuantLib exposes each layer as a separate set of bindings.

PyQuantLib follows QuantLib's two-layer architecture: scalar **Rng** generators (`next()` returns one number) and vectorized **Rsg** sequence generators (`nextSequence()` returns the full N-dimensional sample in one C++ call). For Python users this distinction is critical: Rsg is much faster for path generation because each `nextSequence()` is a single C++ call, while Rng-based path generation crosses the Python/C++ boundary on every step.

## The pipeline

```{mermaid}
flowchart LR
    Rng[Uniform RNG / RSG<br/>MersenneTwister<br/>Sobol<br/>Halton]
    Trans[Transformation<br/>Box-Muller<br/>Inverse-CDF]
    Gauss[Gaussian RNG / RSG]
    Bridge[BrownianBridge<br/>BrownianGenerator]
    Path[PathGenerator<br/>MultiPathGenerator]
    Engine[MC engine<br/>averages payoff]

    Rng --> Trans --> Gauss --> Bridge --> Path --> Engine
```

Most users assemble this implicitly: `MCEuropeanEngine(process, "PseudoRandom", ...)` selects an MT-based pipeline, `"LowDiscrepancy"` selects a Sobol pipeline. Direct contact with the pieces is only needed when building a custom MC engine.

## What the bindings expose

| Layer | Bindings |
|---|---|
| Uniform Rng / Rsg | `MersenneTwisterUniformRng`, `SobolRsg` (with `DirectionIntegers` enum), `HaltonRsg`, `Burley2020SobolRsg` |
| Gaussian transformation | `BoxMullerGaussianRng`, `GaussianRandomGenerator`, `GaussianRandomSequenceGenerator`, `GaussianLowDiscrepancySequenceGenerator` |
| Brownian-bridge ordering | `BrownianBridge`, `SobolBrownianBridgeRsg`, `Burley2020SobolBrownianBridgeRsg` |
| Brownian generators (multi-factor) | `MTBrownianGenerator`, `SobolBrownianGenerator`, `Burley2020SobolBrownianGenerator` (with their factories) |
| Path generators | `GaussianPathGenerator`, `GaussianSobolPathGenerator`, `GaussianMultiPathGenerator`, `GaussianSobolMultiPathGenerator` |

## The MC engine kwarg

For the pre-built MC engines, the choice of generator family is a string kwarg:

```python
engine = ql.MCEuropeanEngine(
    process, "PseudoRandom",
    timeSteps=100,
    antitheticVariate=True,        # mirror Gaussian draws
    requiredSamples=100_000,
    seed=42,                       # only effective for "PseudoRandom"
)
```

`"PseudoRandom"` selects the MT pipeline. `"LowDiscrepancy"` selects a Sobol pipeline (the `seed` argument is then ignored).

## Common pitfalls

- **Reproducibility**: only the `"PseudoRandom"` pipeline respects `seed`. Two MT runs with the same seed give identical prices. Sobol is deterministic regardless of the `seed` argument.
- **Comparing prices across generators**: a price difference between MT and Sobol at the same `requiredSamples` is *not* a bug. The MT result has MC noise; the Sobol result does not.

## See also

- {doc}`/api/math`: `MersenneTwisterUniformRng`, `SobolRsg`, `Burley2020SobolRsg`, all transformations
- {doc}`/api/methods`: `BrownianBridge`, path / multi-path generators, sample types
- {doc}`/api/pricingengines`: MC engines and their generator choices
- {doc}`/cookbook/index`: convergence study recipe
