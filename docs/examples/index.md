# Examples

Jupyter notebooks demonstrating PyQuantLib usage.

```{note}
These examples require PyQuantLib to be installed. See {doc}`/installation` for setup.
```

Users familiar with QuantLib-Python (SWIG) will find the API similar.

## Running the Examples

### Prerequisites

```bash
pip install -e ".[examples]"
```

### Launch

```bash
cd examples
jupyter notebook
```

## Available Examples

| Notebook | Description |
|----------|-------------|
| [01_hello_pyquantlib](https://github.com/quantales/pyquantlib/blob/main/examples/01_hello_pyquantlib.ipynb) | European option pricing with Black-Scholes |
| [02_numpy_interoperability](https://github.com/quantales/pyquantlib/blob/main/examples/02_numpy_interoperability.ipynb) | Array and Matrix conversion with NumPy |
| [03_equity_option](https://github.com/quantales/pyquantlib/blob/main/examples/03_equity_option.ipynb) | Equity options with multiple pricing engines |
| [04_svi_smile](https://github.com/quantales/pyquantlib/blob/main/examples/04_svi_smile.ipynb) | SVI volatility smile parametrization |
| [05_modified_kirk_engine](https://github.com/quantales/pyquantlib/blob/main/examples/05_modified_kirk_engine.ipynb) | Custom Python pricing engine for spread options |
