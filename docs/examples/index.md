# Examples

Jupyter notebooks demonstrating PyQuantLib usage.

```{note}
These examples require PyQuantLib to be installed. See {doc}`/installation` for setup.
```

Users familiar with QuantLib-Python (SWIG) will find the API similar.

## Available Examples

```{toctree}
:maxdepth: 1

01_hello_pyquantlib
02_numpy_interoperability
03_equity_option
04_svi_smile
05_modified_kirk_engine
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
| {doc}`01_hello_pyquantlib` | European option pricing with Black-Scholes |
| {doc}`02_numpy_interoperability` | Array and Matrix conversion with NumPy |
| {doc}`03_equity_option` | Equity options with multiple pricing engines |
| {doc}`04_svi_smile` | SVI volatility smile parametrization |
| {doc}`05_modified_kirk_engine` | Custom Python pricing engine for spread options |
