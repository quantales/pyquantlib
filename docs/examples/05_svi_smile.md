# SVI Volatility Smile

SVI volatility smile parametrization and visualization.

```{note}
View the full notebook: [05_svi_smile.ipynb](https://github.com/quantales/pyquantlib/blob/main/examples/05_svi_smile.ipynb)
```

The Stochastic Volatility Inspired (SVI) model is a popular parametric form for volatility smiles, widely used in equity and FX markets.

## Quick Preview

```python
import pyquantlib as ql

# SVI parameters: [a, b, sigma, rho, m]
params = [0.04, 0.1, 0.3, -0.4, 0.0]

# Create smile section (T=1y, F=100)
smile = ql.SviSmileSection(1.0, 100.0, params)

# Query volatilities
print(f"ATM vol: {smile.volatility(100.0):.4f}")
print(f"90 strike vol: {smile.volatility(90.0):.4f}")
print(f"110 strike vol: {smile.volatility(110.0):.4f}")
```

## The SVI Formula

SVI parametrizes total variance $w(k) = \sigma^2 T$ as:

$$w(k) = a + b \left( \rho (k - m) + \sqrt{(k - m)^2 + \sigma^2} \right)$$

where $k = \log(K/F)$ is log-moneyness.

## Parameter Effects

| Parameter | Effect |
|-----------|--------|
| `a` | Vertical translation (overall level) |
| `b` | Wing steepness |
| `sigma` | ATM curvature (sharpness) |
| `rho` | Skew/asymmetry |
| `m` | Horizontal translation |

The notebook includes interactive plots showing how each parameter affects the smile shape.

## Validation

```python
# Check no-arbitrage constraints
ql.checkSviParameters(0.04, 0.1, 0.3, -0.4, 0.0, 1.0)

# Compute total variance directly
k = 0.1  # log-moneyness
w = ql.sviTotalVariance(0.04, 0.1, 0.3, -0.4, 0.0, k)
```

Download the [full notebook](https://github.com/quantales/pyquantlib/blob/main/examples/05_svi_smile.ipynb) for visualization and detailed examples.
