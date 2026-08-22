# Examples

End-to-end notebooks, rendered with their outputs. Most port a QuantLib C++ example to PyQuantLib, so the numbers can be checked directly against QuantLib's own reference output.

Where the {doc}`/cookbook/index` isolates one pattern per recipe, these notebooks run a full workflow: market data in, curve or model built, instrument priced, results tabulated.

```{toctree}
:maxdepth: 1

notebooks/hello_pyquantlib
notebooks/equity_option
notebooks/bonds
notebooks/multicurve_bootstrapping
notebooks/cds
notebooks/bermudan_swaption
notebooks/inflation_derivatives
notebooks/replication
notebooks/spread_option
notebooks/svi_smile
notebooks/numpy_interoperability
```

## Notebook index

| Notebook | What it covers |
|---|---|
| {doc}`notebooks/hello_pyquantlib` | The shortest complete path: build a Black-Scholes process, price a European option, read the Greeks. |
| {doc}`notebooks/equity_option` | Port of QuantLib's `EquityOption`: European, Bermudan, and American payoffs across analytic, binomial, MC, and FD engines. |
| {doc}`notebooks/bonds` | Port of QuantLib's `Bonds`: bootstrap a curve from deposits and swaps, then price zero-coupon, fixed-rate, and floating-rate bonds off it. |
| {doc}`notebooks/multicurve_bootstrapping` | Port of QuantLib's `MulticurveBootstrapping`: an OIS discount curve plus forwarding curves bootstrapped against it. |
| {doc}`notebooks/cds` | Port of QuantLib's `CDS`: bootstrap a hazard-rate curve from quoted spreads and reprice the contracts. |
| {doc}`notebooks/bermudan_swaption` | Port of QuantLib's `BermudanSwaption`: calibrate short-rate models to the swaption grid and price the Bermudan. |
| {doc}`notebooks/inflation_derivatives` | The inflation stack: index fixings, zero and year-on-year curves, and inflation-linked instruments. |
| {doc}`notebooks/replication` | Port of QuantLib's `Replication`: static replication of a barrier option with a portfolio of vanillas. |
| {doc}`notebooks/spread_option` | Spread options priced with the built-in `KirkEngine` alongside the pure-Python `ModifiedKirkEngine`. |
| {doc}`notebooks/svi_smile` | Fitting an SVI parameterisation to a volatility smile and wrapping it as a `SmileSection`. |
| {doc}`notebooks/numpy_interoperability` | `Array` / `Matrix` conversions, zero-copy semantics, and vectorised pricing loops. |

## Running them locally

The notebooks live in [`examples/`](https://github.com/quantales/pyquantlib/tree/main/examples) in the repository and run against an installed PyQuantLib:

```bash
pip install -e ".[examples]"
cd examples
jupyter notebook
```

```{note}
Outputs shown here are committed with the notebooks rather than regenerated at
build time, so they reflect the PyQuantLib version current at the last refresh.
Re-running locally against a newer version may produce small numerical
differences.
```
