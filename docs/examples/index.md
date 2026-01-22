# Examples

Jupyter notebooks demonstrating PyQuantLib usage.

```{note}
These examples require PyQuantLib to be installed. See {doc}`/installation` for setup.
```

Users familiar with QuantLib-Python (SWIG) will find the API similar.

## Available Examples

```{toctree}
:maxdepth: 1

01_option_pricing
02_numpy_interoperability
03_modified_kirk_engine
05_svi_smile
```

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

## Example Overview

| Notebook | Description |
|----------|-------------|
| {doc}`01_option_pricing` | European option pricing with Black-Scholes |
| {doc}`02_numpy_interoperability` | Array and Matrix conversion with NumPy |
| {doc}`03_modified_kirk_engine` | Custom Python pricing engine for spread options |
| {doc}`05_svi_smile` | SVI volatility smile parametrization |
